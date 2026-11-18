import type { Attachment } from "svelte/attachments";

/**
 * Fades an element up into view the first time it scrolls into the viewport.
 * Content stays visible without JavaScript and for users who prefer reduced motion.
 * Pair with the `.reveal` / `.is-visible` styles defined on the landing page.
 */
export function reveal(delayMs = 0): Attachment<HTMLElement> {
	return (node) => {
		const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
		if (reduceMotion || typeof IntersectionObserver === "undefined") {
			node.classList.add("is-visible");
			return;
		}

		node.style.setProperty("--reveal-delay", `${delayMs}ms`);
		node.classList.add("reveal");

		const observer = new IntersectionObserver(
			(entries) => {
				if (entries.some((entry) => entry.isIntersecting)) {
					node.classList.add("is-visible");
					observer.disconnect();
				}
			},
			{ threshold: 0.15, rootMargin: "0px 0px -40px 0px" }
		);
		observer.observe(node);

		return () => observer.disconnect();
	};
}
