<script lang="ts">
	import ServiceCard from './ServiceCard.svelte';
	import SectionWrapper from './SectionWrapper.svelte';

	type ServiceFeature = {
		featureList: string[];
		description: string;
		// We'll store the "highlight text" here to avoid index-based logic in the template
		highlight: string;
		imgUrl: string;
	};

	const serviceFeatures: ServiceFeature[] = [
		{
			featureList: [
				'Strategic roadmaps for AI adoption in regulated industries (Healthcare, Finance).',
				'HIPAA-compliant governance frameworks and ethical AI policies.',
				'Vendor evaluation and executive pilot management.'
			],
			description:
				'Navigate the complexities of enterprise AI with a proven leader in governance and implementation.',
			highlight: 'Establish robust <span class="emph">AI Governance & Strategy</span>',
			imgUrl: '/assets/service_0.jpg'
		},
		{
			featureList: [
				'Custom RAG (Retrieval-Augmented Generation) pipelines for internal knowledge bases.',
				'Agentic SQL chatbots that query your database in plain English.',
				'Fine-tuning LLMs for specific domain terminologies.'
			],
			description:
				'Transform your business data into conversational insights using state-of-the-art Generative AI.',
			highlight: 'deploy custom <span class="emph">Generative AI Solutions</span>',
			imgUrl: '/assets/service_2.jpg'
		},
		{
			featureList: [
				'SQL Server Architecture (2008–2022) and Migration strategies.',
				'High-performance ETL pipelines (SSIS + Python integration).',
				'Data Warehouse design for large-scale analytics (Star/Snowflake schemas).'
			],
			description:
				'Build a solid data foundation with over 15 years of expert database engineering.',
			highlight: 'Optimize <span class="emph">Enterprise Data Warehousing</span>',
			imgUrl: '/assets/service_1.jpg'
		},
		{
			featureList: [
				'No-show prediction and behavioral health analytics (Capstone Project).',
				'Classification, Regression, and Clustering models using Scikit-Learn/XGBoost.',
				'Actionable insights from unstructured text via NLP.'
			],
			description: 'Turn historical data into future foresight with rigorous predictive modeling.',
			highlight: 'Drive decisions with <span class="emph">Predictive Analytics</span>',
			imgUrl: '/assets/service_4.jpg'
		},
		{
			featureList: [
				'On-prem NVIDIA GPU server architecture for secure AI workloads.',
				'TensorRT optimization for low-latency inference.',
				'Secure API gateways for internal model deployment.'
			],
			description:
				'Deploy AI securely with specialized infrastructure designed for privacy and performance.',
			highlight: 'Architect <span class="emph">Secure AI Infrastructure</span>',
			imgUrl: '/assets/service_3.jpg'
		},
		{
			featureList: [
				'Automated document review systems for legal discovery.',
				'Privacy audits and compliance reporting tools.',
				'Interdisciplinary bridge between Legal counsel and Technical teams.'
			],
			description:
				'Leverage unique dual-expertise in Law (J.D.) and Technology to solve compliance challenges.',
			highlight: 'Innovate with <span class="emph">Legal Technology & Compliance</span>',
			imgUrl: '/assets/service_5.jpg'
		}
	];
</script>

<SectionWrapper id="services">
	<div class="services">
		<header class="header">
			<p class="kicker">
				Empowering Your Business with <span class="brand">AI, SQL, and Legal Tech</span> Expertise
			</p>
			<h3 class="title">Professional Services</h3>
		</header>

		<div class="cards">
			{#each serviceFeatures as serviceFeature, index}
				<ServiceCard {serviceFeature} {index}>
					<!-- Render HTML safely since we use <span> classes in the string -->
					{@html serviceFeature.highlight}
				</ServiceCard>
			{/each}
		</div>
	</div>
</SectionWrapper>

<style>
	.services {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 26px;
		padding: 18px 0 28px;
	}

	.header {
		text-align: center;
		display: flex;
		flex-direction: column;
		gap: 10px;
	}

	.kicker {
		margin: 0;
		color: var(--muted);
		font-size: 16px;
		line-height: 1.5;
	}

	.brand {
		color: var(--brand);
		font-weight: 700;
	}

	.title {
		margin: 0;
		font-weight: 800;
		letter-spacing: -0.02em;
		line-height: 1.1;
		font-size: clamp(34px, 4.2vw, 56px);
	}

	/* Make sure .emph is globally available or passed down. 
     Since we use @html, the style needs to be global or accessible. 
     Svelte scoped styles won't apply to @html content unless we use :global() */
	:global(.emph) {
		color: var(--brand);
		font-weight: 650;
	}

	.cards {
		width: 100%;
		display: flex;
		flex-direction: column;
		gap: 18px;
	}
</style>
