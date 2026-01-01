<script lang="ts">
	type Suggestion = { word: string; score: number };
	type SolveResponse = { remaining_count: number; top_suggestions: Suggestion[]; error?: string };

	type Row = {
		guess: string; // up to 5 letters
		feedback: string; // exactly 5 of b/y/g
	};

	let rows: Row[] = [{ guess: '', feedback: 'bbbbb' }];

	let loading = false;
	let errorMsg = '';
	let result: SolveResponse | null = null;

	const TOP_N = 7;

	function normGuess(s: string) {
		return s
			.toLowerCase()
			.replace(/[^a-z]/g, '')
			.slice(0, 5);
	}

	function normalizeFeedback(s: string) {
		return (s || '')
			.toLowerCase()
			.replace(/[^byg]/g, 'b')
			.padEnd(5, 'b')
			.slice(0, 5);
	}

	function getGuessChar(row: Row, col: number) {
		const g = normGuess(row.guess).padEnd(5, ' ');
		return g[col] === ' ' ? '' : g[col];
	}

	function getFbChar(row: Row, col: number) {
		const fb = normalizeFeedback(row.feedback);
		return fb[col] || 'b';
	}

	function setGuessChar(rowIndex: number, colIndex: number, value: string) {
		const ch = (value || '')
			.toLowerCase()
			.replace(/[^a-z]/g, '')
			.slice(0, 1);

		const row = rows[rowIndex];
		const chars = normGuess(row.guess).padEnd(5, ' ').split('');
		chars[colIndex] = ch || ' ';
		row.guess = chars.join('').trimEnd();
		rows = [...rows];
	}

	function setRowGuess(rowIndex: number, word: string) {
		const w = normGuess(word).padEnd(5, ' ').slice(0, 5);
		rows[rowIndex] = { ...rows[rowIndex], guess: w.trimEnd() };
		rows = [...rows];
	}

	function resetRowFeedback(rowIndex: number) {
		rows[rowIndex] = { ...rows[rowIndex], feedback: 'bbbbb' };
		rows = [...rows];
	}

	function cycleFeedback(rowIndex: number, colIndex: number) {
		const row = rows[rowIndex];
		const fb = normalizeFeedback(row.feedback).split('');

		const cur = fb[colIndex] || 'b';
		fb[colIndex] = cur === 'b' ? 'y' : cur === 'y' ? 'g' : 'b';

		row.feedback = fb.join('');
		rows = [...rows];
	}

	function hasLetter(rowIndex: number, colIndex: number) {
		return getGuessChar(rows[rowIndex], colIndex).length === 1;
	}

	function tryCycleFeedback(rowIndex: number, colIndex: number) {
		// Only allow cycling if there is a letter in that tile
		if (!hasLetter(rowIndex, colIndex)) return;
		cycleFeedback(rowIndex, colIndex);
	}

	function focusTile(rowIndex: number, colIndex: number) {
		requestAnimationFrame(() => {
			document
				.querySelector<HTMLInputElement>(`input[data-row="${rowIndex}"][data-col="${colIndex}"]`)
				?.focus();
		});
	}

	function handleInput(rowIndex: number, colIndex: number, e: Event) {
		const input = e.target as HTMLInputElement;
		setGuessChar(rowIndex, colIndex, input.value);

		const val = (input.value || '').trim();
		if (val && colIndex < 4) {
			focusTile(rowIndex, colIndex + 1);
		}
	}

	function handleKeyDown(rowIndex: number, colIndex: number, e: KeyboardEvent) {
		const key = e.key;

		if (key === 'ArrowLeft') {
			e.preventDefault();
			if (colIndex > 0) focusTile(rowIndex, colIndex - 1);
			return;
		}

		if (key === 'ArrowRight') {
			e.preventDefault();
			if (colIndex < 4) focusTile(rowIndex, colIndex + 1);
			return;
		}

		if (key === 'Backspace') {
			const current = getGuessChar(rows[rowIndex], colIndex);
			if (!current && colIndex > 0) {
				focusTile(rowIndex, colIndex - 1);
			}
			return;
		}
	}

	function addRowAndFocus() {
		const idx = rows.length;
		rows = [...rows, { guess: '', feedback: 'bbbbb' }];
		focusTile(idx, 0);
		return idx;
	}

	function removeLastRow() {
		if (rows.length <= 1) return;
		rows = rows.slice(0, -1);
	}

	function buildPayload() {
		const history: [string, string][] = [];

		for (const r of rows) {
			const guess = normGuess(r.guess);
			const fb = normalizeFeedback(r.feedback);
			if (guess.length === 5) history.push([guess, fb]);
		}

		return { history, top_n: TOP_N };
	}

	function lastRowIndex() {
		return rows.length - 1;
	}

	function isRowBlank(row: Row) {
		return normGuess(row.guess).length === 0;
	}

	function getTargetRowForAutofill() {
		const last = rows[lastRowIndex()];
		if (last && isRowBlank(last)) return lastRowIndex();
		return addRowAndFocus();
	}

	function applySuggestion(word: string) {
		const idx = getTargetRowForAutofill();
		setRowGuess(idx, word);
		resetRowFeedback(idx);
		focusTile(idx, 4);
	}

	async function submit() {
		loading = true;
		errorMsg = '';
		result = null;

		const payload = buildPayload();
		if (!payload.history.length) {
			loading = false;
			errorMsg = 'Enter at least one complete 5-letter guess (with feedback).';
			return;
		}

		try {
			const r = await fetch('/api/wordle/solve', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(payload)
			});

			const data = (await r.json()) as SolveResponse;

			if (!r.ok) {
				errorMsg = data?.error || `Request failed (${r.status}).`;
			} else {
				result = data;
				// Always add a new blank row after solving (like real Wordle flow)
				addRowAndFocus();
			}
		} catch {
			errorMsg = 'Failed to reach server.';
		} finally {
			loading = false;
		}
	}
