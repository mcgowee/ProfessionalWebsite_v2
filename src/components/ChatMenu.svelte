<script lang="ts">
  import { onMount } from 'svelte';

  let open = false;
  let rootEl: HTMLDivElement | null = null;

  type DemoItem = {
    href: string;
    label: string;
    desc?: string;
  };

  const demos: DemoItem[] = [
    { href: '/chat2', label: 'SQL Analytics Agent', desc: 'Natural language → SQL (read-only) + results + SQL shown' },
    { href: '/wordle', label: 'Wordle Solver', desc: 'Constraint solving + scoring heuristics' },
  ];

  const isBrowser = typeof window !== 'undefined' && typeof document !== 'undefined';

  function toggle() {
    open = !open;
  }

  function close() {
    open = false;
  }

  function onKeydown(e: KeyboardEvent) {
    if (e.key === 'Escape') close();
  }

  function onDocClick(e: MouseEvent) {
    const target = e.target as Node | null;
    if (!rootEl || !target) return;
    if (!rootEl.contains(target)) close();
  }

  onMount(() => {
    if (!isBrowser) return;

    document.addEventListener('click', onDocClick, true);
    document.addEventListener('keydown', onKeydown);

    return () => {
      document.removeEventListener('click', onDocClick, true);
      document.removeEventListener('keydown', onKeydown);
    };
  });
</script>

<div class="menu" bind:this={rootEl}>
  <button
    type="button"
    class="trigger"
    aria-haspopup="menu"
    aria-expanded={open}
    on:click|stopPropagation={toggle}
  >
    Demos <span class="chev" aria-hidden="true">▾</span>
  </button>

  {#if open}
    <div class="dropdown" role="menu" aria-label="Demos">
      {#each demos as d}
        <a class="item" href={d.href} role="menuitem" on:click={close}>
          <div class="item__label">{d.label}</div>
          {#if d.desc}
            <div class="item__desc">{d.desc}</div>
          {/if}
        </a>
      {/each}

      <div class="divider"></div>

      <a class="item item--sub" href="/projects/sql-agent" role="menuitem" on:click={close}>
        <div class="item__label">Featured Project: SQL Agent</div>
        <div class="item__desc">Case study + architecture + guardrails</div>
      </a>
    </div>
  {/if}
</div>

<style>
  .menu{
    position: relative;
    display: inline-flex;
    align-items: center;
  }

  .trigger{
    border: 1px solid transparent;
    background: transparent;
    color: var(--text);
    padding: 8px 10px;
    border-radius: 10px;
    cursor: pointer;
    font-size: 14px;
    line-height: 1;
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }

  .trigger:hover{
    background: rgba(255, 79, 163, 0.12);
  }

  .trigger:focus-visible{
    outline: 3px solid rgba(255, 79, 163, 0.35);
    outline-offset: 2px;
  }

  .chev{
    opacity: 0.85;
    font-size: 12px;
    transform: translateY(1px);
  }

  .dropdown{
    position: absolute;
    right: 0;
    top: calc(100% + 10px);
    width: min(420px, 92vw);
    border: 1px solid var(--border);
    background: rgba(255,255,255,0.98);
    border-radius: 14px;
    box-shadow: var(--shadow);
    overflow: hidden;
    z-index: 3000;
  }

  .item{
    display: block;
    padding: 12px 12px;
    text-decoration: none;
    color: var(--text);
  }

  .item:hover{
    background: rgba(255, 79, 163, 0.08);
    text-decoration: none;
  }

  .item__label{
    font-size: 14px;
    font-weight: 800;
    margin: 0 0 4px;
  }

  .item__desc{
    font-size: 12px;
    color: var(--muted);
    line-height: 1.35;
  }

  .divider{
    height: 1px;
    background: rgba(0,0,0,0.08);
    margin: 6px 0;
  }

  .item--sub{
    background: rgba(255, 79, 163, 0.06);
  }

  .item--sub:hover{
    background: rgba(255, 79, 163, 0.10);
  }
</style>
