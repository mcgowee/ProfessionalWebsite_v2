<script lang="ts">
	import CtAs from './CTAs.svelte';
	import SectionWrapper from './SectionWrapper.svelte';
</script>

<SectionWrapper>
	<div class="hero">
		<h2 class="title">
			<span class="muted">Sakura</span><span class="brand">AI</span> =
			<span class="muted">SQL</span> <span class="brand">AI</span>
		</h2>

		<p class="subtitle">
			<strong>Empower your data journey with AI-driven insights.</strong><br />
			Sakura<span class="brand">AI</span> brings you the future of AI user interfaces and SQL
			analytics.<br />
			Transforming your database interactions and enabling advanced
			<em class="brand">Business Intelligence.</em><br />
			<span class="kanji-note"
				>(Note: The Japanese Kanji for "Love" is <strong>愛</strong>, pronounced "Ai")</span
			>
		</p>

		<CtAs />
	</div>
</SectionWrapper>

<style>
	.hero {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 22px;
		padding: 18px 0 28px;
		text-align: center;
	}

	.title {
		margin: 0;
		font-weight: 700;
		letter-spacing: -0.03em;
		line-height: 1.05;
		max-width: 1100px;
		font-size: clamp(42px, 6vw, 84px);
	}

	.subtitle {
		margin: 0;
		max-width: 980px;
		color: var(--muted);
		line-height: 1.65;
		font-size: clamp(18px, 2.2vw, 24px);
	}

	.muted {
		color: #475569; /* slate-ish */
	}

	.brand {
		color: var(--brand);
	}
</style>
