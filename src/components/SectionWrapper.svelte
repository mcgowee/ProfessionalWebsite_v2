<script lang="ts">
  export let id: string | undefined = undefined;
</script>

<section {id} class="section">
  <div class="inner">
    <slot />
  </div>
</section>

<style>
  .section {
    min-height: 100vh;
    padding: 0 20px;
    display: flex;
  }

  .inner {
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    flex: 1;
  }
</style>
