<script lang="ts">
	import { onMount } from 'svelte';

	export let label = 'Menu';
	export let items: { href: string; label: string; desc?: string }[] = [];

	let open = false;
	let rootEl: HTMLDivElement | null = null;
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
		{label} <span class="chev" aria-hidden="true">▾</span>
	</button>

	{#if open}
		<div class="dropdown" role="menu" aria-label={label}>
			{#each items as item}
				<a class="item" href={item.href} role="menuitem" on:click={close}>
					<div class="item__label">{item.label}</div>
					{#if item.desc}
						<div class="item__desc">{item.desc}</div>
					{/if}
				</a>
			{/each}
		</div>
	{/if}
</div>

<style>
	.menu {
		position: relative;
		display: inline-flex;
		align-items: center;
	}

	.trigger {
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

	.trigger:hover {
		background: rgba(255, 79, 163, 0.12);
	}

	.trigger:focus-visible {
		outline: 3px solid rgba(255, 79, 163, 0.35);
		outline-offset: 2px;
	}

	.chev {
		opacity: 0.85;
		font-size: 12px;
		transform: translateY(1px);
	}

	.dropdown {
		position: absolute;
		right: 0;
		top: calc(100% + 10px);
		width: min(420px, 92vw);
		border: 1px solid var(--border);
		background: rgba(255, 255, 255, 0.98);
		border-radius: 14px;
		box-shadow: var(--shadow);
		overflow: hidden;
		z-index: 3000;
	}

	.item {
		display: block;
		padding: 12px 12px;
		text-decoration: none;
		color: var(--text);
	}

	.item:hover {
		background: rgba(255, 79, 163, 0.08);
		text-decoration: none;
	}

	.item__label {
		font-size: 14px;
		font-weight: 800;
		margin: 0 0 4px;
	}

	.item__desc {
		font-size: 12px;
		color: var(--muted);
		line-height: 1.35;
	}
</style>
