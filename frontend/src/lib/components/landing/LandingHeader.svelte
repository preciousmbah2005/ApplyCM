<script lang="ts">
	import { navLinks } from "./content";

	let scrolled = $state(false);
	let menuOpen = $state(false);

	function closeMenu() {
		menuOpen = false;
	}
</script>

<svelte:window onscroll={() => (scrolled = window.scrollY > 12)} />

<header class="site-header" class:scrolled>
	<div class="inner">
		<a href="/" class="logo" aria-label="ApplyCM home">Apply<span>CM</span></a>

		<button
			class="menu-toggle"
			aria-expanded={menuOpen}
			aria-controls="landing-nav"
			onclick={() => (menuOpen = !menuOpen)}
		>
			<span class="sr-only">{menuOpen ? "Close menu" : "Open menu"}</span>
			<svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">
				{#if menuOpen}
					<path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
				{:else}
					<path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
				{/if}
			</svg>
		</button>

		<nav id="landing-nav" class="site-nav" class:open={menuOpen} aria-label="Main">
			<ul class="links">
				{#each navLinks as link (link.href)}
					<li><a href={link.href} onclick={closeMenu}>{link.label}</a></li>
				{/each}
			</ul>
			<div class="actions">
				<a href="/login" class="login">Log in</a>
				<a href="/signup" class="pill pill-dark">Create your profile</a>
			</div>
		</nav>
	</div>
</header>

<style>
	.site-header {
		position: sticky;
		top: 0;
		z-index: 50;
		background: #fff;
		transition: box-shadow 0.3s ease;
	}
	.site-header.scrolled {
		box-shadow: 0 2px 18px rgba(0, 39, 66, 0.12);
	}
	.inner {
		max-width: var(--max-width);
		margin: 0 auto;
		height: 4.5rem;
		padding: 0 1.5rem;
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1.5rem;
	}
	.logo {
		font-size: 1.6rem;
		font-weight: 800;
		letter-spacing: -0.03em;
		color: var(--blue-900);
		text-decoration: none;
	}
	.logo span {
		color: var(--blue);
	}
	.site-nav {
		display: flex;
		align-items: center;
		gap: 2rem;
	}
	.links {
		display: flex;
		gap: 1.75rem;
		list-style: none;
		margin: 0;
		padding: 0;
	}
	.links a,
	.login {
		font-weight: 600;
		font-size: 0.95rem;
		color: var(--text);
		text-decoration: none;
		background-image: linear-gradient(var(--blue), var(--blue));
		background-size: 0 2px;
		background-position: 0 100%;
		background-repeat: no-repeat;
		padding-bottom: 2px;
		transition: background-size 0.3s ease, color 0.3s ease;
	}
	.links a:hover,
	.login:hover {
		color: var(--blue);
		background-size: 100% 2px;
	}
	.actions {
		display: flex;
		align-items: center;
		gap: 1.25rem;
	}
	.menu-toggle {
		display: none;
		background: none;
		border: 0;
		padding: 0.5rem;
		color: var(--blue-900);
		cursor: pointer;
		border-radius: 8px;
	}

	@media (max-width: 960px) {
		.menu-toggle {
			display: inline-flex;
		}
		.site-nav {
			position: absolute;
			top: 4.5rem;
			left: 0;
			right: 0;
			flex-direction: column;
			align-items: stretch;
			gap: 1rem;
			padding: 1.25rem 1.5rem 1.75rem;
			background: #fff;
			box-shadow: 0 12px 24px rgba(0, 39, 66, 0.12);
			display: none;
		}
		.site-nav.open {
			display: flex;
		}
		.links {
			flex-direction: column;
			gap: 0.9rem;
		}
		.actions {
			justify-content: space-between;
		}
	}
</style>
