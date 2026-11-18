<script lang="ts">
	import { CONTACT_EMAIL, navLinks } from "./content";

	const year = new Date().getFullYear();
</script>

<footer class="site-footer">
	<div class="inner">
		<div class="brand">
			<a href="/" class="logo">Apply<span>CM</span></a>
			<p>One profile for every university in Cameroon, with AI guidance on what to study.</p>
		</div>

		<nav aria-label="Footer">
			<h2>Explore</h2>
			<ul>
				{#each navLinks as link (link.href)}
					<li><a href={link.href}>{link.label}</a></li>
				{/each}
			</ul>
		</nav>

		<div>
			<h2>Get started</h2>
			<ul>
				<li><a href="/signup">Create an account</a></li>
				<li><a href="/login">Log in</a></li>
				<li><a href="mailto:{CONTACT_EMAIL}">Contact us</a></li>
			</ul>
		</div>
	</div>

	<div class="bottom">
		<p>© {year} ApplyCM · Built by students of The ICT University, Yaoundé</p>
	</div>
</footer>

<style>
	.site-footer {
		background: var(--footer);
		color: rgba(255, 255, 255, 0.82);
	}
	.inner {
		max-width: var(--max-width);
		margin: 0 auto;
		padding: 4rem 1.5rem 3rem;
		display: grid;
		grid-template-columns: 2fr 1fr 1fr;
		gap: 2.5rem;
	}
	.logo {
		font-size: 1.6rem;
		font-weight: 800;
		letter-spacing: -0.03em;
		color: #fff;
		text-decoration: none;
	}
	.logo span {
		color: var(--lime);
	}
	.brand p {
		margin: 0.75rem 0 0;
		max-width: 22rem;
		line-height: 1.6;
	}
	h2 {
		margin: 0 0 1rem;
		font-size: 0.85rem;
		font-weight: 700;
		letter-spacing: 0.1em;
		text-transform: uppercase;
		color: #fff;
	}
	ul {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		gap: 0.6rem;
	}
	ul a {
		text-decoration: none;
		transition: color 0.2s ease;
	}
	ul a:hover {
		color: var(--lime);
	}
	.bottom {
		border-top: 1px solid rgba(255, 255, 255, 0.12);
	}
	.bottom p {
		max-width: var(--max-width);
		margin: 0 auto;
		padding: 1.25rem 1.5rem;
		font-size: 0.875rem;
	}

	@media (max-width: 760px) {
		.inner {
			grid-template-columns: 1fr 1fr;
		}
		.brand {
			grid-column: 1 / -1;
		}
	}
</style>
