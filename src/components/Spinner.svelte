<script lang="ts">
  export let size = 20; // px
  export let color = 'currentColor';
  export let label = 'Loading';
</script>

<span
  class="spinnerWrap"
  role="status"
  aria-live="polite"
  aria-label={label}
>
  <span
    class="spinner"
    style={`width:${size}px;height:${size}px;border-left-color:${color};`}
    aria-hidden="true"
  ></span>
  <span class="srOnly">{label}</span>
</span>

<style>
  .spinnerWrap {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    vertical-align: middle;
  }

  .spinner {
    border: 3px solid rgba(0, 0, 0, 0.15);
    border-radius: 50%;
    animation: spin 800ms linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .srOnly {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }
</style>
