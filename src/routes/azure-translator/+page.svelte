<script lang="ts">
	import { onDestroy } from 'svelte';

	let srcLang = 'es';
	let tgtLang = 'en';

	let finalTranscript = '';
	let partialTranscript = '';
	$: transcription = (finalTranscript + partialTranscript).trim();

	let translation = '';
	let detectedLang = '';
	let langWarning = '';

	let isLive = false;
	let isBusy = false;

	// Avoid TS “implicit any”
	let socket: any = null;

	let audioCtx: AudioContext | null = null;
	let source: MediaStreamAudioSourceNode | null = null;
	let worklet: AudioWorkletNode | null = null;
	let mute: GainNode | null = null;
	let mediaStream: MediaStream | null = null;

	let capture: 'mic' | 'system' = 'mic';
	let surface: 'auto' | 'screen' | 'window' | 'tab' = 'auto';

	let isSharingSystem = false;
	let systemStream: MediaStream | null = null;
	let ghostVideo: HTMLVideoElement | null = null;
	let lastSurfacePicked = '';
	let captureHint = '';

	let autoDetect = true;

	function short(lang: string) {
		return (lang || 'en').split('-')[0];
	}

	function getSocketBase(): string {
		const origin = window.location.origin;
		const viteBase = (import.meta as any)?.env?.VITE_WS_BASE || '';
		const isLocalPage =
			window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

		if (!isLocalPage && typeof viteBase === 'string' && viteBase.includes('localhost')) {
			return origin;
		}
		if (typeof viteBase === 'string' && viteBase.trim()) return viteBase.trim();
		return origin;
	}

	async function initAzureLive() {
		if (socket?.connected) return;

		const mod = await import('socket.io-client');
		const io = mod.io;

		const base = getSocketBase();
		const ns = '/azure-live';
		const path = '/socket.io';

		socket = io(base + ns, {
			path,
			transports: ['websocket', 'polling'],
			withCredentials: true,
			auth: { src_lang: srcLang, tgt_lang: tgtLang, auto_detect: autoDetect }
		});

		socket.on('connect', () => console.log('[azure-live] connected', socket.id, 'base=', base));
		socket.on('connect_error', (err: any) =>
			console.warn('[azure-live] connect_error:', err?.message || err)
		);
		socket.on('disconnect', (reason: any) => console.log('[azure-live] disconnected:', reason));

		socket.off('partial_result');
		socket.off('final_result');
		socket.off('final_translation');
		socket.off('lang_detected');
		socket.off('lang_warning');
		socket.off('langs_updated');
		socket.off('auto_detect_updated');

		socket.on('partial_result', (m: any) => {
			// console.log('[azure-live] partial:', m);
			partialTranscript = (m?.text ?? '').trim();
		});

		socket.on('final_result', (m: any) => {
			console.log('[azure-live] FINAL RECEIVED:', m);
			const txt = (m?.text ?? '').trim();
			if (!txt) return;
			finalTranscript += (finalTranscript ? '\n' : '') + txt;
			partialTranscript = '';
		});

		socket.on('final_translation', (m: any) => {
			console.log('[azure-live] TRANSLATION RECEIVED:', m);
			const txt = (m?.translation ?? '').trim();
			if (!txt) return;
			translation += (translation ? '\n' : '') + txt;
		});

		socket.on('lang_detected', (m: any) => {
			detectedLang = m?.detected || '';
		});

		socket.on('lang_warning', (m: any) => {
			const spoken = short(m?.detected || '');
			const expected = short(srcLang);
			if (spoken && expected && spoken !== expected) {
				langWarning = `Language mismatch: speaking “${spoken}”, but “From” is set to “${expected}”.`;
			}
		});

		socket.on('langs_updated', () => {
			const stamp = new Date().toLocaleTimeString();
			const divider = `\n—— ${stamp} • Switched: ${short(srcLang)} → ${short(tgtLang)} ——\n`;
			finalTranscript += divider;
			translation += divider;
			partialTranscript = '';
		});

		socket.on('auto_detect_updated', (m: any) => {
			autoDetect = !!m?.enabled;
		});
	}

	function swapLangs() {
		const oldSrc = srcLang;
		srcLang = tgtLang;
		tgtLang = oldSrc;
		if (isLive && socket?.connected)
			socket.emit('set_langs', { src_lang: srcLang, tgt_lang: tgtLang });
	}

	async function startSystemShare() {
		if (!navigator.mediaDevices?.getDisplayMedia) {
			alert('System audio capture is not supported in this browser.');
			return;
		}
		if (isSharingSystem) return;

		const video: any = { cursor: 'never' };
		if (surface === 'screen') video.displaySurface = 'monitor';
		if (surface === 'window') video.displaySurface = 'window';
		if (surface === 'tab') video.displaySurface = 'browser';

		const dm = await navigator.mediaDevices.getDisplayMedia({
			video,
			audio: true
		});

		if (!ghostVideo) {
			ghostVideo = document.createElement('video');
			ghostVideo.muted = true;
			ghostVideo.playsInline = true;
			ghostVideo.style.cssText =
				'position:fixed;width:1px;height:1px;opacity:0;pointer-events:none;';
			document.body.appendChild(ghostVideo);
		}
		ghostVideo.srcObject = dm;
		try {
			await ghostVideo.play();
		} catch {}

		systemStream = dm;
		isSharingSystem = true;

		const v = dm.getVideoTracks()[0];
		lastSurfacePicked = v ? (v.getSettings() as any).displaySurface || '' : '';
		const a = dm.getAudioTracks();
		captureHint = a.length
			? ''
			: 'Make sure you checked “Share audio” in the picker (Tab/Screen works best).';

		v?.addEventListener('ended', stopSystemShare);
		a?.[0]?.addEventListener('ended', stopSystemShare);
	}

	function stopSystemShare() {
		if (!isSharingSystem) return;
		try {
			systemStream?.getTracks().forEach((t) => t.stop());
		} catch {}
		systemStream = null;
		isSharingSystem = false;

		try {
			if (ghostVideo) {
				ghostVideo.pause();
				(ghostVideo as any).srcObject = null;
				ghostVideo.remove();
			}
		} catch {}
		ghostVideo = null;

		lastSurfacePicked = '';
		captureHint = '';
	}

	async function startLive() {
		if (isBusy) return;
		isBusy = true;
		await initAzureLive();
		langWarning = '';

		socket.emit('start_stream', { src_lang: srcLang, tgt_lang: tgtLang, auto_detect: autoDetect });

		try {
			if (capture === 'system') {
				if (!isSharingSystem || !systemStream) {
					alert('Start System Share first (and check “Share audio”).');
					isBusy = false;
					return;
				}
				mediaStream = systemStream;
			} else {
				mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
			}
		} catch (e) {
			console.warn('[startLive] capture failed', e);
			isBusy = false;
			return;
		}

		const ac = new AudioContext({ sampleRate: 16000 });
		try {
			await ac.audioWorklet.addModule('/pcm16-worklet.js?v=2');
		} catch (err) {
			console.error('[startLive] Worklet failed to load', err);
			isBusy = false;
			return;
		}

		const srcNode = ac.createMediaStreamSource(mediaStream);
		const node = new AudioWorkletNode(ac, 'pcm16-encoder', {
			numberOfInputs: 1,
			numberOfOutputs: 1,
			outputChannelCount: [1],
			channelCount: 1,
			processorOptions: { targetSampleRate: 16000 }
		});

		const muteNode = ac.createGain();
		muteNode.gain.value = 0;

		node.port.onmessage = (ev: MessageEvent) => {
			// console.log('[azure-live] worklet message');
			if (!isLive) return;
			const data: any = (ev as any).data || {};

			if (data.log) {
				console.log('[azure-live-worklet]', data.log);
				return;
			}

			const pcm = data.pcm;
			if (!pcm) return;
			socket.emit('audio_chunk', {
				chunk: new Uint8Array(pcm),
				src_lang: srcLang,
				tgt_lang: tgtLang
			});
		};

		srcNode.connect(node);
		node.connect(muteNode).connect(ac.destination);

		audioCtx = ac;
		source = srcNode;
		worklet = node;
		mute = muteNode;

		finalTranscript = '';
		partialTranscript = '';
		translation = '';
		detectedLang = '';

		isLive = true;
		isBusy = false;
		console.log('[azure-live] Live started successfully');
	}

	function stopLive(e?: Event) {
		if (e) {
			console.log('[azure-live] stopLive called by event:', e.type, e.target);
		} else {
			console.log('[azure-live] stopLive called programmatically');
			// console.log(new Error().stack);
		}

		isLive = false;
		isBusy = false;

		try {
			source?.disconnect();
		} catch {}
		try {
			worklet?.disconnect();
		} catch {}
		try {
			mute?.disconnect();
		} catch {}
		try {
			audioCtx?.close();
		} catch {}

		if (mediaStream && mediaStream !== systemStream) {
			try {
				mediaStream.getTracks().forEach((t) => t.stop());
			} catch {}
		}

		mediaStream = null;
		source = null;
		worklet = null;
		mute = null;
		audioCtx = null;

		console.log('[azure-live] emitting end_of_stream');
		socket?.emit('end_of_stream');
		partialTranscript = '';
	}

	onDestroy(() => {
		console.log('[azure-live] onDestroy triggered');
		try {
			stopLive();
		} catch {}
		try {
			stopSystemShare();
		} catch {}
		try {
			socket?.disconnect();
		} catch {}
		socket = null;
	});
