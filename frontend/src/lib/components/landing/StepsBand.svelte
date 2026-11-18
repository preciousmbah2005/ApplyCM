<script lang="ts">
	import { reveal } from "$lib/attachments/reveal";
	import { steps } from "./content";
</script>

<section id="how-it-works" class="steps-band" aria-labelledby="steps-title">
	<div class="inner">
		<header class="head" {@attach reveal()}>
			<h2 id="steps-title">How ApplyCM works</h2>
			<p>From "what should I study?" to "application sent" in four steps.</p>
		</header>

		<ol class="steps">
			{#each steps as step, i (step.number)}
				<li {@attach reveal(i * 100)}>
					<span class="num" aria-hidden="true">{step.number}</span>
					<h3>{step.title}</h3>
					<p>{step.body}</p>
				</li>
			{/each}
		</ol>
	</div>
</section>

<style>
	.steps-band {
		background: var(--lime);
		color: var(--blue-900);
	}
	.inner {
		max-width: var(--max-width);
		margin: 0 auto;
		padding: 5rem 1.5rem;
	}
	.head {
		max-width: 40rem;
		margin-bottom: 3rem;
	}
	h2 {
		margin: 0 0 0.75rem;
		font-size: clamp(2rem, 3.6vw, 2.75rem);
		font-weight: 800;
		letter-spacing: -0.03em;
	}
	.head p {
		margin: 0;
		font-size: 1.1rem;
		line-height: 1.6;
	}
	.steps {
		list-style: none;
		margin: 0;
		padding: 0;
		display: grid;
		grid-template-columns: repeat(4, 1fr);
	}
	.steps li {
		padding: 0 1.75rem;
		border-left: 2px solid rgba(0, 39, 66, 0.25);
	}
	.steps li:first-child {
		padding-left: 0;
		border-left: 0;
	}
	.num {
		display: block;
		font-size: 4rem;
		font-weight: 800;
		line-height: 1;
		margin-bottom: 1rem;
		letter-spacing: -0.04em;
	}
	h3 {
		margin: 0 0 0.5rem;
		font-size: 1.2rem;
		font-weight: 700;
	}
	.steps p {
		margin: 0;
		line-height: 1.6;
		font-size: 0.98rem;
	}

	@media (max-width: 960px) {
		.steps {
			grid-template-columns: repeat(2, 1fr);
			row-gap: 2.5rem;
		}
		.steps li:nth-child(3) {
			padding-left: 0;
			border-left: 0;
		}
	}
	@media (max-width: 560px) {
		.steps {
			grid-template-columns: 1fr;
		}
		.steps li {
			padding: 0 0 2rem;
			border-left: 0;
			border-bottom: 2px solid rgba(0, 39, 66, 0.25);
		}
		.steps li:last-child {
			border-bottom: 0;
			padding-bottom: 0;
		}
	}
</style>
