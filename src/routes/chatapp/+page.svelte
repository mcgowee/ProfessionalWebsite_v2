<script lang="ts">
  import { generateText } from '../../api.ts';
  import { onMount } from "svelte";

  interface Message {
    sender: 'User' | 'Bot';
    text: string;
  }

  let prompt = '';
  let messages: Message[] = [];
  let sessionId = "web-" + crypto.randomUUID();
  let isSending = false;

  let messagesEl: HTMLDivElement | null = null;

  function scrollToBottom() {
    // small delay so DOM updates first
    setTimeout(() => {
      if (messagesEl) messagesEl.scrollTop = messagesEl.scrollHeight;
    }, 0);
  }

  onMount(() => {
    const saved = localStorage.getItem("chat_session_id");
    if (saved) sessionId = saved;
    else localStorage.setItem("chat_session_id", sessionId);
  });

  async function sendMessage() {
    const text = prompt.trim();
    if (!text || isSending) return;

    isSending = true;
    messages = [...messages, { sender: 'User', text }];
    prompt = '';
    scrollToBottom();

    try {
      const botResponse = await generateText(text, 250, sessionId);
      messages = [...messages, { sender: 'Bot', text: botResponse }];
    } catch (err) {
      const msg = err instanceof Error ? err.message : "failed to get response";
      messages = [...messages, { sender: 'Bot', text: `Error: ${msg}` }];
    } finally {
      isSending = false;
      scrollToBottom();
    }
  }
</script>

<style>
  .chat-container {
    max-width: 560px;
    margin: 2rem auto;
    padding: 1.5rem;
    background: var(--bg, #fff);
    border-radius: var(--radius, 10px);
    box-shadow: var(--shadow-sm, 0 2px 8px rgba(0,0,0,0.04));
    border: 1px solid var(--border, #e6e7e8);
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  h1 {
    margin: 0 0 0.5rem 0;
    font-size: 2rem;
  }

  .messages {
    flex-grow: 1;
    overflow-y: auto;
    max-height: 340px;
    padding-right: 0.5rem;
    border: 1px solid var(--border, #e6e7e8);
    border-radius: 8px;
    padding: 0.75rem;
    background: #fff;
  }

  .message {
    margin-bottom: 0.5rem;
    padding: 0.5rem 0.75rem;
    border-radius: 8px;
    background: var(--message-bg, #f8fafd);
    line-height: 1.35;
    word-break: break-word;
  }

  .user {
    color: #2563eb;
    text-align: right;
  }

  .bot {
    color: #178100;
    text-align: left;
  }

  input[type="text"] {
    padding: 0.6rem 0.9rem;
    font-size: 1rem;
    border-radius: 8px;
    border: 1px solid var(--border, #d1d5db);
    outline-offset: 2px;
  }

  button {
    background-color: #4338ca;
    color: white;
    padding: 0.65rem 1.25rem;
    font-size: 1rem;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    transition: background-color 0.2s, opacity 0.2s;
    align-self: flex-start;
  }

  button:hover,
  button:focus {
    background-color: #3730a3;
  }

  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .row {
    display: flex;
    gap: 0.75rem;
    align-items: center;
  }

  .row input {
    flex: 1;
  }
</style>

<div class="chat-container">
  <h1>Chatbot</h1>

  <div class="messages" bind:this={messagesEl}>
    {#each messages as m, index}
      {#key index}
        <div class="message {m.sender === 'User' ? 'user' : 'bot'}" role="article" aria-label={`${m.sender} message`}>
          <strong>{m.sender}:</strong> {m.text}
        </div>
      {/key}
    {/each}
  </div>

  <div class="row">
    <input
      type="text"
      bind:value={prompt}
      placeholder="Type your message..."
      on:keydown={(e) => e.key === 'Enter' && sendMessage()}
      aria-label="Chat input"
      disabled={isSending}
    />
    <button on:click={sendMessage} type="button" disabled={isSending || !prompt.trim()}>
      {isSending ? 'Sending…' : 'Send'}
    </button>
  </div>
</div>
