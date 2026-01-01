<script lang="ts">
	import Conversion from '../components/Conversion.svelte';
	import Hero from '../components/Hero.svelte';
	import Service from '../components/Service.svelte';

	// Keeping these imports commented until you re-enable those sections:
	// import FaQs from '../components/FAQs.svelte';
	// import Reviews from '../components/Reviews.svelte';
</script>

<section class="intro">
	<img class="headshot" src="/headshot.jpg" alt="Earl Leonard McGowen IV" />

	<div class="introText">
		<h1 class="introTitle">Welcome to My Professional Site</h1>
		<p class="introBody">
			Hi, I&apos;m Earl Leonard McGowen IV, a seasoned database programmer, legal analyst, and AI
			enthusiast with over 15 years of experience in database programming and architecture. I
			specialize in creating innovative solutions using cutting-edge technologies. Explore my site
			to learn more about my work and expertise.
		</p>
	</div>
</section>

<main class="main">
	<section class="featured">
		<div class="featured-card">
			<h3>🚀 New: SQL QA Chatbot</h3>
			<p>Ask questions about your data in plain English. Powered by OpenAI & Agentic SQL.</p>
			<a href="/chat2" class="btn-primary">Try SQL Chat</a>
		</div>
		<div class="featured-card">
			<h3>🎙️ Live Translator</h3>
			<p>Real-time speech-to-speech translation using Azure Cognitive Services.</p>
			<a href="/azure-translator" class="btn-secondary">Try Translator</a>
		</div>
	</section>

	<Hero />

	<Service />
	<!--
  <Reviews />
  <FaQs />
  -->

	<Conversion />
</main>

<style>
	.intro {
		margin-top: 22px;
		padding: 18px;
		background: var(--bg);
		border: 1px solid var(--border);
		border-radius: var(--radius);
		box-shadow: var(--shadow-sm);

		display: grid;
		grid-template-columns: 140px 1fr;
		gap: 18px;
		align-items: center;
	}

	.headshot {
		width: 140px;
		height: 140px;
		object-fit: cover;
		border-radius: 999px;
		border: 4px solid var(--brand);
		box-shadow: var(--shadow-sm);
	}

	.introTitle {
		margin: 0 0 10px;
		font-size: 28px;
		line-height: 1.15;
		letter-spacing: -0.01em;
	}

	.introBody {
		margin: 0;
		color: var(--muted);
		font-size: 16px;
		line-height: 1.6;
	}

	.main {
		margin-top: 18px;
		display: flex;
		flex-direction: column;
		gap: 18px;
	}

	.featured {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 18px;
	}

	.featured-card {
		background: var(--surface);
		border: 1px solid var(--border);
		border-radius: var(--radius);
		padding: 20px;
		box-shadow: var(--shadow-sm);
		display: flex;
		flex-direction: column;
		align-items: flex-start;
	}

	.featured-card h3 {
		margin: 0 0 8px;
		font-size: 1.25rem;
	}

	.featured-card p {
		margin: 0 0 16px;
		color: var(--muted);
		line-height: 1.5;
	}

	.btn-primary {
		display: inline-block;
		padding: 10px 16px;
		background: var(--brand);
		color: #fff;
		text-decoration: none;
		border-radius: 8px;
		font-weight: 600;
	}

	.btn-secondary {
		display: inline-block;
		padding: 10px 16px;
		background: var(--surface);
		color: var(--text);
		border: 1px solid var(--border);
		text-decoration: none;
		border-radius: 8px;
		font-weight: 600;
	}

	.btn-primary:hover {
		background: #d946ef;
	}
	.btn-secondary:hover {
		background: #f3f4f6;
	}

	@media (max-width: 600px) {
		.featured {
			grid-template-columns: 1fr;
		}
	}

	@media (max-width: 720px) {
		.intro {
			grid-template-columns: 1fr;
			text-align: left;
		}

		.headshot {
			width: 110px;
			height: 110px;
		}
	}
</style>
