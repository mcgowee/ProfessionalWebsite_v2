<svelte:head>
  <title>SQL Analytics Agent | Earl McGowen</title>
  <meta
    name="description"
    content="A production-oriented SQL Analytics Agent that converts natural-language questions into read-only SQL queries with guardrails, explainability, and a full-stack SvelteKit + Flask architecture."
  />
</svelte:head>

<div class="page">
  <!-- Hero -->
  <section class="hero">
    <div class="hero__inner">
      <p class="kicker">Project</p>
      <h1>SQL Analytics Agent</h1>
      <p class="subtitle">
        Natural-language analytics over relational data using a controlled LLM agent with
        safety guardrails and explainability.
      </p>

      <div class="hero__meta">
        <div class="pill">SvelteKit</div>
        <div class="pill">Flask</div>
        <div class="pill">LLM (Local/Cloud)</div>
        <div class="pill">SQL</div>
        <div class="pill">Relational DB</div>
      </div>

      <div class="hero__actions">
        <!-- Update href to your canonical demo route (e.g. /demos/sql-chat later) -->
        <a class="btn btn--primary" href="/chat4">View Live Demo</a>
        <a class="btn btn--ghost" href="#architecture">View Architecture</a>
      </div>

      <p class="note">
        Demo runs in <strong>read-only</strong> mode with query constraints to prevent destructive operations.
      </p>
    </div>
  </section>

  <!-- Content -->
  <section class="content">
    <div class="grid">
      <article class="card">
        <h2>The Problem</h2>
        <p>
          Business users often need answers from relational databases but don’t write SQL.
          Dashboards answer predefined questions, while unrestricted LLMs introduce risk when
          connected directly to production data.
        </p>
        <p>
          The challenge is building an AI system that translates natural-language questions into
          <strong>correct SQL</strong>, while enforcing <strong>safety</strong>, <strong>performance</strong>, and
          <strong>auditability</strong>.
        </p>
      </article>

      <article class="card">
        <h2>The Solution</h2>
        <p>
          This SQL Analytics Agent acts as a controlled intermediary between users and a relational database.
          It converts natural-language questions into SQL, validates and constrains queries, executes them
          under read-only access, and returns structured results.
        </p>
        <ul class="bullets">
          <li>Natural language → SQL generation with schema grounding</li>
          <li>Read-only execution + guardrails</li>
          <li>Structured results suitable for analytics workflows</li>
        </ul>
      </article>
    </div>

    <article class="card wide" id="architecture">
      <h2>Architecture Overview</h2>

      <div class="diagram">
        <div class="node">User</div>
        <div class="arrow">→</div>
        <div class="node">SvelteKit UI</div>
        <div class="arrow">→</div>
        <div class="node">Flask API</div>
        <div class="arrow">→</div>
        <div class="node">LLM + Schema Context</div>
        <div class="arrow">→</div>
        <div class="node">SQL Validation</div>
        <div class="arrow">→</div>
        <div class="node">Read-Only DB</div>
        <div class="arrow">→</div>
        <div class="node">Results</div>
      </div>

      <ol class="steps">
        <li>User asks an analytics question in natural language.</li>
        <li>Backend injects approved schema context into the prompt.</li>
        <li>LLM generates SQL (not free-form answers).</li>
        <li>SQL is validated, constrained, and executed in read-only mode.</li>
        <li>Structured results return to the UI for display.</li>
      </ol>
    </article>

    <div class="grid">
      <article class="card">
        <h2>Safety & Guardrails</h2>
        <ul class="bullets">
          <li><strong>Read-only role</strong>: prevents INSERT/UPDATE/DELETE/DDL</li>
          <li><strong>Schema allowlist</strong>: only approved tables/columns exposed</li>
          <li><strong>Row limits</strong>: blocks large result sets</li>
          <li><strong>Timeouts</strong>: prevents long-running queries</li>
          <li><strong>No direct user SQL execution</strong>: queries are generated + validated</li>
        </ul>
        <p class="callout">
          These constraints make the agent safer for real organizational data, not just demos.
        </p>
      </article>

      <article class="card">
        <h2>Explainability</h2>
        <p>
          Trust matters. The system is designed to show how answers are produced:
        </p>
        <ul class="bullets">
          <li>Generated SQL can be reviewed</li>
          <li>Results map directly to database fields</li>
          <li>Failures return structured errors instead of hallucinations</li>
          <li>Query logic aligns with the relational model</li>
        </ul>
      </article>
    </div>

    <article class="card wide">
      <h2>Example Questions</h2>
      <p class="muted">Use these prompts to explore the demo quickly:</p>

      <div class="examples">
        <div class="example">Which customers have the highest total purchases?</div>
        <div class="example">Show monthly sales trends by category.</div>
        <div class="example">Which products have declining revenue over the last year?</div>
        <div class="example">What are the top artists by total track sales?</div>
      </div>

      <p class="muted" style="margin-top: 12px;">
        Each question is translated into SQL, executed safely, and returned as structured data.
      </p>
    </article>

    <div class="grid">
      <article class="card">
        <h2>Technology Stack</h2>

        <h3>Frontend</h3>
        <ul class="bullets">
          <li>SvelteKit</li>
          <li>Scoped component CSS</li>
          <li>Fetch-based API integration</li>
        </ul>

        <h3>Backend</h3>
        <ul class="bullets">
          <li>Python + Flask API</li>
          <li>Prompt-driven SQL generation</li>
        </ul>

        <h3>Data</h3>
        <ul class="bullets">
          <li>Relational database (example: Chinook)</li>
          <li>Explicit schema context exposure</li>
        </ul>
      </article>

      <article class="card">
        <h2>What This Demonstrates</h2>
        <ul class="bullets">
          <li>Safe AI design for structured data</li>
          <li>Analytics-focused SQL generation</li>
          <li>Data governance mindset (constraints + auditability)</li>
          <li>Full-stack delivery (UI + API + data)</li>
          <li>Production-oriented thinking beyond “chatbots”</li>
        </ul>

        <h2 style="margin-top: 18px;">Limitations & Future Work</h2>
        <ul class="bullets">
          <li>Query plan inspection / cost estimation</li>
          <li>Chart-based visualization of results</li>
          <li>Multi-database backends (Postgres, SQL Server)</li>
          <li>Evaluation harness for SQL accuracy</li>
          <li>Role-based access control</li>
        </ul>
      </article>
    </div>

    <section class="cta">
      <div class="cta__inner">
        <h2>Try the Live Demo</h2>
        <p>
          Explore natural-language analytics with read-only constraints and structured results.
        </p>
        <div class="cta__actions">
          <a class="btn btn--primary" href="/chat4">Launch SQL Analytics Agent</a>
          <a class="btn btn--ghost" href="/projects">Back to Projects</a>
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
  max-width: 70ch;
}