</script>

<div class="wrap">
	<img
		src="/assets/translator_hero.png?v=2"
		alt="Visualizing speech to translation"
		class="hero-img"
		style="width: 100%; max-width: 800px; height: auto; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 2rem;"
	/>
	<h1>Azure Live Translator</h1>

	<div
		class="info-block"
		style="margin-top: 0; margin-bottom: 2rem; border-top: none; padding-top: 0;"
	>
		<div class="info-grid">
			<div class="info-card">
				<h4>🎧 Audio Modes</h4>
				<ul>
					<li><strong>Mic:</strong> Standard microphone input for your voice.</li>
					<li>
						<strong>System Audio:</strong> Captures audio from your computer (Tabs, Windows, or Screen).
					</li>
					<li>
						<strong>Use Case:</strong> Select "System Audio" to transcribe/translate live meetings
						from
						<strong>Teams</strong>, <strong>Zoom</strong>, or <strong>YouTube</strong> videos directly
						into the AI.
					</li>
				</ul>
			</div>
			<div class="info-card">
				<h4>🤖 Architecture & AI</h4>
				<p>
					Audio is streamed via <strong>WebSockets</strong> to a <strong>Flask</strong> backend,
					processed by
					<strong>Azure Cognitive Services</strong>, and can be piped to <strong>LLMs</strong> for:
				</p>
				<ul>
					<li>Sentiment/Emotion Detection</li>
					<li>Summarization & Insights</li>
				</ul>
			</div>
			<div class="info-card warn-card">
				<h4>⚠️ Troubleshooting</h4>
				<ul>
					<li><strong>Browser:</strong> Use Chrome or Edge for best "System Audio" support.</li>
					<li>
						<strong>Permissions:</strong> specific tabs often work better than "Entire Screen" for audio
						sharing.
					</li>
					<li><strong>Silence?</strong> Check if you ticked "Share tab audio" in the popup.</li>
				</ul>
			</div>
		</div>
	</div>

	<div class="row">
		<label
			>From:
			<select
				bind:value={srcLang}
				on:change={() =>
					isLive &&
					socket?.connected &&
					socket.emit('set_langs', { src_lang: srcLang, tgt_lang: tgtLang })}
			>
				<option value="en">English</option>
				<option value="es">Spanish</option>
				<option value="fr">French</option>
				<option value="de">German</option>
				<option value="it">Italian</option>
				<option value="pt">Portuguese</option>
				<option value="hi">Hindi</option>
				<option value="ja">Japanese</option>
				<option value="ko">Korean</option>
				<option value="zh-Hans">Chinese (Simplified)</option>
				<option value="zh-Hant">Chinese (Traditional)</option>
				<option value="ar">Arabic</option>
				<option value="am">Amharic</option>
			</select>
		</label>

		<button on:click={swapLangs} title="Swap languages">⇄ Swap</button>

		<label
			>To:
			<select
				bind:value={tgtLang}
				on:change={() =>
					isLive &&
					socket?.connected &&
					socket.emit('set_langs', { src_lang: srcLang, tgt_lang: tgtLang })}
			>
				<option value="en">English</option>
				<option value="es">Spanish</option>
				<option value="fr">French</option>
				<option value="de">German</option>
				<option value="it">Italian</option>
				<option value="pt">Portuguese</option>
				<option value="hi">Hindi</option>
				<option value="ja">Japanese</option>
				<option value="ko">Korean</option>
				<option value="zh-Hans">Chinese (Simplified)</option>
				<option value="zh-Hant">Chinese (Traditional)</option>
				<option value="ar">Arabic</option>
				<option value="am">Amharic</option>
			</select>
		</label>

		<label style="margin-left:.5rem;">
			<input
				type="checkbox"
				bind:checked={autoDetect}
				on:change={() =>
					socket?.connected && socket.emit('set_auto_detect', { enabled: autoDetect })}
			/>
			Auto-detect
		</label>
	</div>

	<div class="row">
		<label><input type="radio" bind:group={capture} value="mic" /> Mic</label>
		<label style="margin-left:.75rem;"
			><input type="radio" bind:group={capture} value="system" /> System audio</label
		>
	</div>

	<div class="row">
		<label><input type="radio" bind:group={surface} value="auto" /> Auto</label>
		<label style="margin-left:.75rem;"
			><input type="radio" bind:group={surface} value="screen" /> Screen</label
		>
		<label style="margin-left:.75rem;"
			><input type="radio" bind:group={surface} value="window" /> Window</label
		>
		<label style="margin-left:.75rem;"
			><input type="radio" bind:group={surface} value="tab" /> Tab</label
		>
	</div>

	<div class="row">
		<button on:click={startSystemShare} disabled={isSharingSystem}>Start System Share</button>
		<button on:click={stopSystemShare} disabled={!isSharingSystem}>Stop System Share</button>
		<span class="muted"
			>Picked: {lastSurfacePicked || '—'} {captureHint ? `• ${captureHint}` : ''}</span
		>
	</div>

	<div class="row">
		<button on:click={startLive} disabled={isLive || isBusy}>Start Live</button>
		<button on:click={(e) => stopLive(e)} disabled={!isLive || isBusy}>Stop Live</button>
		<span class="muted">Detected: {detectedLang || '—'}</span>
	</div>

	{#if langWarning && isLive}
		<div class="warn">{langWarning}</div>
	{/if}

	<div class="panes">
		<section class="panel">
			<h2>Transcript</h2>
			<pre>{transcription}</pre>
		</section>

		<section class="panel">
			<h2>Translation</h2>
			<pre>{translation}</pre>
		</section>
	</div>
</div>

<style>
	.wrap {
		max-width: 1100px;
		margin: 0 auto;
		padding: 1rem;
	}
	h1 {
		margin: 0.25rem 0 1rem;
	}
	.row {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		align-items: center;
		margin: 0.5rem 0;
	}
	label {
		display: flex;
		gap: 0.35rem;
		align-items: center;
		font-size: 0.95rem;
	}
	select,
	button {
		padding: 0.45rem 0.6rem;
		border: 1px solid #ccc;
		border-radius: 6px;
		background: #fff;
	}
	button {
		cursor: pointer;
		background: #f9f9f9;
	}
	button:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}
	.panes {
		display: grid;
		grid-template-columns: minmax(0, 2fr) minmax(0, 1fr);
		gap: 1rem;
		margin-top: 1rem;
	}
	@media (max-width: 900px) {
		.panes {
			grid-template-columns: 1fr;
		}
	}
	.panel {
		border: 1px solid #e5e7eb;
		border-radius: 12px;
		background: #fff;
		box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
		padding: 0.75rem;
	}
	.panel h2 {
		margin: 0 0 0.5rem;
		font-size: 1rem;
		color: #111827;
	}
	pre {
		margin: 0;
		padding: 0.5rem;
		background: #f9fafb;
		border-radius: 8px;
		white-space: pre-wrap;
		word-break: break-word;
		max-height: 320px;
		overflow: auto;
	}
	.warn {
		margin-top: 0.5rem;
		padding: 0.6rem 0.8rem;
		border: 1px solid #ef4444;
		background: #fee2e2;
		color: #991b1b;
		border-radius: 8px;
	}
	.muted {
		font-size: 0.9rem;
		color: #6b7280;
	}

	/* New Info Section Styles */
	.info-block {
		margin-top: 2.5rem;
		padding-top: 1.5rem;
		border-top: 1px solid #e5e7eb;
	}

	.info-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		gap: 1rem;
	}
	.info-card {
		background: #f9fafb;
		border: 1px solid #e5e7eb;
		border-radius: 10px;
		padding: 1rem;
	}
	.info-card h4 {
		margin: 0 0 0.5rem;
		font-size: 1rem;
		color: #111827;
	}
	.info-card p,
	.info-card li {
		color: #4b5563;
		font-size: 0.95rem;
		line-height: 1.5;
	}
	.info-card ul {
		margin: 0;
		padding-left: 1.25rem;
	}
	.warn-card {
		background: #fff7ed;
		border-color: #fed7aa;
	}
	.warn-card h4 {
		color: #9a3412;
	}
</style>
