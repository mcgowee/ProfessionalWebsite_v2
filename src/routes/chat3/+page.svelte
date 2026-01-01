<script lang="ts">
  import Spinner from '../../components/Spinner.svelte';

  let messages: { sender: string; text: string }[] = [];
  let userInput = '';
  let isLoading = false;
  let selectedRoute = 'translation';
  let selectedLanguage = 'spanish';

  async function sendMessage() {
    if (userInput.trim()) {
      messages = [...messages, { sender: 'User', text: userInput }];
      isLoading = true;
      try {
        // Use a project-relative endpoint; adjust /api path as appropriate for your backend proxy
        const response = await fetch(`/api/${selectedRoute}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ text: userInput, language: selectedLanguage })
        });
        if (response.ok) {
          const data = await response.json();
          messages = [...messages, { sender: 'ChatGPT', text: data.response }];
        } else {
          messages = [...messages, { sender: 'ChatGPT', text: 'Failed to get a response from the server.' }];
        }
      } catch (error) {
        messages = [...messages, { sender: 'ChatGPT', text: 'An error occurred while communicating with the server.' }];
      } finally {
        isLoading = false;
        userInput = '';
      }
    }
  }
</script>

<main class="chat3-container">
  <h2 class="chat3-title">Chat with OpenAI ChatGPT</h2>
  <fieldset class="route-select">
    <legend class="visually-hidden">Select API route</legend>
    <label>
      <input type="radio" name="route" value="translation" bind:group={selectedRoute}>
      Translation
    </label>
    <label>
      <input type="radio" name="route" value="customTranslation" bind:group={selectedRoute}>
      Custom Translation
    </label>
  </fieldset>

  {#if selectedRoute === 'customTranslation'}
    <fieldset class="lang-select">
      <legend class="visually-hidden">Select language</legend>
      <label><input type="radio" name="language" value="spanish" bind:group={selectedLanguage}>Spanish</label>
      <label><input type="radio" name="language" value="german" bind:group={selectedLanguage}>German</label>
      <label><input type="radio" name="language" value="japanese" bind:group={selectedLanguage}>Japanese</label>
    </fieldset>
  {/if}

  <div class="chat3-info">
    <strong>
      This chat app uses 
      <a href="https://svelte.dev/" target="_blank" rel="noopener" class="svelte-link">Svelte</a> and 
      <a href="https://pypi.org/project/Flask/" target="_blank" rel="noopener" class="flask-link">Flask</a>.
    </strong>
    <p>
      Powered by <strong>OpenAI's ChatGPT</strong> for language generation and translation demo.
      Explore the <a href="https://python.langchain.com/v0.2/docs/tutorials/llm_chain/" target="_blank" rel="noopener" class="ext-link">LangChain documentation</a> for more.
    </p>
  </div>
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
    <label class="visually-hidden" for="chat3-input">Type your message</label>
    <input
      id="chat3-input"
      class="chat-input"
      bind:value={userInput}
      on:keydown={(e) => e.key === 'Enter' && sendMessage()}
      placeholder="Type your message..."
      autocomplete="off"
    />
    <button class="send-btn" type="button" on:click={sendMessage} disabled={isLoading}>
      Send
    </button>
  </form>
</main>

<style>
.chat3-container {
  max-width: 560px;
  margin: 32px auto 0;
  padding: 24px;
  background: var(--bg, #fff);
  border-radius: var(--radius, 10px);
  box-shadow: var(--shadow-sm, 0 2px 8px rgba(0,0,0,0.04));
  border: 1px solid var(--border, #e6e7e8);
}
.chat3-title {
  margin: 0 0 12px 0;
  font-size: 2rem;
}
.route-select,
.lang-select {
  display: flex;
  gap: 20px;
  margin-bottom: 14px;
}
.route-select label,
.lang-select label {
  font-size: 1rem;
  cursor: pointer;
}
.chat3-info {
  margin-bottom: 16px;
  color: var(--muted, #444);
  font-size: 1rem;
}
.svelte-link { color: #ff3e00; font-weight: bold; }
.flask-link { color: #00af5b; font-weight: bold; }
.ext-link { color: #2e78db; text-decoration: underline; }
.chat-window {
  background: #f8fafd;
  border: 1px solid #dde3e8;
  border-radius: 8px;
  padding: 14px;
  height: 220px;
  overflow-y: auto;
  margin-bottom: 15px;
}
.user-message {
  text-align: right;
  color: #2563eb;
  margin-bottom: 8px;
}
.chatgpt-message {
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
/* Accessibility helper */
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