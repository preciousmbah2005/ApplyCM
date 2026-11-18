export const CONTACT_EMAIL = "precious.mbah@ictuniversity.edu.cm";

export const navLinks = [
	{ href: "#how-it-works", label: "How it works" },
	{ href: "#features", label: "Features" },
	{ href: "#career-guide", label: "Career Guide" },
	{ href: "#universities", label: "Universities" }
] as const;

export const steps = [
	{
		number: "1",
		title: "Find your path",
		body: "Not sure what to study? Take the AI Career Guide questionnaire and get the fields of study that fit you best."
	},
	{
		number: "2",
		title: "Build one profile",
		body: "Fill in your personal details, contacts, O/A-Level results, activities and personal statement once."
	},
	{
		number: "3",
		title: "Choose your schools",
		body: "Search universities by name, city, degree or field, compare tuition, and save the ones you like."
	},
	{
		number: "4",
		title: "Apply in one click",
		body: "Your profile is turned into a PDF and emailed to every school you picked. Track each one as it goes out."
	}
] as const;

export const features = [
	{
		id: "career-guide",
		eyebrow: "AI Career Guide",
		title: "Know what to study before you apply",
		body: "Just finished high school and unsure of your next step? Answer a short questionnaire about your subjects, interests and budget. Our model, trained by the ApplyCM team, suggests the fields of study that suit you and the universities that offer them within what you can afford.",
		points: ["Top fields of study ranked for you", "Schools filtered by your budget", "Built and trained from scratch by our team"]
	},
	{
		id: "profile",
		eyebrow: "One application profile",
		title: "Type it once, use it everywhere",
		body: "A guided six-step form covers your profile, contact details, education with result slips, testing, activities and writing. Your progress is saved as you go.",
		points: ["Six guided steps", "Saved automatically", "Reused for every school"]
	},
	{
		id: "submit",
		eyebrow: "One-click submission",
		title: "Your application, delivered as a PDF",
		body: "When you're ready, ApplyCM generates a clean PDF of your profile and emails it straight to the admissions office of each university you chose. You get a copy too.",
		points: ["Sent to all your favorites at once", "A copy lands in your inbox", "No printing, no queues"]
	},
	{
		id: "tracking",
		eyebrow: "Status tracking",
		title: "See where every application stands",
		body: "Each school gets its own status, so you always know which applications went out and which need another try.",
		points: ["Per-school Sent / Failed status", "Resend any that failed", "Everything in one place"]
	}
] as const;

export const universities = [
	{ name: "The ICT University", short: "ICTU", location: "Messassi, Yaoundé" },
	{ name: "National Advanced School of Engineering", short: "Polytech", location: "Melen, Yaoundé" },
	{ name: "IUSTY", short: "IUSTY", location: "Soa, Yaoundé" },
	{ name: "MIST", short: "MIST", location: "Messassi, Yaoundé" }
] as const;

export const stats = [
	{ value: "4", label: "Partner universities" },
	{ value: "12", label: "Programs to explore" },
	{ value: "50,000", label: "FCFA / year, lowest tuition listed" },
	{ value: "1", label: "Profile for all of them" }
] as const;

export const problems = [
	{
		title: "Every school, a new form",
		body: "Students fill in the same details again and again, on paper or on different websites, for each university."
	},
	{
		title: "Travel and queues",
		body: "Applying often means travelling to each campus, paying for copies and waiting in line just to submit a file."
	},
	{
		title: "Choosing without guidance",
		body: "Many students leave high school with no clear idea of which field suits them or which schools they can afford."
	}
] as const;
