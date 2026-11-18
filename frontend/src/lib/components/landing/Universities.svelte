<script lang="ts">
	import { reveal } from "$lib/attachments/reveal";
	import { stats, universities } from "./content";
</script>

<section id="universities" class="universities" aria-labelledby="uni-title">
	<div class="inner">
		<header class="head" {@attach reveal()}>
			<p class="kicker">Partner universities</p>
			<h2 id="uni-title">Apply to universities in Yaoundé today</h2>
			<p class="sub">We're starting with these institutions and adding more schools across Cameroon.</p>
		</header>

		<ul class="schools">
			{#each universities as uni, i (uni.name)}
				<li class="school" {@attach reveal(i * 90)}>
					<span class="mono" aria-hidden="true">{uni.short}</span>
					<span class="name">{uni.name}</span>
					<span class="loc">{uni.location}</span>
				</li>
			{/each}
		</ul>

		<dl class="stats">
			{#each stats as stat, i (stat.label)}
				<div class="stat" {@attach reveal(i * 90)}>
					<dt>{stat.label}</dt>
					<dd>{stat.value}</dd>
				</div>
			{/each}
		</dl>
	</div>
</section>

<style>
	.universities {
		background: var(--grey-100);
	}
	.inner {
		max-width: var(--max-width);
		margin: 0 auto;
		padding: 6rem 1.5rem;
	}
	.head {
		text-align: center;
		max-width: 40rem;
		margin: 0 auto 3rem;
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
		margin: 0 0 0.75rem;
		font-size: clamp(2rem, 3.6vw, 2.75rem);
		line-height: 1.12;
		font-weight: 800;
		letter-spacing: -0.03em;
		color: var(--blue-900);
	}
	.sub {
		margin: 0;
		color: var(--text-soft);
		font-size: 1.05rem;
		line-height: 1.6;
	}
	.schools {
		list-style: none;
		margin: 0 0 4rem;
		padding: 0;
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		gap: 1.25rem;
	}
	.school {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: 0.35rem;
		padding: 1.5rem;
		background: #fff;
		border-radius: 18px;
		box-shadow: 0 1px 2px rgba(0, 39, 66, 0.06);
		transition: transform 0.3s ease, box-shadow 0.3s ease;
	}
	.school:hover {
		transform: translateY(-4px);
		box-shadow: 0 16px 32px rgba(0, 68, 117, 0.12);
	}
	.mono {
		display: inline-grid;
		place-items: center;
		min-width: 3.25rem;
		height: 3.25rem;
		padding: 0 0.6rem;
		margin-bottom: 0.75rem;
		border-radius: 14px;
		font-weight: 800;
		font-size: 0.95rem;
		color: #fff;
		background: linear-gradient(135deg, var(--blue), var(--blue-900));
	}
	.name {
		font-weight: 700;
		color: var(--blue-900);
		line-height: 1.3;
	}
	.loc {
		font-size: 0.9rem;
		color: var(--text-soft);
	}

	.stats {
		margin: 0;
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		border-top: 2px solid rgba(0, 39, 66, 0.12);
	}
	.stat {
		display: flex;
		flex-direction: column-reverse;
		justify-content: flex-end;
		padding: 2rem 1.5rem 0;
		text-align: center;
	}
	.stat + .stat {
		border-left: 2px solid rgba(0, 39, 66, 0.12);
	}
	dd {
		margin: 0 0 0.4rem;
		font-size: clamp(2.25rem, 4vw, 3.25rem);
		font-weight: 800;
		letter-spacing: -0.03em;
		color: var(--blue);
	}
	dt {
		color: var(--text-soft);
		font-weight: 500;
	}

	@media (max-width: 960px) {
		.schools,
		.stats {
			grid-template-columns: repeat(2, 1fr);
		}
		.stat:nth-child(3) {
			border-left: 0;
		}
	}
	@media (max-width: 520px) {
		.schools {
			grid-template-columns: 1fr;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.school {
			transition: none;
		}
		.school:hover {
			transform: none;
		}
	}
</style>
