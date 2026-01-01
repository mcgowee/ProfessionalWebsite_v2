<script>
  import Spinner from '../../components/Spinner.svelte';
  import { onMount, tick } from 'svelte';

  /** @typedef {{ sender: string, type: string, text?: string, answer?: string, sql?: string, columns?: string[], rows?: any[] }} ChatMessage */

  /** @type {ChatMessage[]} */
  let messages = [];

  /** @type {string} */
  let userInput = '';

  /** @type {boolean} */
  let isLoading = false;

  /** @type {number} */
  let maxRows = 50;

  /** @type {string} */
  let sessionId = 'web-sql-' + crypto.randomUUID();

  /** @type {HTMLDivElement | null} */
  let chatWindow = null;

  onMount(() => {
    const saved = localStorage.getItem('chat2_session_id');
    if (saved) sessionId = saved;
    else localStorage.setItem('chat2_session_id', sessionId);

    messages = [
      {
        sender: 'AI',
        type: 'info',
        text:
          'Ask a question about the Chinook database. This demo generates SQL under read-only constraints and returns structured results.'
      }
    ];
  });

  /** @param {string} question */
  function setSampleQuestion(question) {
    userInput = question;
  }

  function clearChat() {
    messages = [
      {
        sender: 'AI',
        type: 'info',
        text:
          'Chat cleared. Ask a question about the Chinook database. This demo generates SQL under read-only constraints and returns structured results.'
      }
    ];
  }

  async function scrollToBottom() {
    await tick();
    if (chatWindow) chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  /** @param {any} data */
  function normalizeColumnsAndRows(data) {
    /** @type {any[]} */
    const rows = Array.isArray(data?.rows) ? data.rows : [];

    /** @type {string[]} */
    let columns = Array.isArray(data?.columns) ? data.columns : [];

    if (!columns.length && rows.length && typeof rows[0] === 'object' && rows[0] !== null) {
      columns = Object.keys(rows[0]);
    }

    return { columns, rows };
  }

  /**
   * @param {string[]} columns
   * @param {any[]} rows
   * @param {number} limit
   */
  function renderRowsAsText(columns, rows, limit = 10) {
    const slice = rows.slice(0, limit);
    if (!slice.length) return '';

    const lines = slice.map((r) =>
      columns.map((c) => `${c}=${r && r[c] !== undefined ? r[c] : ''}`).join(' | ')
    );

    return '- ' + lines.join('\n- ');
  }

  async function sendMessage() {
    const question = userInput.trim();
    if (!question || isLoading) return;

    messages = [...messages, { sender: 'User', type: 'text', text: question }];
    isLoading = true;
    await scrollToBottom();

    try {
      const response = await fetch('/api/sql_qa', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, session_id: sessionId, max_rows: maxRows })
      });

      /** @type {any} */
      const data = await response.json().catch(() => ({}));

      if (response.ok) {
        const answer = data.answer ?? data.response ?? 'No answer returned.';
        const sql = data.sql || '';
        const { columns, rows } = normalizeColumnsAndRows(data);

        messages = [
          ...messages,
          {
            sender: 'AI',
            type: 'result',
            answer,
            sql,
            columns,
            rows
          }
        ];
      } else {
        messages = [...messages, { sender: 'AI', type: 'error', text: `Error: ${data?.error || 'Request failed.'}` }];
      }
    } catch {
      messages = [...messages, { sender: 'AI', type: 'error', text: 'An error occurred while communicating with the server.' }];
    } finally {
      isLoading = false;
      userInput = '';
      await scrollToBottom();
    }
  }

  /** @param {KeyboardEvent} e */
  function onInputKeydown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }
</script>

