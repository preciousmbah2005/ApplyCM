<script lang="ts">
	import { reveal } from "$lib/attachments/reveal";
	import { features } from "./content";

	const [guide, ...rest] = features;
</script>

<section id="features" class="features" aria-labelledby="features-title">
	<div class="inner">
		<header class="head" {@attach reveal()}>
			<p class="kicker">What you get</p>
			<h2 id="features-title">Everything you need to go from secondary school to university</h2>
		</header>

		<article id={guide.id} class="guide gradient-border" {@attach reveal()}>
			<div class="guide-copy">
				<p class="eyebrow">{guide.eyebrow}</p>
				<h3>{guide.title}</h3>
				<p class="body">{guide.body}</p>
				<ul class="points">
					{#each guide.points as point (point)}
						<li>{point}</li>
					{/each}
				</ul>
				<a href="/signup" class="pill pill-dark">Take the questionnaire</a>
			</div>

			<div class="guide-visual" aria-hidden="true">
				<p class="vis-label">Your top fields</p>
				{#each [{ f: "Software Engineering", p: 86 }, { f: "Cybersecurity", p: 71 }, { f: "Telecommunications", p: 58 }] as row (row.f)}
					<div class="row">
						<span>{row.f}</span>
						<span class="pct">{row.p}%</span>
						<div class="bar"><span style="--w: {row.p}%"></span></div>
					</div>
				{/each}
				<p class="vis-foot">Budget: up to 600,000 FCFA / year</p>
			</div>
		</article>

		<div class="grid">
			{#each rest as feature, i (feature.id)}
				<article id={feature.id} class="card gradient-border" {@attach reveal(i * 120)}>
					<p class="eyebrow">{feature.eyebrow}</p>
					<h3>{feature.title}</h3>
					<p class="body">{feature.body}</p>
					<ul class="points">
						{#each feature.points as point (point)}
							<li>{point}</li>
						{/each}
					</ul>
				</article>
			{/each}
		</div>
	</div>
</section>

<style>
	.features {
		background: #fff;
	}
	.inner {
		max-width: var(--max-width);
		margin: 0 auto;
		padding: 6rem 1.5rem;
	}
	.head {
		max-width: 46rem;
		margin-bottom: 3rem;
	}
	.kicker {
		margin: 0 0 0.75rem;
		font-weight: 700;
		font-size: 0.85rem;
		letter-spacing: 0.1em;
		text-transform: uppercase;
		color: var(--blue);
	}
	h2 {
		margin: 0;
		font-size: clamp(2rem, 3.6vw, 2.75rem);
		line-height: 1.12;
		font-weight: 800;
		letter-spacing: -0.03em;
		color: var(--blue-900);
	}
	.gradient-border {
		position: relative;
		border: 3px solid transparent;
		border-radius: 22px;
		background:
			linear-gradient(#fff, #fff) padding-box,
			linear-gradient(120deg, var(--lime), var(--cyan)) border-box;
		transition: transform 0.3s ease, box-shadow 0.3s ease;
	}
	.gradient-border:hover {
		transform: translateY(-4px);
		box-shadow: 0 18px 40px rgba(0, 68, 117, 0.12);
	}
	.guide {
		display: grid;
		grid-template-columns: 1.2fr 1fr;
		gap: 3rem;
		padding: 2.75rem;
		margin-bottom: 2rem;
		scroll-margin-top: 6rem;
	}
	.eyebrow {
		margin: 0 0 0.6rem;
		font-weight: 700;
		color: var(--blue);
	}
	h3 {
		margin: 0 0 0.85rem;
		font-size: 1.55rem;
		line-height: 1.2;
		font-weight: 800;
		letter-spacing: -0.02em;
		color: var(--blue-900);
	}
	.guide h3 {
		font-size: clamp(1.7rem, 2.8vw, 2.2rem);
	}
	.body {
		margin: 0 0 1.25rem;
		line-height: 1.7;
		color: var(--text-soft);
	}
	.points {
		list-style: none;
		margin: 0 0 1.75rem;
		padding: 0;
		display: grid;
		gap: 0.55rem;
	}
	.points li {
		position: relative;
		padding-left: 1.75rem;
		font-weight: 500;
		color: var(--text);
	}
	.points li::before {
		content: "";
		position: absolute;
		left: 0;
		top: 0.2em;
		width: 1.1rem;
		height: 1.1rem;
		border-radius: 50%;
		background: var(--lime) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M4 8.5l2.5 2.5L12 5.5' fill='none' stroke='%23002742' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / 70% no-repeat;
	}
	.card .points {
		margin-bottom: 0;
	}

	.guide-visual {
		align-self: center;
		background: linear-gradient(160deg, var(--blue-800), var(--blue-900));
		color: #fff;
		border-radius: 18px;
		padding: 1.75rem;
	}
	.vis-label {
		margin: 0 0 1.25rem;
		font-size: 0.75rem;
		font-weight: 700;
		letter-spacing: 0.1em;
		text-transform: uppercase;
		color: var(--cyan);
	}
	.row {
		display: grid;
		grid-template-columns: 1fr auto;
		gap: 0.4rem;
		margin-bottom: 1.1rem;
		font-weight: 600;
	}
	.pct {
		color: var(--lime);
	}
	.bar {
		grid-column: 1 / -1;
		height: 10px;
		border-radius: 999px;
		background: rgba(255, 255, 255, 0.12);
		overflow: hidden;
	}
	.bar span {
		display: block;
		height: 100%;
		width: var(--w);
		border-radius: inherit;
		background: linear-gradient(90deg, var(--lime), var(--cyan));
		transform: scaleX(0);
		transform-origin: left;
		transition: transform 1.2s 0.3s cubic-bezier(0.22, 1, 0.36, 1);
	}
	:global(.is-visible) .bar span {
		transform: scaleX(1);
	}
	.vis-foot {
		margin: 1.5rem 0 0;
		padding-top: 1rem;
		border-top: 1px solid rgba(255, 255, 255, 0.15);
		font-size: 0.9rem;
		color: rgba(255, 255, 255, 0.8);
	}

	.grid {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 2rem;
	}
	.card {
		padding: 2rem;
		scroll-margin-top: 6rem;
	}

	@media (max-width: 960px) {
		.guide {
			grid-template-columns: 1fr;
			padding: 2rem;
		}
		.grid {
			grid-template-columns: 1fr;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.gradient-border,
		.bar span {
			transition: none;
		}
		.gradient-border:hover {
			transform: none;
		}
	}
</style>
