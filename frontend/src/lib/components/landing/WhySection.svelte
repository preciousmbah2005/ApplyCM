<script lang="ts">
	import { reveal } from "$lib/attachments/reveal";
	import { problems } from "./content";
</script>

<section id="why" class="why" aria-labelledby="why-title">
	<div class="inner">
		<div class="intro" {@attach reveal()}>
			<p class="kicker">Why we built ApplyCM</p>
			<h2 id="why-title">Applying to university in Cameroon shouldn't be this hard</h2>
			<p class="lead">
				We are students at The ICT University. We built ApplyCM to fix the problems we and our classmates faced
				when we left secondary school.
			</p>
		</div>

		<ul class="problems">
			{#each problems as problem, i (problem.title)}
				<li {@attach reveal(i * 110)}>
					<span class="dot" aria-hidden="true">{i + 1}</span>
					<h3>{problem.title}</h3>
					<p>{problem.body}</p>
				</li>
			{/each}
		</ul>
	</div>
</section>

<style>
	.why {
		background: #fff;
	}
	.inner {
		max-width: var(--max-width);
		margin: 0 auto;
		padding: 6rem 1.5rem;
		display: grid;
		grid-template-columns: 1fr 1.1fr;
		gap: 4rem;
		align-items: start;
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
		margin: 0 0 1.25rem;
		font-size: clamp(2rem, 3.6vw, 2.75rem);
		line-height: 1.12;
		font-weight: 800;
		letter-spacing: -0.03em;
		color: var(--blue-900);
	}
	.lead {
		margin: 0;
		font-size: 1.1rem;
		line-height: 1.7;
		color: var(--text-soft);
	}
	.problems {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		gap: 1.25rem;
	}
	.problems li {
		display: grid;
		grid-template-columns: auto 1fr;
		gap: 0.25rem 1.25rem;
		padding: 1.5rem 1.75rem;
		border-radius: 18px;
		background: var(--grey-100);
		transition: transform 0.3s ease;
	}
	.dot {
		grid-row: span 2;
		width: 2.5rem;
		height: 2.5rem;
		border-radius: 50%;
		display: grid;
		place-items: center;
		font-weight: 800;
		color: var(--blue-900);
		background: var(--cyan);
	}
	.problems li:nth-child(2) .dot {
		background: var(--lime);
	}
	.problems li:nth-child(3) .dot {
		background: var(--purple);
		color: #fff;
	}
	.problems li:hover {
		transform: translateY(-3px);
	}
	h3 {
		margin: 0 0 0.4rem;
		font-size: 1.15rem;
		font-weight: 700;
		color: var(--blue-900);
	}
	.problems p {
		margin: 0;
		line-height: 1.6;
		color: var(--text-soft);
	}

	@media (max-width: 960px) {
		.inner {
			grid-template-columns: 1fr;
			gap: 2.5rem;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.problems li {
			transition: none;
		}
		.problems li:hover {
			transform: none;
		}
	}
</style>
