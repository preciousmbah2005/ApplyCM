<script lang="ts">
	import { reveal } from "$lib/attachments/reveal";
	import { CONTACT_EMAIL } from "./content";
</script>

<section class="contact" aria-labelledby="contact-title">
	<div class="banner" {@attach reveal()}>
		<div>
			<h2 id="contact-title">Have a question?</h2>
			<p>
				Are you a student, a parent or a university that wants to join ApplyCM? Write to us and our team will get
				back to you.
			</p>
		</div>
		<a href="mailto:{CONTACT_EMAIL}" class="pill pill-dark">Email the team</a>
	</div>
</section>

<style>
	.contact {
		background: #fff;
		padding: 0 1.5rem 6rem;
	}
	.banner {
		max-width: calc(var(--max-width) - 3rem);
		margin: 0 auto;
		padding: 3rem 3.5rem;
		border-radius: 28px;
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 2rem;
		color: var(--blue-900);
		background: linear-gradient(110deg, var(--cyan) 0%, #7fd8f0 45%, var(--lime) 100%);
	}
	h2 {
		margin: 0 0 0.5rem;
		font-size: clamp(1.8rem, 3vw, 2.4rem);
		font-weight: 800;
		letter-spacing: -0.03em;
	}
	p {
		margin: 0;
		max-width: 38rem;
		line-height: 1.6;
		font-size: 1.05rem;
	}
	.pill {
		flex-shrink: 0;
	}

	@media (max-width: 760px) {
		.banner {
			flex-direction: column;
			align-items: flex-start;
			padding: 2.25rem 1.75rem;
		}
	}
</style>
