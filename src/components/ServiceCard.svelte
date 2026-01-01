<script lang="ts">
  type ServiceFeature = {
    featureList: string[];
    description: string;
    imgUrl: string;
  };

  export let serviceFeature: ServiceFeature;
  export let index: number;

  // Alternate layout every other card
  $: reversed = index % 2 === 1;
</script>

<article class="card" class:reversed={reversed}>
  <div class="media">
    <img class="image" src={serviceFeature.imgUrl} alt="" loading="lazy" />
  </div>

  <div class="content">
    <h4 class="headline">
      <slot />
    </h4>

    <p class="desc">{serviceFeature.description}</p>

    {#if serviceFeature.featureList?.length}
      <ul class="bullets">
        {#each serviceFeature.featureList as item}
          <li>{item}</li>
        {/each}
      </ul>
    {/if}
  </div>
</article>

<style>
  .card {
    width: 100%;
    display: grid;
    grid-template-columns: 1fr 1.3fr;
    gap: 18px;

    padding: 16px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow-sm);
    background: var(--bg);
  }

  .card.reversed {
    grid-template-columns: 1.3fr 1fr;
  }

  .card.reversed .media {
    order: 2;
  }

  .media {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .image {
    width: 100%;
    height: auto;
    max-height: 260px;
    object-fit: contain;
    border-radius: 14px;
    background: rgba(0, 0, 0, 0.02);
  }

  .content {
    display: flex;
    flex-direction: column;
    gap: 10px;
    justify-content: center;
    min-width: 0;
  }

  .headline {
    margin: 0;
    font-size: 20px;
    line-height: 1.25;
    letter-spacing: -0.01em;
  }

  .desc {
    margin: 0;
    color: var(--muted);
    line-height: 1.6;
  }

  .bullets {
    margin: 6px 0 0;
    padding-left: 18px;
  }

  .bullets li {
    margin: 6px 0;
    color: var(--muted);
  }

  @media (max-width: 860px) {
    .card,
    .card.reversed {
      grid-template-columns: 1fr;
    }

    .card.reversed .media {
      order: 0;
    }

    .image {
      max-height: 220px;
    }
  }
</style>
