<script lang="ts">
	import LandingHeader from "$lib/components/landing/LandingHeader.svelte";
	import Hero from "$lib/components/landing/Hero.svelte";
	import StepsBand from "$lib/components/landing/StepsBand.svelte";
	import Features from "$lib/components/landing/Features.svelte";
	import Universities from "$lib/components/landing/Universities.svelte";
	import WhySection from "$lib/components/landing/WhySection.svelte";
	import ContactBanner from "$lib/components/landing/ContactBanner.svelte";
	import LandingFooter from "$lib/components/landing/LandingFooter.svelte";
</script>

<svelte:head>
	<title>ApplyCM · One application for every university in Cameroon</title>
	<meta
		name="description"
		content="ApplyCM helps Cameroonian students discover what to study with an AI Career Guide, find universities within their budget, and apply to all of them with one profile."
	/>
	<link
		href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&display=swap"
		rel="stylesheet"
	/>
</svelte:head>

<div class="landing">
	<a href="#main" class="skip-link">Skip to content</a>
	<LandingHeader />
	<main id="main">
		<Hero />
		<StepsBand />
		<Features />
		<Universities />
		<WhySection />
		<ContactBanner />
	</main>
	<LandingFooter />
</div>

<style>
	.landing {
		--blue: #0b6dbd;
		--blue-700: #045c9a;
		--blue-800: #004475;
		--blue-900: #002742;
		--cyan: #40c5eb;
		--lime: #b6d961;
		--purple: #916cc6;
		--grey-100: #f3f5f7;
		--footer: #2f3a45;
		--text: #212529;
		--text-soft: #4f5b66;
		--max-width: 1200px;

		font-family: "Figtree", var(--font-body), system-ui, sans-serif;
		color: var(--text);
		background: #fff;
		overflow-x: clip;
	}

	.landing :global(section[id]) {
		scroll-margin-top: 4.5rem;
	}

	.landing :global(:is(a, button):focus-visible) {
		outline: 3px solid var(--cyan);
		outline-offset: 3px;
		border-radius: 6px;
	}

	.landing :global(.pill) {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		padding: 0.85rem 1.6rem;
		border-radius: 999px;
		border: 2px solid transparent;
		font-weight: 700;
		font-size: 1rem;
		text-decoration: none;
		white-space: nowrap;
		transition:
			transform 0.3s ease,
			box-shadow 0.3s ease,
			background-color 0.3s ease,
			color 0.3s ease;
	}
	.landing :global(.pill:hover) {
		transform: translateY(-2px);
	}
	.landing :global(.pill-dark) {
		background: #111;
		color: #fff;
	}
	.landing :global(.pill-dark:hover) {
		background: var(--blue-900);
		box-shadow: 0 10px 22px rgba(0, 39, 66, 0.25);
	}
	.landing :global(.pill-light) {
		background: #fff;
		color: var(--blue-900);
	}
	.landing :global(.pill-light:hover) {
		box-shadow: 0 10px 24px rgba(0, 0, 0, 0.25);
	}
	.landing :global(.pill-outline) {
		border-color: rgba(255, 255, 255, 0.7);
		color: #fff;
	}
	.landing :global(.pill-outline:hover) {
		background: rgba(255, 255, 255, 0.12);
		border-color: #fff;
	}

	/* Uses `translate` (not `transform`) so cards keep their own transform-based hover lifts. */
	.landing :global(.reveal) {
		opacity: 0;
		translate: 0 28px;
		transition:
			opacity 0.7s ease var(--reveal-delay, 0ms),
			translate 0.7s cubic-bezier(0.22, 1, 0.36, 1) var(--reveal-delay, 0ms),
			transform 0.3s ease,
			box-shadow 0.3s ease;
	}
	.landing :global(.reveal.is-visible) {
		opacity: 1;
		translate: none;
	}

	.landing :global(.sr-only) {
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

	.skip-link {
		position: absolute;
		left: 1rem;
		top: -3rem;
		z-index: 100;
		padding: 0.6rem 1rem;
		border-radius: 8px;
		background: var(--blue-900);
		color: #fff;
		font-weight: 700;
		text-decoration: none;
		transition: top 0.2s ease;
	}
	.skip-link:focus {
		top: 1rem;
	}

	@media (prefers-reduced-motion: reduce) {
		.landing :global(.pill) {
			transition: none;
		}
		.landing :global(.pill:hover) {
			transform: none;
		}
	}
</style>
