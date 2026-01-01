<svelte:head>
  <title>Projects | Earl McGowen</title>
  <meta
    name="description"
    content="Project case studies showcasing AI, data engineering, data warehousing, and analytics work: SQL agents, RAG, predictive modeling, and dashboarding."
  />
</svelte:head>

<div class="page">
  <section class="hero">
    <div class="hero__inner">
      <p class="kicker">Portfolio</p>
      <h1>Projects</h1>
      <p class="subtitle">
        Case studies that show how I design and build real-world systems across
        <strong>AI</strong>, <strong>data engineering</strong>, <strong>data warehousing</strong>,
        and <strong>analytics</strong>.
      </p>

      <div class="hero__actions">
        <a class="btn btn--primary" href="/projects/sql-agent">Featured: SQL Analytics Agent</a>
        <a class="btn btn--ghost" href="/contact">Contact</a>
      </div>

      <p class="note">
        Each project page focuses on evidence: problem, architecture, tech stack, guardrails, and outcomes.
      </p>
    </div>
  </section>

  <section class="content">
    <div class="grid">
      <!-- Featured -->
      <article class="card card--featured">
        <div class="card__top">
          <div>
            <p class="tag tag--featured">Featured</p>
            <h2>SQL Analytics Agent</h2>
            <p class="desc">
              Natural-language analytics over relational data using a controlled LLM agent with
              read-only guardrails and explainability.
            </p>
          </div>
          <div class="stack">
            <span class="pill">SvelteKit</span>
            <span class="pill">Flask</span>
            <span class="pill">LLM</span>
            <span class="pill">SQL</span>
          </div>
        </div>

        <div class="card__actions">
          <a class="btn btn--primary" href="/projects/sql-agent">Read Case Study</a>
          <!-- Update if/when you move chat4 to /demos/sql-chat -->
          <a class="btn btn--ghost" href="/chat2">Live Demo</a>
        </div>

        <ul class="bullets">
          <li>Schema-grounded SQL generation</li>
          <li>Read-only constraints + row limits + timeouts</li>
          <li>Explainability via generated SQL + structured results</li>
        </ul>
      </article>

      <!-- Project: Predictive Modeling (placeholder) -->
      <article class="card">
        <p class="tag">In Progress</p>
        <h2>Predictive No-Show Modeling</h2>
        <p class="desc">
          End-to-end predictive analytics workflow for appointment no-shows:
          feature engineering, model evaluation (ROC/PR-AUC), and deployment plan.
        </p>
        <div class="stack">
          <span class="pill">Python</span>
          <span class="pill">ML</span>
          <span class="pill">Evaluation</span>
          <span class="pill">Analytics</span>
        </div>

        <div class="card__actions">
          <button class="btn btn--ghost btn--disabled" disabled>
            Case Study Soon
          </button>
        </div>

        <p class="tiny">
          Tip: When ready, create <code>/projects/predictive-modeling</code>.
        </p>
      </article>

      <!-- Project: Data Warehouse (placeholder) -->
      <article class="card">
        <p class="tag">In Progress</p>
        <h2>Data Warehouse & ETL Design</h2>
        <p class="desc">
          Dimensional modeling, governance-aware pipelines, and analytics-ready marts.
          Focus on reliability, auditability, and BI performance.
        </p>
        <div class="stack">
          <span class="pill">SQL</span>
          <span class="pill">DW</span>
          <span class="pill">ETL</span>
          <span class="pill">BI</span>
        </div>

        <div class="card__actions">
          <button class="btn btn--ghost btn--disabled" disabled>
            Case Study Soon
          </button>
        </div>

        <p class="tiny">
          Tip: When ready, create <code>/projects/data-warehouse</code>.
        </p>
      </article>

      <!-- Project: RAG / Agents (placeholder) -->
      <article class="card">
        <p class="tag">In Progress</p>
        <h2>RAG for Analytics</h2>
        <p class="desc">
          Retrieval-augmented generation patterns for internal knowledge + analytics context,
          with evaluation, prompt-injection resistance, and monitoring.
        </p>
        <div class="stack">
          <span class="pill">RAG</span>
          <span class="pill">Embeddings</span>
          <span class="pill">Eval</span>
          <span class="pill">Observability</span>
        </div>

        <div class="card__actions">
          <button class="btn btn--ghost btn--disabled" disabled>
            Case Study Soon
          </button>
        </div>

        <p class="tiny">
          Tip: When ready, create <code>/projects/rag-analytics</code>.
        </p>
      </article>
    </div>

    <section class="footer-cta">
      <div class="footer-cta__inner">
        <h2>Want to see a specific skill?</h2>
        <p>
          If you’re hiring for AI + data engineering or analytics, I can tailor a short demo or case study
          to your stack (SQL Server, Postgres, dbt, Power BI, Python, etc.).
        </p>
        <div class="footer-cta__actions">
          <a class="btn btn--primary" href="/contact">Reach Out</a>
          <a class="btn btn--ghost" href="/about">About Me</a>
        </div>
      </div>
    </section>
  </section>
</div>

