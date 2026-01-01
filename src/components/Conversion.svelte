<script lang="ts">
  import CtAs from './CTAs.svelte';
</script>

<section class="conversion" aria-label="Design ideas call to action">
  <h4 class="title">
    SakuraAI <span class="strong">Design Ideas</span>
  </h4>

  <p class="tagline">✦ Technology meets language meets creativity ✦</p>

  <CtAs dark={true} />
</section>

<style>
  .conversion {
    margin-top: 10px;
    padding: 56px 18px;
    border-radius: var(--radius);
    background: #181b34;
    color: #fff;
    text-align: center;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 16px;
  }

  .title {
    margin: 0;
    font-weight: 650;
    letter-spacing: -0.01em;
    font-size: clamp(18px, 2.3vw, 26px);
  }

  .strong {
    font-weight: 800;
  }

  .tagline {
    margin: 0;
    opacity: 0.92;
    font-size: clamp(14px, 1.8vw, 18px);
    line-height: 1.5;
  }

  @media (max-width: 720px) {
    .conversion {
      padding: 44px 16px;
    }
  }
</style>
