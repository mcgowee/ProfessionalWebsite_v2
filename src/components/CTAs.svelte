<script lang="ts">
  export let dark: boolean = false;
</script>

<div class="ctaRow">
  <a class:dark class="btn" href="/contact">
    Contact Me
  </a>
</div>

<style>
  .ctaRow {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 12px 16px;
    border-radius: 12px;
    color: #fff;
    text-decoration: none;
    font-weight: 600;
    font-size: 16px;
    background: #1f2937;
    transition: background-color 160ms ease, transform 80ms ease;
    user-select: none;
  }

  .btn:hover {
    background: #4b5563;
    text-decoration: none;
  }

  .btn:active {
    transform: translateY(1px);
  }

  .btn.dark {
    background: #181b34;
  }

  .btn.dark:hover {
    background: #23264a;
  }
</style>