<main class="page">
  <header class="hero">
    <div class="hero__left">
      <h1 class="title">SQL Analytics Agent (Demo)</h1>
      <p class="subtitle">
        Natural language → <strong>read-only</strong> SQL queries on a relational database, with structured results and explainability.
      </p>

      <div class="badges">
        <span class="badge">SvelteKit UI</span>
        <span class="badge">Flask API</span>
        <span class="badge">LLM</span>
        <span class="badge">SQL</span>
        <span class="badge">Chinook DB</span>
      </div>
    </div>

    <div class="hero__right">
      <div class="guardrails">
        <div class="guardrails__title">Guardrails</div>
        <div class="guardrails__row">
          <span class="label">Mode</span>
          <span class="value ok">Read-only</span>
        </div>
        <div class="guardrails__row">
          <span class="label">Max rows</span>
          <span class="value">
            <input class="maxrows" type="number" min="10" max="500" step="10" bind:value={maxRows} />
          </span>
        </div>
        <div class="guardrails__row">
          <span class="label">Session</span>
          <span class="value mono" title={sessionId}>{sessionId}</span>
        </div>
      </div>
    </div>
  </header>

  <section class="db">
    <div class="db__card">
      <div class="db__text">
        <h2 class="h2">Chinook Database</h2>
        <p class="p">
          Chinook is a sample relational database representing a digital media store (artists, albums, tracks, invoices, and customers).
          It’s ideal for demonstrating SQL analytics patterns.
        </p>
        <p class="p">
          Reference:
          <a class="link" href="https://www.sqlitetutorial.net/sqlite-sample-database/" target="_blank" rel="noopener noreferrer">
            SQLite Tutorial – Chinook DB
          </a>
        </p>
      </div>
      <img src="/assets/ChinookDB.png" alt="Chinook Database Schema" class="schema" />
    </div>

    <div class="samples">
      <div class="samples__title">Try an example</div>
      <div class="samples__grid">
        <button type="button" class="chip" on:click={() => setSampleQuestion('What are the genres?')}>
          What are the genres?
        </button>
        <button
          type="button"
          class="chip"
          on:click={() => setSampleQuestion('List the top ten artists with the most albums and add a count.')}
        >
          Top 10 artists by album count
        </button>
        <button type="button" class="chip" on:click={() => setSampleQuestion('Show me all albums by Led Zeppelin.')}>
          Albums by Led Zeppelin
        </button>
        <button type="button" class="chip" on:click={() => setSampleQuestion('What is the average invoice total?')}>
          Average invoice total
        </button>
      </div>
    </div>
  </section>

  <section class="chat">
    <div class="chat__header">
      <h2 class="h2">Chat</h2>
      <div class="chat__actions">
        <a class="smallLink" href="/projects/sql-agent">View case study</a>
        <button class="btn btn--ghost" type="button" on:click={clearChat} disabled={isLoading}>Clear</button>
      </div>
    </div>

    <div class="chatWindow" bind:this={chatWindow} aria-live="polite">
      {#each messages as m (m)}
        {#if m.type === 'result'}
          <div class="msg msg--ai">
            <div class="msg__head">
              <span class="who">AI</span>
              <span class="kind">Result</span>
            </div>

            <details class="panel" open>
              <summary class="panel__summary">Answer</summary>
              <div class="panel__body">{m.answer}</div>
            </details>

            {#if m.rows && m.rows.length}
              <details class="panel">
                <summary class="panel__summary">
                  Top Rows <span class="muted">(showing up to 10)</span>
                </summary>
                <pre class="panel__code">{renderRowsAsText(m.columns ?? [], m.rows, 10)}</pre>
              </details>
            {/if}

            {#if m.sql}
              <details class="panel">
                <summary class="panel__summary">Generated SQL</summary>
                <pre class="panel__code">{m.sql}</pre>
              </details>
            {/if}
          </div>
        {:else if m.sender === 'User'}
          <div class="msg msg--user">
            <div class="msg__head">
              <span class="who">You</span>
              <span class="kind">Question</span>
            </div>
            <div class="msg__text">{m.text}</div>
          </div>
        {:else if m.type === 'error'}
          <div class="msg msg--error">
            <div class="msg__head">
              <span class="who">System</span>
              <span class="kind">Error</span>
            </div>
            <div class="msg__text">{m.text}</div>
          </div>
        {:else}
          <div class="msg msg--info">
            <div class="msg__head">
              <span class="who">{m.sender}</span>
              <span class="kind">Info</span>
            </div>
            <div class="msg__text">{m.text}</div>
          </div>
        {/if}
      {/each}

      {#if isLoading}
        <div class="spinnerRow"><Spinner /></div>
      {/if}
    </div>

    <form class="inputRow" on:submit|preventDefault={sendMessage}>
      <label class="visually-hidden" for="chat2-input">Type your SQL question</label>
      <textarea
        id="chat2-input"
        class="input"
        bind:value={userInput}
        on:keydown={onInputKeydown}
        placeholder="Ask a question about the database… (Enter to send, Shift+Enter for newline)"
        autocomplete="off"
        rows="2"
        disabled={isLoading}
      ></textarea>
      <button class="btn btn--primary" type="button" on:click={sendMessage} disabled={isLoading}>Send</button>
    </form>

    <p class="foot">
      This demo is designed for analytics exploration. It uses read-only constraints and limits result sizes to reduce risk and improve performance.
    </p>
  </section>
</main>

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
  max-width: var(--maxw);
  margin: 0 auto 16px;
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 14px;
  align-items: stretch;
}

.hero__left,
.hero__right,
.db__card,
.samples,
.chat{
  background: rgba(255,255,255,0.92);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-sm);
}

.hero__left { padding: 22px; }
.hero__right { padding: 18px; }

.title {
  margin: 0 0 8px;
  font-size: 34px;
  line-height: 1.15;
  letter-spacing: -0.01em;
}

.subtitle {
  margin: 0 0 14px;
  color: var(--muted);
  line-height: 1.6;
}

.badges {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.badge {
  border: 1px solid rgba(255, 79, 163, 0.25);
  background: rgba(255, 79, 163, 0.08);
  padding: 8px 10px;
  border-radius: 999px;
  font-size: 13px;
  color: rgba(0,0,0,0.65);
}

.guardrails__title {
  font-weight: 800;
  margin-bottom: 10px;
}

.guardrails__row {
  display: grid;
  grid-template-columns: 90px 1fr;
  gap: 10px;
  padding: 8px 0;
  border-top: 1px solid rgba(0,0,0,0.08);
}

.guardrails__row:first-of-type {
  border-top: none;
  padding-top: 0;
}

.label {
  color: var(--muted-2);
  font-size: 13px;
}

.value {
  color: var(--text);
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.ok {
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255, 79, 163, 0.35);
  background: rgba(255, 79, 163, 0.10);
  width: fit-content;
}

.mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  opacity: 0.9;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.maxrows {
  width: 100%;
  max-width: 120px;
  padding: 6px 8px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: rgba(255,255,255,0.9);
  color: var(--text);
}

.db {
  max-width: var(--maxw);
  margin: 0 auto 16px;
  display: grid;
  gap: 14px;
}

.db__card {
  padding: 18px;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 14px;
  align-items: start;
}

.schema {
  width: 280px;
  max-width: 100%;
  border-radius: 14px;
  border: 1px solid var(--border);
  background: rgba(255,255,255,0.9);
}

.h2 {
  margin: 0 0 10px;
  font-size: 18px;
  letter-spacing: 0.01em;
}

.p {
  margin: 0 0 10px;
  color: var(--muted);
  line-height: 1.65;
}

.link {
  color: var(--text);
  text-decoration: underline;
  text-decoration-color: rgba(255, 79, 163, 0.7);
}

.samples { padding: 16px; }

.samples__title {
  font-weight: 800;
  margin-bottom: 10px;
}

.samples__grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.chip {
  border: 1px solid rgba(255, 79, 163, 0.22);
  background: rgba(255,255,255,0.92);
  color: var(--text);
  padding: 10px 12px;
  border-radius: 14px;
  cursor: pointer;
  text-align: left;
  line-height: 1.35;
}

.chip:hover {
  background: rgba(255, 79, 163, 0.08);
}

.chat { padding: 18px; }

.chat__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.chat__actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.smallLink {
  color: var(--text);
  text-decoration: underline;
  text-decoration-color: rgba(255, 79, 163, 0.7);
  font-size: 13px;
}

.chatWindow {
  background: rgba(255,255,255,0.85);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 12px;
  height: 360px;
  overflow-y: auto;
  margin-bottom: 12px;
}

.msg {
  border: 1px solid rgba(0,0,0,0.08);
  border-radius: 14px;
  padding: 10px 12px;
  margin-bottom: 10px;
  background: rgba(255,255,255,0.95);
}

.msg--user {
  background: rgba(255, 79, 163, 0.08);
  border-color: rgba(255, 79, 163, 0.20);
}

.msg--ai {
  background: rgba(255, 123, 189, 0.10);
  border-color: rgba(255, 123, 189, 0.24);
}

.msg--error {
  background: rgba(199, 37, 37, 0.10);
  border-color: rgba(199, 37, 37, 0.22);
}

.msg--info {
  background: rgba(255,255,255,0.95);
}

.msg__head {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 6px;
}

.who {
  font-weight: 900;
  letter-spacing: 0.01em;
}

.kind {
  font-size: 12px;
  color: var(--muted-2);
}

.msg__text {
  color: var(--text);
  line-height: 1.55;
  white-space: pre-wrap;
}

.panel {
  border: 1px solid var(--border);
  border-radius: 14px;
  background: rgba(255,255,255,0.92);
  margin: 8px 0 0;
  overflow: hidden;
}

.panel__summary {
  cursor: pointer;
  padding: 10px 12px;
  user-select: none;
  list-style: none;
  font-weight: 800;
}

.panel__summary::-webkit-details-marker {
  display: none;
}

.panel__body {
  padding: 0 12px 12px;
  color: var(--text);
  line-height: 1.6;
  white-space: pre-wrap;
}

.panel__code {
  margin: 0;
  padding: 0 12px 12px;
  color: rgba(0,0,0,0.78);
  white-space: pre-wrap;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 12px;
  line-height: 1.55;
}

.muted {
  color: var(--muted-2);
  font-weight: 500;
}

.spinnerRow {
  display: flex;
  justify-content: center;
  padding: 8px 0 0;
}

.inputRow {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 10px;
  align-items: start;
}

.input {
  width: 100%;
  resize: vertical;
  min-height: 44px;
  max-height: 160px;
  padding: 10px 12px;
  border-radius: 14px;
  border: 1px solid var(--border);
  background: rgba(255,255,255,0.95);
  color: var(--text);
  line-height: 1.45;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 14px;
  border-radius: 12px;
  border: 1px solid var(--border);
  background: rgba(255,255,255,0.92);
  color: var(--text);
  cursor: pointer;
  transition: transform 140ms ease, background 140ms ease, border-color 140ms ease;
  height: 44px;
  box-shadow: var(--shadow-sm);
}

.btn:hover {
  transform: translateY(-1px);
  background: rgba(255, 79, 163, 0.08);
  border-color: rgba(255, 79, 163, 0.35);
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

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.foot {
  margin: 10px 0 0;
  color: var(--muted-2);
  font-size: 13px;
  line-height: 1.6;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  margin: -1px;
  padding: 0;
  overflow: hidden;
  border: 0;
  clip: rect(0 0 0 0);
}

@media (max-width: 980px) {
  .hero {
    grid-template-columns: 1fr;
  }

  .db__card {
    grid-template-columns: 1fr;
  }

  .schema {
    width: 100%;
  }

  .samples__grid {
    grid-template-columns: 1fr;
  }

  .chatWindow {
    height: 320px;
  }

  .inputRow {
    grid-template-columns: 1fr;
  }

  .btn {
    width: 100%;
  }
}
</style>
