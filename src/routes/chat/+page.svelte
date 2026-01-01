<script lang="ts">
  import Spinner from '../../components/Spinner.svelte';
  import { onMount } from 'svelte';

  let messages: { sender: string; text: string }[] = [];
  let userInput = '';
  let isLoading = false;

  // Persist a per-browser session id so conversations don't collide in your DB
  let sessionId = 'web-' + crypto.randomUUID();

  onMount(() => {
    const saved = localStorage.getItem('chat_session_id');
    if (saved) sessionId = saved;
    else localStorage.setItem('chat_session_id', sessionId);
  });

  async function sendMessage() {
    const text = userInput.trim();
    if (!text || isLoading) return;

    messages = [...messages, { sender: 'User', text }];
    isLoading = true;

    try {
      // Calls Nginx -> Flask: POST /api/generate
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: text,
          session_id: sessionId,
          max_tokens: 250
        }),
      });

      const data = await response.json().catch(() => ({}));

      if (response.ok) {
        const replyText =
          data.generated_text ??
          data.reply ??
          'No response returned from server.';
        messages = [...messages, { sender: 'AI', text: replyText }];
      } else {
        const errMsg = data?.error ? `Error: ${data.error}` : 'Failed to get a response from the server.';
        messages = [...messages, { sender: 'AI', text: errMsg }];
      }
    } catch (error) {
      messages = [
        ...messages,
        { sender: 'AI', text: 'An error occurred while communicating with the server.' },
      ];
    } finally {
      isLoading = false;
      userInput = '';
    }
  }
</script>

<main class="chat-container">
  <h2 class="chat-title">Chat with Earl</h2>
  <p class="info">
    <strong>This chat is a simple demo using <span class="svelte-highlight">Svelte</span> front end and <span class="flask-highlight">Flask</span> API AI agent.</strong>
    AI powered by <strong>OpenAI</strong> (via your Flask backend).<br />
    <span class="prototype-label">Initial prototype</span> — <span class="rag-label">Retrieval-Augmented Generation (RAG)</span> and <span class="sql-label">SQL AI agent</span> features in construction.
  </p>

  <div class="chat-window">
    {#each messages as { sender, text }, i}
      <div class="{sender.toLowerCase()}-message">
        <strong>{sender}:</strong> {text}
      </div>
    {/each}

    {#if isLoading}
      <div class="spinner-row"><Spinner /></div>
    {/if}
  </div>

  <form class="input-row" on:submit|preventDefault={sendMessage}>
    <label class="visually-hidden" for="chat-input">Type your message</label>
    <input
      id="chat-input"
      class="chat-input"
      bind:value={userInput}
      on:keydown={(e) => e.key === 'Enter' && sendMessage()}
      placeholder="Type your message..."
      autocomplete="off"
      disabled={isLoading}
    />
    <button class="send-btn" type="button" on:click={sendMessage} disabled={isLoading}>
      Send
    </button>
  </form>
</main>

<style>
.chat-container {
  max-width: 560px;
  margin: 32px auto 0;
  padding: 24px;
  background: var(--bg, #fff);
  border-radius: var(--radius, 10px);
  box-shadow: var(--shadow-sm, 0 2px 8px rgba(0,0,0,0.04));
  border: 1px solid var(--border, #e6e7e8);
}

.chat-title {
  margin-top: 0;
  margin-bottom: 12px;
  font-size: 2rem;
}

.info {
  margin-bottom: 16px;
  color: var(--muted, #555);
  font-size: 1rem;
}

.svelte-highlight { color: #ff3e00; font-weight: bold; }
.flask-highlight { color: #00af5b; font-weight: bold; }
.prototype-label { color: #C72525; font-weight: bold; }
.rag-label { color: #2e78db; font-weight: bold; }
.sql-label { color: #e88809; font-weight: bold; }

.chat-window {
  background: #f8fafd;
  border: 1px solid #dde3e8;
  border-radius: 8px;
  padding: 16px;
  height: 260px;
  overflow-y: auto;
  margin-bottom: 18px;
}

.user-message {
  text-align: right;
  color: #2563eb;
  margin-bottom: 8px;
}
.ai-message {
  text-align: left;
  color: #178100;
  margin-bottom: 8px;
}
.spinner-row {
  display: flex;
  justify-content: center;
  margin-top: 12px;
}

.input-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

.chat-input {
  flex-grow: 1;
  padding: 8px 12px;
  font-size: 1rem;
  border-radius: 8px;
  border: 1px solid #d1d5db;
}

.send-btn {
  padding: 0 18px;
  height: 40px;
  background: #4338ca;
  color: #fff;
  border-radius: 8px;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.13s;
}
.send-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
.send-btn:not(:disabled):hover {
  background: #3730a3;
}

/* Accessibility helper - visually hide label but make it screen-reader accessible */
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
</style>
