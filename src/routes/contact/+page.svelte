<script lang="ts">
  import Spinner from '../../components/Spinner.svelte';

  let name = '';
  let email = '';
  let message = '';

  let statusMessage = '';
  let statusClass: 'success' | 'error' | '' = '';
  let isLoading = false;

  async function handleSubmit() {
    isLoading = true;
    statusMessage = '';
    statusClass = '';

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, message })
      });

      if (response.ok) {
        statusMessage = 'Email sent successfully!';
        statusClass = 'success';
        name = '';
        email = '';
        message = '';
      } else {
        const text = await response.text().catch(() => '');
        statusMessage = text || 'Failed to send email. Please try again later.';
        statusClass = 'error';
      }
    } catch (err) {
      console.error('Failed to send email:', err);
      statusMessage = 'An error occurred while sending the email. Please try again later.';
      statusClass = 'error';
    } finally {
      isLoading = false;
    }
  }
</script>

<main class="page">
  <header class="header">
    <h2 class="title">
      Contact Earl Leonard McGowen
      {#if isLoading}
        <span class="spinnerWrap" aria-hidden="true"><Spinner /></span>
      {/if}
    </h2>
    <p class="lead">Send a message and I’ll get back to you.</p>
  </header>

  {#if statusMessage}
    <div class="notice" class:success={statusClass === 'success'} class:error={statusClass === 'error'} role="status">
      {statusMessage}
    </div>
  {/if}

  <section class="grid">
    <div class="card">
      <h3 class="cardTitle">Contact Form</h3>

      <form class="form" on:submit|preventDefault={handleSubmit}>
        <div class="field">
          <label for="name">Name</label>
          <input id="name" type="text" bind:value={name} required autocomplete="name" />
        </div>

        <div class="field">
          <label for="email">Email</label>
          <input id="email" type="email" bind:value={email} required autocomplete="email" />
        </div>

        <div class="field">
          <label for="message">Message</label>
          <textarea id="message" bind:value={message} required rows="6"></textarea>
        </div>

        <div class="actions">
          <button type="submit" disabled={isLoading}>
            {#if isLoading}Sending…{:else}Send{/if}
          </button>
        </div>
      </form>
    </div>

    <aside class="card">
      <h3 class="cardTitle">Follow Me</h3>

      <ul class="links">
        <li>
          <a href="https://twitter.com/your-twitter-handle" target="_blank" rel="noopener noreferrer">Twitter</a>
        </li>
        <li>
          <a href="https://www.facebook.com/earlmcgowen/" target="_blank" rel="noopener noreferrer">Facebook</a>
        </li>
        <li>
          <a href="https://www.linkedin.com/in/earl-l-mcgowen-b510884/" target="_blank" rel="noopener noreferrer">LinkedIn</a>
        </li>
        <li>
          <a href="http://earlmcgowen.info/" target="_blank" rel="noopener noreferrer">Legacy Site</a>
        </li>
        <li>
          <a href="https://www.youtube.com/channel/UC-y8DJUix0fjtnLSe5_8bnA" target="_blank" rel="noopener noreferrer">YouTube</a>
        </li>
      </ul>
    </aside>
  </section>
</main>

<style>
  .page {
    max-width: 980px;
    margin: 0 auto;
    padding: 18px 18px 34px;
    color: var(--text);
  }

  .header {
    margin-top: 10px;
    margin-bottom: 14px;
  }

  .title {
    margin: 0;
    font-size: clamp(26px, 3vw, 38px);
    letter-spacing: -0.02em;
    line-height: 1.1;
    display: inline-flex;
    align-items: center;
    gap: 10px;
  }


  .spinnerWrap {
    display: inline-flex;
    transform: translateY(2px);
  }

  .lead {
    margin: 10px 0 0;
    color: var(--muted);
    line-height: 1.6;
  }

  .notice {
    margin-top: 12px;
    padding: 12px 14px;
    border-radius: 12px;
    border: 1px solid transparent;
  }

  .notice.success {
    background: #d4edda;
    color: #155724;
    border-color: rgba(21, 87, 36, 0.22);
  }

  .notice.error {
    background: #f8d7da;
    color: #721c24;
    border-color: rgba(114, 28, 36, 0.22);
  }

  .grid {
    margin-top: 14px;
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    gap: 14px;
  }

  .card {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow-sm);
    padding: 16px;
  }

  .cardTitle {
    margin: 0 0 12px;
    font-size: 20px;
    letter-spacing: -0.01em;
  }

  .form {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .field {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  label {
    font-weight: 650;
    font-size: 14px;
  }

  input,
  textarea {
    width: 100%;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 10px 12px;
    font: inherit;
    background: #fff;
    outline: none;
  }

  input:focus,
  textarea:focus {
    border-color: rgba(0, 0, 0, 0.25);
    box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.06);
  }

  .actions {
    margin-top: 6px;
    display: flex;
    align-items: center;
  }

  button {
    border: 0;
    border-radius: 12px;
    padding: 10px 14px;
    color: #fff;
    background: #1f2937;
    font-weight: 700;
    cursor: pointer;
    transition: background-color 160ms ease, transform 80ms ease;
  }

  button:hover {
    background: #4b5563;
  }

  button:active {
    transform: translateY(1px);
  }

  button:disabled {
    opacity: 0.65;
    cursor: not-allowed;
  }

  .links {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .links a {
    color: var(--brand);
    text-decoration: none;
    font-weight: 650;
  }

  .links a:hover {
    text-decoration: underline;
  }

  @media (max-width: 860px) {
    .grid {
      grid-template-columns: 1fr;
    }
  }
</style>
