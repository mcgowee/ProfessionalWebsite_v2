<script lang="ts">
  import Spinner from '../../components/Spinner.svelte';

  // Define an interface for the query items
  interface QueryItem {
    function: string;
    query: string;
  }

  let messages: { sender: string; text: string }[] = [];
  let userInput = '';
  let isLoading = false;
  let queries: QueryItem[] = []; // Initialize with the correct type

  async function sendMessage() {
    if (userInput.trim()) {
      messages = [...messages, { sender: 'User', text: userInput }];
      isLoading = true;
      try {
        const response = await fetch(`/api/chatbot_query`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ question: userInput })
        });
        if (response.ok) {
          const data = await response.json();
          messages = [...messages, { sender: 'AI', text: data.response }];
          queries = data.queries; // Now TypeScript knows the type of each query
        } else {
          messages = [...messages, { sender: 'AI', text: 'Failed to get a response from the server.' }];
        }
      } catch (error) {
        messages = [...messages, { sender: 'AI', text: 'An error occurred while communicating with the server.' }];
      } finally {
        isLoading = false;
        userInput = '';
      }
    }
  }

  function setSampleQuestion(question: string) {
    userInput = question;
  }
</script>

<main class="chat4-container">
  <h2 class="chat4-title">SQL Query Chatbot</h2>
  
  <div class="chat4-info">
    <p class="info-text">
      This chat application is built with 
      <a href="https://svelte.dev/" target="_blank" rel="noopener" class="tech-link svelte-link">Svelte</a> 
      on the frontend and 
      <a href="https://pypi.org/project/Flask/" target="_blank" rel="noopener" class="tech-link flask-link">Flask</a>
      as the API backend.
    </p>
    <p class="info-text">
      It utilizes Ollama and Llama3 for AI responses. 
      <span class="in-construction">This is an initial prototype.</span> A 
      <span class="rag-feature">Retrieval-Augmented Generation (RAG)</span> backend with data retrieved from social media, documents, and other sources 
      is being created 
      <span class="in-construction">(In Construction)</span>. Additionally, a 
      <span class="sql-agent">SQL AI agent</span> is being developed that can query databases and return analytics based on 
      <span class="sql-chaining">SQL Question and Answer AI Chaining</span>.
    </p>
  </div>

  <div class="chat4-database-info">
    <h3 class="database-info-title">Summary of the Chinook Database</h3>
    <p class="database-info-text">
      The Chinook database is a sample database representing a digital media store. It includes tables for artists, albums, media tracks, invoices, and customers, among others. This makes it an excellent resource for practicing SQL queries and learning database management. The schema includes relationships between these tables, such as artists to albums and invoices to customers.
    </p>
    <a href="https://www.sqlitetutorial.net/sqlite-sample-database/" target="_blank" rel="noopener" class="ext-link">
      For more detailed information...
    </a>
    <img src="/assets/ChinookDB.png" alt="Chinook Database Schema" class="database-schema-image"/>
  </div>

  <div class="sample-questions">
    <button on:click={() => setSampleQuestion("What are the genres?")} class="sample-question-btn">What are the genres?</button>
    <button on:click={() => setSampleQuestion("List the top ten artists with the most albums and add a count.")} class="sample-question-btn">List the top ten artists with the most albums and add a count.</button>
    <button on:click={() => setSampleQuestion("Show me all albums by Led Zeppelin.")} class="sample-question-btn">Show me all albums by Led Zeppelin.</button>
    <button on:click={() => setSampleQuestion("What is the average invoice total?")} class="sample-question-btn">What is the average invoice total?</button>
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
    <label class="visually-hidden" for="chat4-input">Type your SQL question</label>
    <input
      id="chat4-input"
      class="chat-input"
      bind:value={userInput}
      on:keydown={(e) => e.key === 'Enter' && sendMessage()}
      placeholder="Type your SQL question..."
      autocomplete="off"
    />
    <button class="send-btn" type="button" on:click={sendMessage} disabled={isLoading}>
      Send
    </button>
  </form>

  {#if queries.length > 0}
    <div class="queries-section">
      <h3 class="queries-title">Generated SQL Queries</h3>
      <ul class="queries-list">
        {#each queries as query}
          <li class="query-item">
            <strong>Function:</strong> {query.function} 
            <br> 
            <strong>Query:</strong> {query.query}
          </li>
        {/each}
      </ul>
    </div>
  {/if}
</main>

<style>
.chat4-container {
  max-width: 560px;
  margin: 32px auto 0;
  padding: 24px;
  background: var(--bg, #fff);
  border-radius: var(--radius, 10px);
  box-shadow: var(--shadow-sm, 0 2px 8px rgba(0,0,0,0.04));
  border: 1px solid var(--border, #e6e7e8);
}

.chat4-title {
  margin: 0 0 12px 0;
  font-size: 2rem;
}

.chat4-info {
  margin-bottom: 16px;
  color: var(--muted, #444);
  font-size: 1rem;
}

.info-text {
  margin-bottom: 12px;
}

.tech-link {
  color: var(--tech-color, #0d6efd);
  text-decoration: none;
}

.svelte-link { color: #ff3e00; }
.flask-link { color: #00af5b; }

.in-construction {
  color: #dc2626;
  font-weight: bold;
}

.rag-feature {
  color: #4f46e5;
  font-weight: bold;
}

.sql-agent {
  color: #811cf8;
  font-weight: bold;
}

.sql-chaining {
  color: #60a5fa;
  font-weight: bold;
}

.chat4-database-info {
  margin-bottom: 20px;
}

.database-info-title {
  font-size: 1.5rem;
  margin-bottom: 8px;
}

.database-info-text {
  margin-bottom: 12px;
}

.ext-link {
  color: #0d6efd;
  text-decoration: underline;
}

.database-schema-image {
  width: 33%;
  margin-top: 12px;
}

.sample-questions {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
}

.sample-question-btn {
  padding: 8px 16px;
  border-radius: 5px;
  background-color: #f3f4f6;
  color: #2d3748;
  cursor: pointer;
  transition: background-color 0.2s;
}

.sample-question-btn:hover {
  background-color: #e5e7eb;
}

.chat-window {
  background: var(--chat-bg, #f8fafd);
  border: 1px solid var(--chat-border, #dde3e8);
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

.ai-message {
  text-align: left;
  color: #178100;
  margin-bottom: 8px;
}

.spinner-row {
  display: flex;
  justify-content: center;
  align-items: center;
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
  border: 1px solid var(--input-border, #d1d5db);
  outline: none;
}

.send-btn {
  padding: 0 18px;
  height: 40px;
  background-color: #4338ca;
  color: white;
  border-radius: 8px;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.send-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.send-btn:not(:disabled):hover {
  background-color: #3730a3;
}

.queries-section {
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid var(--section-border, #e5e7eb);
}

.queries-list {
  list-style-type: disc;
  padding-left: 1.5rem;
  color: var(--text-color, #2d3748);
}

.query-item {
  margin-bottom: 8px;
  font-size: 0.95rem;
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
  clip: rect(0, 0, 0, 0);
}
</style>