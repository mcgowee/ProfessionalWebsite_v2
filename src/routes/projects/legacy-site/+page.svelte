<main class="page-container">
	<div class="content-wrapper">
		<header class="project-header">
			<h1 class="project-title">Legacy Site: earlmcgowen.info</h1>
			<h2 class="project-subtitle">Archive of Content & Professional History (2008–Present)</h2>
			<div class="meta">
				<span>Earl McGowen</span> • <span>Joomla CMS</span> • <span>LAMP Stack</span>
			</div>
			<div class="links">
				<a
					href="http://www.earlmcgowen.info/"
					target="_blank"
					rel="noopener noreferrer"
					class="btn-visit"
				>
					Visit Functioning Archive ↗
				</a>
			</div>
		</header>

		<section class="section">
			<h3>1. Overview</h3>
			<p>
				<strong>earlmcgowen.info</strong> serves as a verified digital archive of my professional
				and personal history, originally established in 2008. While my modern work focuses on AI,
				Data Engineering, and Cloud Architecture, this site represents a classic approach to content
				management, utilizing the
				<strong>Joomla</strong> CMS to organize documents, events, and informational pages.
			</p>
			<p>
				The site functions as a straightforward <strong>content hub</strong> rather than an interactive
				app, prioritizing stability and information retrieval over dynamic client-side interactions.
			</p>
		</section>

		<section class="section">
			<h3>2. Key Content & Features</h3>
			<div class="grid-2">
				<div class="card">
					<h4>📄 Document Repository</h4>
					<p>A structured archive of professional and legal files (PDF/DOCX), including:</p>
					<ul>
						<li>Resumes & CVs (Historical versions)</li>
						<li>Litigation Drafting & Affidavits</li>
						<li>Interrogatories & Legal Templates</li>
					</ul>
				</div>
				<div class="card">
					<h4>📅 Events Calendar</h4>
					<p>
						A dedicated calendar component tracking historical and recurring events, featuring
						monthly/weekly views and database-driven event management.
					</p>
				</div>
				<div class="card">
					<h4>ℹ️ Informational Structure</h4>
					<p>
						Hierarchical navigation (e.g., <code>/about/about_me</code>) separating content into
						logical categories managed via the CMS backend.
					</p>
				</div>
				<div class="card">
					<h4>🏛️ Legal & Compliance</h4>
					<p>
						Hosts formal legal documentation, reflecting a dual-background in Law (J.D.) and
						Technology. Documents are presented as reference materials rather than active client
						intake tools.
					</p>
				</div>
			</div>
		</section>

		<section class="section">
			<h3>3. Technical Architecture</h3>
			<p>
				Reflecting the "classic web" era of its inception, the site utilizes a robust <strong
					>LAMP Stack</strong
				>:
			</p>
			<ul class="tech-list">
				<li><strong>CMS:</strong> Joomla (Open Source)</li>
				<li><strong>Language:</strong> PHP (Server-Side Rendering)</li>
				<li><strong>Database:</strong> MySQL / MariaDB</li>
				<li><strong>Server:</strong> Apache / NGINX (Linux)</li>
				<li><strong>Rendering:</strong> Template-based HTML & CSS (No modern JS framework)</li>
			</ul>
		</section>

		<section class="section">
			<h3>4. Why It Matters</h3>
			<p>
				In an era of fleeting JavaScript frameworks and ephemeral apps, <strong
					>earlmcgowen.info</strong
				> stands as a testament to longevity and digital preservation. It demonstrates the utility of
				traditional CMS architectures for long-term content hosting and provides a verifiable public record
				of professional milestones spanning nearly two decades.
			</p>
		</section>
	</div>
</main>

<style>
	.page-container {
		max-width: 1024px;
		margin: 0 auto;
		padding: 40px 20px;
		color: #333;
		font-family: 'Inter', sans-serif;
		line-height: 1.6;
	}

	.content-wrapper {
		background: #fff;
		border-radius: 16px;
		padding: 40px;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
		border: 1px solid rgba(0, 0, 0, 0.08);
	}

	.project-header {
		text-align: center;
		margin-bottom: 40px;
		border-bottom: 1px solid #eee;
		padding-bottom: 30px;
	}

	.project-title {
		font-size: 2.5rem;
		font-weight: 800;
		color: #1a202c;
		margin-bottom: 10px;
		line-height: 1.2;
	}

	.project-subtitle {
		font-size: 1.25rem;
		color: #4a5568;
		font-weight: 500;
		margin-bottom: 20px;
	}

	.meta {
		display: flex;
		justify-content: center;
		gap: 12px;
		color: #718096;
		font-size: 0.95rem;
		margin-bottom: 24px;
	}

	.btn-visit {
		display: inline-block;
		background: #2b6cb0;
		color: white;
		padding: 12px 24px;
		border-radius: 8px;
		text-decoration: none;
		font-weight: 600;
		transition: background 0.2s;
	}

	.btn-visit:hover {
		background: #2c5282;
	}

	.section {
		margin-bottom: 40px;
	}

	.section h3 {
		font-size: 1.5rem;
		font-weight: 700;
		color: #2d3748;
		margin-bottom: 20px;
		border-left: 4px solid #4299e1;
		padding-left: 12px;
	}

	.grid-2 {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 20px;
	}

	.card {
		background: #f7fafc;
		padding: 24px;
		border-radius: 12px;
		border: 1px solid #e2e8f0;
	}

	.card h4 {
		margin-top: 0;
		margin-bottom: 12px;
		color: #2b6cb0;
		font-size: 1.1rem;
	}

	.card ul {
		padding-left: 20px;
		margin: 0;
	}

	.tech-list {
		display: flex;
		flex-wrap: wrap;
		gap: 12px;
		list-style: none;
		padding: 0;
	}

	.tech-list li {
		background: #edf2f7;
		padding: 8px 16px;
		border-radius: 20px;
		font-size: 0.9rem;
		color: #4a5568;
		border: 1px solid #cbd5e0;
	}

	@media (max-width: 768px) {
		.grid-2 {
			grid-template-columns: 1fr;
		}
		.project-title {
			font-size: 2rem;
		}
	}
</style>
