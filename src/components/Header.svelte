<script lang="ts">
	import NavDropdown from './NavDropdown.svelte';
	import { tick } from 'svelte';

	let panel: HTMLDivElement | null = null;
	let mobileOpen = false;

	async function openMenu() {
		mobileOpen = true;
		await tick();
		panel?.focus();
	}

	function closeMenu() {
		mobileOpen = false;
	}

	function onMobileKeydown(e: KeyboardEvent) {
		if (e.key === 'Escape') closeMenu();
	}

	const socials = [
		{ href: 'https://twitter.com/your-twitter-handle', label: 'Twitter' },
		{ href: 'https://www.facebook.com/earlmcgowen/', label: 'Facebook' },
		{ href: 'https://www.linkedin.com/in/earl-l-mcgowen-b510884/', label: 'LinkedIn' },
		{ href: 'https://www.youtube.com/channel/UC-y8DJUix0fjtnLSe5_8bnA', label: 'YouTube' }
	];

	const nav = [
		{ href: '/', label: 'Home' },
		{ href: '/chat2', label: 'SQL Chat' },
		{ href: '/azure-translator', label: 'Translator' },
		{ href: '/projects', label: 'Projects' },
		{ href: '/about', label: 'About' },
		{ href: '/contact', label: 'Contact' }
	];

	const appItems = [
		{ href: '/wordle', label: 'Wordle Solver', desc: 'Constraint solving + heuristics' }
	];

	const legacyItems = [
		{ href: '/chat', label: 'Basic Chat', desc: 'Simple Svelte+Flask prototype' },
		{ href: '/chat3', label: 'Old Translator', desc: 'Previous translation demo' },
		{ href: '/chat4', label: 'SQL Demo', desc: 'Early SQL chatbot prototype' },
		{ href: '/chatapp', label: 'Legacy General Chat', desc: 'Original Llama3 Chatbot' }
	];
</script>

