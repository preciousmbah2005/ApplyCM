<script lang="ts">
	const schools = [
		{ name: "The ICT University", status: "Sent" },
		{ name: "Polytech Yaoundé", status: "Sent" },
		{ name: "MIST", status: "Sent" }
	];
</script>

<section class="hero" aria-labelledby="hero-title">
	<div class="shape shape-a" aria-hidden="true"></div>
	<div class="shape shape-b" aria-hidden="true"></div>

	<div class="inner">
		<div class="copy">
			<p class="eyebrow hero-in" style="--d: 0ms">University admissions for Cameroon</p>
			<h1 id="hero-title" class="hero-in" style="--d: 80ms">
				Your future starts with <span class="underline">one</span> application.
			</h1>
			<p class="lead hero-in" style="--d: 160ms">
				ApplyCM helps students who just finished secondary school discover what to study, find universities
				they can afford, and apply to all of them with a single profile.
			</p>
			<div class="ctas hero-in" style="--d: 240ms">
				<a href="/signup" class="pill pill-light">Create your profile</a>
				<a href="#career-guide" class="pill pill-outline">Explore the Career Guide</a>
			</div>
		</div>

		<div class="visual hero-in" style="--d: 320ms" aria-hidden="true">
			<div class="card profile-card">
				<div class="avatar">AN</div>
				<div>
					<p class="card-title">Application profile</p>
					<p class="card-sub">6 of 6 steps complete</p>
				</div>
				<div class="progress"><span></span></div>
			</div>

			<div class="card ai-card">
				<p class="card-label">AI Career Guide · Top match</p>
				<p class="card-title">Software Engineering</p>
				<div class="meter"><span style="--w: 86%"></span></div>
				<p class="card-sub">Within your budget: 3 universities</p>
			</div>

			<div class="card status-card">
				<p class="card-label">PDF application sent to</p>
				<ul>
					{#each schools as school (school.name)}
						<li>
							<span>{school.name}</span>
							<span class="badge">{school.status}</span>
						</li>
					{/each}
				</ul>
			</div>
		</div>
	</div>
</section>

<style>
	.hero {
		position: relative;
		overflow: hidden;
		color: #fff;
		background:
			radial-gradient(circle at 85% 15%, rgba(64, 197, 235, 0.35), transparent 45%),
			linear-gradient(135deg, var(--blue) 0%, var(--blue-800) 60%, var(--blue-900) 100%);
	}
	.shape {
		position: absolute;
		border-radius: 50%;
		pointer-events: none;
	}
	.shape-a {
		width: 520px;
		height: 520px;
		right: -160px;
		bottom: -260px;
		border: 60px solid rgba(182, 217, 97, 0.18);
	}
	.shape-b {
		width: 220px;
		height: 220px;
		left: -80px;
		top: -90px;
		background: rgba(64, 197, 235, 0.15);
	}
	.inner {
		position: relative;
		max-width: var(--max-width);
		margin: 0 auto;
		padding: 5.5rem 1.5rem 6.5rem;
		display: grid;
		grid-template-columns: 1.15fr 1fr;
		gap: 3.5rem;
		align-items: center;
	}
	.eyebrow {
		display: inline-block;
		margin: 0 0 1.25rem;
		padding: 0.4rem 0.9rem;
		border-radius: 999px;
		background: rgba(255, 255, 255, 0.14);
		font-weight: 600;
		font-size: 0.85rem;
		letter-spacing: 0.02em;
	}
	h1 {
		margin: 0;
		font-size: clamp(2.5rem, 5.4vw, 4.4rem);
		line-height: 1.04;
		font-weight: 800;
		letter-spacing: -0.035em;
	}
	.underline {
		position: relative;
		white-space: nowrap;
	}
	.underline::after {
		content: "";
		position: absolute;
		left: 0;
		right: 0;
		bottom: 0.04em;
		height: 0.16em;
		border-radius: 4px;
		background: var(--lime);
		z-index: -1;
	}
	h1 .underline {
		z-index: 0;
	}
	.lead {
		margin: 1.5rem 0 2.25rem;
		max-width: 36rem;
		font-size: 1.15rem;
		line-height: 1.65;
		color: rgba(255, 255, 255, 0.88);
	}
	.ctas {
		display: flex;
		flex-wrap: wrap;
		gap: 1rem;
	}

	.visual {
		position: relative;
		display: grid;
		gap: 1rem;
		max-width: 420px;
		justify-self: end;
		width: 100%;
	}
	.card {
		background: #fff;
		color: var(--text);
		border-radius: 18px;
		padding: 1.1rem 1.25rem;
		box-shadow: 0 18px 40px rgba(0, 20, 40, 0.28);
		animation: float 6s ease-in-out infinite;
	}
	.ai-card {
		margin-left: 2.5rem;
		animation-delay: -2s;
	}
	.status-card {
		animation-delay: -4s;
	}
	.profile-card {
		display: grid;
		grid-template-columns: auto 1fr;
		gap: 0.25rem 0.9rem;
		align-items: center;
	}
	.avatar {
		width: 2.75rem;
		height: 2.75rem;
		border-radius: 50%;
		display: grid;
		place-items: center;
		font-weight: 700;
		color: var(--blue-900);
		background: var(--lime);
	}
	.progress,
	.meter {
		grid-column: 1 / -1;
		height: 8px;
		border-radius: 999px;
		background: var(--grey-100);
		overflow: hidden;
		margin-top: 0.6rem;
	}
	.progress span,
	.meter span {
		display: block;
		height: 100%;
		width: var(--w);
		border-radius: inherit;
		background: linear-gradient(90deg, var(--lime), var(--cyan));
		transform-origin: left;
		animation: fill 1.6s 0.6s cubic-bezier(0.22, 1, 0.36, 1) both;
	}
	.progress span {
		--w: 100%;
	}
	.card-label {
		margin: 0 0 0.35rem;
		font-size: 0.72rem;
		font-weight: 700;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: var(--blue);
	}
	.card-title {
		margin: 0;
		font-weight: 700;
		font-size: 1.05rem;
		color: var(--blue-900);
	}
	.card-sub {
		margin: 0.15rem 0 0;
		font-size: 0.85rem;
		color: var(--text-soft);
	}
	.meter + .card-sub {
		margin-top: 0.6rem;
	}
	.status-card ul {
		list-style: none;
		margin: 0.5rem 0 0;
		padding: 0;
		display: grid;
		gap: 0.55rem;
	}
	.status-card li {
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 0.92rem;
		font-weight: 500;
	}
	.badge {
		font-size: 0.75rem;
		font-weight: 700;
		padding: 0.2rem 0.6rem;
		border-radius: 999px;
		background: #e8f5d0;
		color: #3d5a0b;
	}

	.hero-in {
		animation: rise 0.8s var(--d, 0ms) cubic-bezier(0.22, 1, 0.36, 1) both;
	}

	@keyframes rise {
		from {
			opacity: 0;
			transform: translateY(24px);
		}
		to {
			opacity: 1;
			transform: none;
		}
	}
	@keyframes float {
		0%,
		100% {
			transform: translateY(0);
		}
		50% {
			transform: translateY(-8px);
		}
	}
	@keyframes fill {
		from {
			transform: scaleX(0);
		}
	}

	@media (max-width: 960px) {
		.inner {
			grid-template-columns: 1fr;
			padding: 3.5rem 1.5rem 4.5rem;
		}
		.visual {
			justify-self: start;
		}
	}
	@media (max-width: 480px) {
		.ai-card {
			margin-left: 0;
		}
	}
	@media (prefers-reduced-motion: reduce) {
		.hero-in,
		.card,
		.progress span,
		.meter span {
			animation: none;
		}
	}
</style>