.hero__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 0 0 18px;
}

.pill {
  border: 1px solid rgba(255, 79, 163, 0.22);
  background: rgba(255,255,255,0.92);
  padding: 8px 10px;
  border-radius: 999px;
  font-size: 13px;
  color: rgba(0,0,0,0.65);
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
  margin: 0 auto 16px;
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

.card.wide {
  max-width: var(--maxw);
  margin: 0 auto 16px;
  grid-column: span 12;
}

h2 {
  margin: 0 0 10px;
  font-size: 18px;
  letter-spacing: 0.01em;
}

h3 {
  margin: 14px 0 8px;
  font-size: 14px;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.10em;
}

p {
  margin: 0 0 10px;
  line-height: 1.65;
  color: var(--muted);
}

.bullets {
  margin: 10px 0 0 18px;
  color: var(--muted);
}

.bullets li {
  margin: 8px 0;
  line-height: 1.6;
}

.callout {
  margin-top: 12px;
  padding: 10px 12px;
  border-radius: 14px;
  border: 1px solid rgba(255, 79, 163, 0.35);
  background: rgba(255, 79, 163, 0.10);
  color: var(--text);
}

.diagram {
  margin: 12px 0 14px;
  padding: 14px;
  border-radius: var(--radius);
  border: 1px dashed rgba(255, 79, 163, 0.35);
  background: rgba(255,255,255,0.92);
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}

.node {
  padding: 10px 12px;
  border-radius: 14px;
  border: 1px solid rgba(255, 79, 163, 0.22);
  background: rgba(255,255,255,0.96);
  color: var(--text);
  font-size: 13px;
  white-space: nowrap;
}

.arrow {
  color: var(--muted);
  font-size: 16px;
  padding: 0 2px;
}

.steps {
  margin: 0 0 0 18px;
  color: var(--muted);
}

.steps li {
  margin: 8px 0;
  line-height: 1.6;
}

.muted {
  color: var(--muted-2);
}

.examples {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin-top: 10px;
}

.example {
  border: 1px solid var(--border);
  background: rgba(255,255,255,0.92);
  border-radius: 14px;
  padding: 12px;
  color: var(--text);
  font-size: 13px;
  line-height: 1.5;
}

.cta {
  max-width: var(--maxw);
  margin: 22px auto 0;
  padding: 0 0;
}

.cta__inner {
  border: 1px solid rgba(255, 79, 163, 0.30);
  background: rgba(255, 79, 163, 0.10);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow-sm);
}

.cta__inner h2 {
  margin-bottom: 8px;
}

.cta__inner p {
  margin-bottom: 12px;
}

.cta__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

/* Responsive */
@media (max-width: 900px) {
  h1 { font-size: 32px; }
  .card { grid-column: span 12; }
  .examples { grid-template-columns: 1fr; }
}
</style>