<header class="header">
	<div class="brand">
		<a class="brandLink" href="/" aria-label="Home">
			<img class="logo" src="/logo.jpg" alt="SakuraAI logo" />
		</a>

		<div class="titleBlock">
			<a class="homeTitle" href="/">
				<h1 class="title">Sakura<span class="accent">AI</span></h1>
			</a>
			<p class="subtitle">An Earl McGowen Company</p>
		</div>
	</div>

	<div class="right">
		<div class="socials" aria-label="Social links">
			{#each socials as s}
				<a class="socialLink" href={s.href} target="_blank" rel="noopener noreferrer">
					{s.label}
				</a>
			{/each}
		</div>

		<button
			type="button"
			class="hamburger"
			aria-label="Open menu"
			aria-expanded={mobileOpen}
			on:click={openMenu}
		>
			☰
		</button>
	</div>
</header>

<nav class="nav" aria-label="Primary">
	<ul class="navList">
		{#each nav as item}
			<li class="navItem">
				<a class="navLink" href={item.href}>{item.label}</a>
			</li>
		{/each}

		<li class="navItem">
			<NavDropdown label="Apps" items={appItems} />
		</li>

		<li class="navItem">
			<NavDropdown label="Legacy" items={legacyItems} />
		</li>

		<slot />
	</ul>
</nav>

{#if mobileOpen}
	<div
		class="mobilePanel"
		role="dialog"
		aria-modal="true"
		tabindex="-1"
		bind:this={panel}
		on:click={closeMenu}
		on:keydown={onMobileKeydown}
	>
		<div class="mobileCard" on:pointerdown|stopPropagation>
			<div class="mobileSection">
				<p class="mobileHeading">Links</p>
				{#each nav as item}
					<a class="mobileLink" href={item.href} on:click={closeMenu}>{item.label}</a>
				{/each}

				<p class="mobileHeading" style="margin-top: 14px;">Apps</p>
				<a class="mobileLink" href="/wordle" on:click={closeMenu}>Wordle Solver</a>

				<p class="mobileHeading" style="margin-top: 14px;">Legacy</p>
				<a class="mobileLink" href="/chat" on:click={closeMenu}>Basic Chat</a>
				<a class="mobileLink" href="/chat3" on:click={closeMenu}>Old Translator</a>
				<a class="mobileLink" href="/chat4" on:click={closeMenu}>SQL Demo</a>
				<a class="mobileLink" href="/chatapp" on:click={closeMenu}>Legacy General Chat</a>
			</div>

			<div class="mobileSection">
				<p class="mobileHeading">Social</p>
				{#each socials as s}
					<a class="mobileLink" href={s.href} target="_blank" rel="noopener noreferrer">
						{s.label}
					</a>
				{/each}
				<a
					class="mobileLink"
					href="http://earlmcgowen.info/"
					target="_blank"
					rel="noopener noreferrer"
				>
					Legacy Site
				</a>
			</div>

			<button type="button" class="closeBtn" on:click={closeMenu}>Close</button>
		</div>
	</div>
{/if}

<style>
	.header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 16px;
		padding: 24px 20px 8px;
	}

	.brand {
		display: flex;
		align-items: center;
		gap: 14px;
		min-width: 0;
	}

	.logo {
		height: 52px;
		width: 52px;
		border-radius: 12px;
		object-fit: cover;
		box-shadow: var(--shadow-sm);
		border: 1px solid var(--border);
		background: var(--surface);
	}

	.titleBlock {
		min-width: 0;
	}

	.title {
		margin: 0;
		font-size: 44px;
		letter-spacing: -0.02em;
		line-height: 1;
	}

	.accent {
		color: var(--brand);
	}

	.subtitle {
		margin: 6px 0 0;
		color: var(--muted);
		font-size: 16px;
	}

	.right {
		display: flex;
		align-items: center;
		gap: 12px;
	}

	.socials {
		display: flex;
		gap: 10px;
	}

	.socialLink {
		font-size: 14px;
		color: var(--muted);
		padding: 6px 8px;
		border-radius: 10px;
	}

	.socialLink:hover {
		background: rgba(255, 79, 163, 0.1);
		color: var(--text);
		text-decoration: none;
	}

	.hamburger {
		display: none;
		border: 1px solid var(--border);
		background: rgba(255, 255, 255, 0.92);
		border-radius: 12px;
		padding: 8px 10px;
		font-size: 18px;
		cursor: pointer;
		box-shadow: var(--shadow-sm);
	}

	.nav {
		margin: 8px 20px 0;
		background: rgba(255, 255, 255, 0.92);
		border: 1px solid var(--border);
		border-radius: var(--radius);
		box-shadow: var(--shadow-sm);
	}

	.navList {
		list-style: none;
		margin: 0;
		padding: 12px 14px;
		display: flex;
		gap: 14px;
		flex-wrap: wrap;
		align-items: center;
	}

	.navLink {
		color: var(--text);
		font-size: 14px;
		padding: 8px 10px;
		border-radius: 10px;
		display: inline-block;
	}

	.navLink:hover {
		background: rgba(255, 79, 163, 0.12);
		text-decoration: none;
	}

	/* Mobile */
	@media (max-width: 980px) {
		.socials {
			display: none;
		}
		.hamburger {
			display: inline-flex;
			align-items: center;
			justify-content: center;
		}
	}

	.mobilePanel {
		position: fixed;
		inset: 0;
		background: rgba(0, 0, 0, 0.35);
		display: flex;
		align-items: flex-start;
		justify-content: center;
		padding: 80px 16px 16px;
		z-index: 9999;
	}

	.mobileCard {
		width: min(520px, 100%);
		background: rgba(255, 255, 255, 0.96);
		border-radius: 18px;
		box-shadow: var(--shadow);
		border: 1px solid var(--border);
		padding: 16px;
	}

	.mobileSection {
		margin-bottom: 14px;
	}

	.mobileHeading {
		margin: 0 0 10px;
		font-weight: 700;
		color: var(--text);
	}

	.mobileLink {
		display: block;
		padding: 10px 10px;
		border-radius: 12px;
		color: var(--text);
	}

	.mobileLink:hover {
		background: rgba(255, 79, 163, 0.1);
		text-decoration: none;
	}

	.closeBtn {
		width: 100%;
		border: 1px solid var(--border);
		background: rgba(255, 255, 255, 0.92);
		border-radius: 12px;
		padding: 10px 12px;
		cursor: pointer;
	}

	.closeBtn:hover {
		background: rgba(255, 79, 163, 0.1);
	}
</style>