</script>

<main class="wrap">
	<header class="top">
		<img src="/assets/wordle_hero.jpg?v=2" alt="AI solving word puzzles" class="hero-img" />
		<h1>Wordle Solver</h1>

		<p class="intro">
			This tool narrows the candidate word list using your guess history and Wordle-style feedback:
			<strong>b</strong>=blank, <strong>y</strong>=yellow, <strong>g</strong>=green. It then ranks
			remaining words by <strong>letter frequency</strong> (favoring words with many unique, common letters).
		</p>

		<div class="how">
			<div class="howTitle">How to use</div>
			<ul>
				<li>Type letters — it auto-advances to the next tile.</li>
				<li>Use <strong>ArrowLeft / ArrowRight</strong> to move between tiles.</li>
				<li>Click a tile (only if it has a letter) to cycle feedback: Blank → Yellow → Green.</li>
				<li>
					Click <strong>Solve</strong> to get suggestions. A new blank row is added automatically.
				</li>
				<li>Click a <strong>Top Suggestion</strong> to auto-fill the next row.</li>
			</ul>
		</div>

		<div class="how">
			<div class="howTitle">Technical Implementation</div>
			<p>
				This solver demonstrates <strong>Algorithmic Constraint Satisfaction</strong> and
				<strong>Heuristic Optimization</strong>.
			</p>
			<ul>
				<li>
					<strong>Server-Side Logic (Flask/Python):</strong> The backend maintains a vectorized dictionary
					of 12,000+ words.
				</li>
				<li>
					<strong>Constraint Filtering:</strong> Each guess applies a hard filter (O(N) complexity) to
					the candidate set based on position-dependent (Green) and count-dependent (Yellow) rules.
				</li>
				<li>
					<strong>Dynamic Heuristics:</strong> Instead of static frequency tables, the solver
					assumes the <em>remaining</em> pool is the universe. It recalculates letter frequency distributions
					dynamically after every filter step to suggest the word that maximizes information gain (Entropy).
				</li>
				<li>
					<strong>Tech Stack:</strong> SvelteKit (Frontend) + Flask (API) + NumPy-style array processing.
				</li>
			</ul>
		</div>
	</header>

	<section class="panel">
		<div class="controls">
			<button type="button" class="btn" on:click={() => addRowAndFocus()}>Add Row</button>
			<button type="button" class="btn" on:click={removeLastRow} disabled={rows.length <= 1}>
				Remove Last
			</button>
			<button type="button" class="btn primary" on:click={submit} disabled={loading}>
				{#if loading}Solving…{:else}Solve{/if}
			</button>
		</div>

		<div class="grid" aria-label="Guess history">
			{#each rows as r, rowIndex (rowIndex)}
				<div class="row" aria-label={'Row ' + (rowIndex + 1)}>
					{#each [0, 1, 2, 3, 4] as col}
						<input
							class={'tile ' + getFbChar(r, col)}
							type="text"
							inputmode="text"
							autocomplete="off"
							spellcheck="false"
							maxlength="1"
							value={getGuessChar(r, col)}
							data-row={rowIndex}
							data-col={col}
							aria-label={'Letter ' + (col + 1) + ' row ' + (rowIndex + 1)}
							on:input={(e) => handleInput(rowIndex, col, e)}
							on:keydown={(e) => handleKeyDown(rowIndex, col, e)}
							on:click={() => tryCycleFeedback(rowIndex, col)}
						/>
					{/each}
				</div>
			{/each}
		</div>

		{#if errorMsg}
			<div class="msg error" role="alert">{errorMsg}</div>
		{/if}

		{#if result}
			<div class="results">
				<div class="summary"><strong>Remaining candidates:</strong> {result.remaining_count}</div>

				<h2>Top Suggestions (click to auto-fill)</h2>

				<div class="suggestions" aria-label="Top suggestions">
					{#each result.top_suggestions as s}
						<button
							type="button"
							class="suggestion"
							on:click={() => applySuggestion(s.word)}
							aria-label={'Use suggestion ' + s.word}
						>
							<span class="word">{s.word}</span>
							<span class="score">score {s.score}</span>
						</button>
					{/each}
				</div>
			</div>
		{/if}
	</section>
</main>

<style>
	.wrap {
		max-width: 980px;
		margin: 0 auto;
		padding: 24px 16px 60px;
	}

	.top h1 {
		margin: 0 0 8px;
		font-size: 34px;
		letter-spacing: -0.02em;
	}

	.intro {
		margin: 0;
		color: var(--muted, #555);
		line-height: 1.55;
		max-width: 900px;
	}

	.how {
		margin-top: 14px;
		padding: 14px 14px 10px;
		border: 1px solid rgba(0, 0, 0, 0.1);
		border-radius: 12px;
		background: #fafafa;
	}

	.howTitle {
		font-weight: 800;
		margin-bottom: 6px;
	}

	.how ul {
		margin: 0;
		padding-left: 18px;
		color: #333;
		line-height: 1.5;
	}

	.panel {
		margin-top: 16px;
		padding: 18px;
		border: 1px solid rgba(0, 0, 0, 0.12);
		border-radius: 12px;
		background: #fff;
	}

	.controls {
		display: flex;
		gap: 10px;
		flex-wrap: wrap;
		margin-bottom: 14px;
	}

	.btn {
		border: 1px solid rgba(0, 0, 0, 0.18);
		background: #f7f7f7;
		padding: 10px 12px;
		border-radius: 10px;
		cursor: pointer;
		font-weight: 600;
	}
	.btn:disabled {
		opacity: 0.55;
		cursor: not-allowed;
	}
	.btn.primary {
		background: #111827;
		color: #fff;
		border-color: #111827;
	}

	.grid {
		display: flex;
		flex-direction: column;
		gap: 12px;
	}
	.row {
		display: flex;
		gap: 10px;
		flex-wrap: wrap;
	}

	.tile {
		width: 54px;
		height: 54px;
		border-radius: 12px;
		border: 1px solid rgba(0, 0, 0, 0.22);
		text-align: center;
		font-weight: 900;
		font-size: 20px;
		text-transform: uppercase;
		outline: none;
		cursor: pointer;
		transition:
			transform 0.05s ease,
			box-shadow 0.15s ease,
			border-color 0.15s ease;
	}
	.tile:active {
		transform: scale(0.98);
	}
	.tile:focus {
		box-shadow: 0 0 0 3px rgba(17, 24, 39, 0.12);
		border-color: rgba(0, 0, 0, 0.55);
	}

	.tile.b {
		background: #e5e7eb;
		color: #111;
	}
	.tile.y {
		background: #f59e0b;
		color: #111;
	}
	.tile.g {
		background: #16a34a;
		color: #fff;
	}

	.msg {
		margin-top: 12px;
		padding: 10px 12px;
		border-radius: 10px;
		font-weight: 600;
	}
	.msg.error {
		background: #fee2e2;
		border: 1px solid #fecaca;
		color: #7f1d1d;
	}

	.results {
		margin-top: 16px;
		border-top: 1px solid rgba(0, 0, 0, 0.12);
		padding-top: 14px;
	}
	.summary {
		margin-bottom: 10px;
		color: #111;
	}

	.results h2 {
		margin: 10px 0 10px;
		font-size: 18px;
	}

	/* FIX: show all suggestions (no cutoff). Grid wraps naturally. */
	.suggestions {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
		gap: 10px;
		overflow: visible;
	}

	.suggestion {
		border: 1px solid rgba(0, 0, 0, 0.14);
		background: #f9fafb;
		border-radius: 12px;
		padding: 10px 12px;
		text-align: left;
		cursor: pointer;
		display: flex;
		justify-content: space-between;
		gap: 12px;
		align-items: baseline;
		min-height: 44px;
	}
	.suggestion:hover {
		background: #f3f4f6;
	}
	.suggestion:focus {
		outline: none;
		box-shadow: 0 0 0 3px rgba(17, 24, 39, 0.12);
	}

	.hero-img {
		width: 100%;
		max-width: 800px;
		height: auto;
		border-radius: 12px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
		margin-bottom: 2rem;
	}

	.word {
		font-weight: 900;
		letter-spacing: 0.08em;
		text-transform: uppercase;
	}
	.score {
		color: var(--muted, #666);
		font-weight: 700;
		white-space: nowrap;
	}
</style>