<style>
.page{
  color: var(--text);
  background:
    radial-gradient(900px 600px at 15% 0%, rgba(255, 79, 163, 0.18), transparent 60%),
    radial-gradient(700px 500px at 85% 10%, rgba(255, 123, 189, 0.14), transparent 55%),
    var(--bg);
  min-height: 100vh;
  padding: 24px 18px 64px;
}

.hero {
  padding: 56px 18px 20px;
}

.hero__inner {
  max-width: var(--maxw);
  margin: 0 auto;
  padding: 28px;
  border: 1px solid var(--border);
  background: rgba(255,255,255,0.92);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

.kicker {
  margin: 0 0 8px;
  font-size: 12px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--muted);
}

h1 {
  margin: 0 0 10px;
  font-size: 40px;
  line-height: 1.12;
}

.subtitle {
  margin: 0 0 18px;
  color: var(--muted);
  font-size: 16px;
  line-height: 1.6;
  max-width: 75ch;
}

.hero__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 0 0 10px;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 14px;
  border-radius: 12px;
  border: 1px solid var(--border);
  text-decoration: none;
  color: var(--text);
  background: rgba(255,255,255,0.92);
  box-shadow: var(--shadow-sm);
  transition: transform 140ms ease, background 140ms ease, border-color 140ms ease;
}

.btn:hover {
  transform: translateY(-1px);
  background: rgba(255, 79, 163, 0.08);
  border-color: rgba(255, 79, 163, 0.35);
  text-decoration: none;
}

.btn--primary {
  background: rgba(255, 79, 163, 0.18);
  border-color: rgba(255, 79, 163, 0.45);
}

.btn--primary:hover {
  background: rgba(255, 79, 163, 0.26);
  border-color: rgba(255, 79, 163, 0.65);
}

.btn--ghost {
  background: rgba(255,255,255,0.92);
}

.btn--disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.btn--disabled:hover {
  transform: none;
  background: rgba(255,255,255,0.92);
  border-color: var(--border);
}

.note {
  margin: 10px 0 0;
  color: var(--muted-2);
  font-size: 13px;
}

.content {
  padding: 20px 18px 64px;
}

.grid {
  max-width: var(--maxw);
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 14px;
}

.card {
  grid-column: span 6;
  border: 1px solid var(--border);
  background: rgba(255,255,255,0.92);
  border-radius: var(--radius);
  padding: 18px;
  box-shadow: var(--shadow-sm);
}

.card--featured {
  grid-column: span 12;
  background: linear-gradient(180deg, rgba(255, 79, 163, 0.12), rgba(255,255,255,0.92));
  border-color: rgba(255, 79, 163, 0.30);
}

.card__top {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 14px;
  align-items: start;
}

h2 {
  margin: 6px 0 8px;
  font-size: 18px;
  letter-spacing: 0.01em;
}

.desc {
  margin: 0 0 12px;
  line-height: 1.65;
  color: var(--muted);
}

.tag {
  margin: 0;
  display: inline-flex;
  align-items: center;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255, 79, 163, 0.28);
  background: rgba(255, 79, 163, 0.10);
  font-size: 12px;
  color: rgba(0,0,0,0.65);
  width: fit-content;
}

.tag--featured {
  border-color: rgba(255, 79, 163, 0.40);
  background: rgba(255, 79, 163, 0.14);
  color: rgba(0,0,0,0.70);
}

.stack {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: flex-end;
}

.pill {
  border: 1px solid rgba(255, 79, 163, 0.22);
  background: rgba(255,255,255,0.92);
  padding: 8px 10px;
  border-radius: 999px;
  font-size: 13px;
  color: rgba(0,0,0,0.65);
  white-space: nowrap;
}

.card__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 10px 0 10px;
}

.bullets {
  margin: 10px 0 0 18px;
  color: var(--muted);
}

.bullets li {
  margin: 8px 0;
  line-height: 1.6;
}

.tiny {
  margin: 12px 0 0;
  font-size: 12px;
  color: var(--muted-2);
}

code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 0.95em;
  padding: 2px 6px;
  border-radius: 10px;
  border: 1px solid rgba(255, 79, 163, 0.25);
  background: rgba(255, 79, 163, 0.08);
  color: rgba(0,0,0,0.75);
}

.footer-cta {
  max-width: var(--maxw);
  margin: 18px auto 0;
  padding: 0;
  grid-column: 1 / -1;
}

.footer-cta__inner {
  border: 1px solid rgba(255, 79, 163, 0.30);
  background: rgba(255, 79, 163, 0.10);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow-sm);
}

.footer-cta__inner h2 {
  margin: 0 0 8px;
  font-size: 18px;
}

.footer-cta__inner p {
  margin: 0 0 12px;
  color: var(--muted);
  line-height: 1.65;
}

.footer-cta__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

/* Responsive */
@media (max-width: 900px) {
  h1 { font-size: 32px; }
  .card { grid-column: span 12; }
  .card__top { grid-template-columns: 1fr; }
  .stack { justify-content: flex-start; }
}
</style>
