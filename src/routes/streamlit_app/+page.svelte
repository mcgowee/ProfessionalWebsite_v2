<script lang="ts">

  import Spinner from '../../components/Spinner.svelte';
  import { onMount } from 'svelte';

  let messages: Array<{ sender: string; text: string }> = [];

  let userInput = '';
  let isLoading = false;

  let sessionId = 'web-streamlit-' + crypto.randomUUID();

  onMount(() => {
    const saved = localStorage.getItem('streamlit_chat_session_id');
    if (saved) {
      sessionId = saved;
    } else {
      localStorage.setItem('streamlit_chat_session_id', sessionId);
    }
  });

  async function sendMessage() {
    const text = (userInput || '').trim();
    if (!text || isLoading) return;

    messages = [...messages, { sender: 'User', text }];
    isLoading = true;

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: text,
          session_id: sessionId,
          max_tokens: 250
        })
      });

      const data = await response.json().catch(() => ({}));

      if (response.ok) {
        const replyText =
          data.generated_text ??
          data.reply ??
          'No response returned from server.';
        messages = [...messages, { sender: 'AI', text: replyText }];
      } else {
        messages = [...messages, { sender: 'AI', text: `Error: ${data && data.error ? data.error : 'Request failed.'}` }];
      }
    } catch (err) {
      messages = [...messages, { sender: 'AI', text: 'An error occurred while communicating with the server.' }];
    } finally {
      isLoading = false;
      userInput = '';
    }
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter') sendMessage();
  }
</script>

<main class="page">
  <h2 class="title">Chat with Local LLM</h2>

  <div class="info">
    <p>
      <strong>
        This chat application is built with
        <a href="https://svelte.dev/" target="_blank" rel="noopener">Svelte</a>
        on the frontend and
        <a href="https://pypi.org/project/Flask/" target="_blank" rel="noopener">Flask</a>
        as the API backend.
      </strong>
    </p>
    <p>
      It uses your hosted Flask AI service for generating responses.
    </p>
    <p>
      For more detailed information about the LangChain framework and its capabilities, please refer to their
      <a href="https://python.langchain.com/v0.2/docs/tutorials/llm_chain/" target="_blank" rel="noopener">official documentation</a>.
    </p>
  </div>

  <div class="chat-window" aria-live="polite">
    {#each messages as { sender, text }, i}
      <div class="message {sender.toLowerCase()}-message">
        <strong>{sender}:</strong> {text}
      </div>
    {/each}

    {#if isLoading}
      <div class="spinner-row">
        <Spinner />
      </div>
    {/if}
  </div>

  <div class="input-row">
    <label class="visually-hidden" for="streamlit-chat-input">Type your message</label>
    <input
      id="streamlit-chat-input"
      class="chat-input"
      bind:value={userInput}
      on:keydown={handleKeydown}
      placeholder="Type your message..."
      autocomplete="off"
      disabled={isLoading}
    />
    <button class="send-btn" type="button" on:click={sendMessage} disabled={isLoading}>
      Send
    </button>
  </div>
</main>

<style>
  .page {
    max-width: 720px;
    margin: 32px auto 0;
    padding: 24px;
    background: #fff;
    border: 1px solid #e6e7e8;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    font-family: Arial, sans-serif;
  }

  .title {
    margin: 0 0 14px;
    font-size: 2rem;
    color: #1f2937;
  }

  .info {
    margin-bottom: 16px;
    color: #4b5563;
    font-size: 1rem;
    line-height: 1.35;
  }

  .info a {
    color: #2e78db;
    text-decoration: underline;
  }

  .chat-window {
    background: #f8fafb;
    border: 1px solid #dde3e8;
    border-radius: 8px;
    padding: 14px;
    height: 320px;
    overflow-y: auto;
    margin-bottom: 14px;
  }

  .message {
    margin-bottom: 10px;
    padding: 8px 10px;
    border-radius: 8px;
    background: #ffffff;
    border: 1px solid #eef2f5;
    white-space: pre-wrap; /* preserves newlines from AI */
  }

  .user-message {
    text-align: right;
    color: #2563eb;
    background: #f3f7ff;
    border-color: #dbeafe;
  }

  .ai-message {
    text-align: left;
    color: #178100;
    background: #f4fff6;
    border-color: #dcfce7;
  }

  /* Back-compat if any old sender string is "ChatGPT" */
  .chatgpt-message {
    text-align: left;
    color: #178100;
    background: #f4fff6;
    border-color: #dcfce7;
  }

  .spinner-row {
    display: flex;
    justify-content: center;
    margin-top: 10px;
  }

  .input-row {
    display: flex;
    gap: 10px;
    align-items: center;
  }

  .chat-input {
    flex: 1;
    padding: 10px 12px;
    font-size: 1rem;
    border-radius: 8px;
    border: 1px solid #d1d5db;
    outline-offset: 2px;
  }

  .send-btn {
    height: 42px;
    padding: 0 18px;
    background: #4338ca;
    color: #fff;
    border-radius: 8px;
    border: none;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.15s;
  }

  .send-btn:hover {
    background: #3730a3;
  }

  .send-btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
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
</style>
