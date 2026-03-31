# Interview Study Sheet - Perfect Answers

## 1. Tell me about yourself (2 min)

"I'm Branndon Coelho (rhymes with "mello"), a senior software engineer with over 15 years of experience, currently at Headspace. I specialize in Python, Django, and building scalable API systems. My work spans architecting production LLM applications with Langchain to leading Headspace's server-driven UI migration that cut feature release cycles from weeks to hours. I'm passionate about AI, automation, performance, and building resilient systems."

## 2. Complex project - what made it challenging and how did you solve it? (STAR, 2-3 min)

**Situation:** At Headspace, every screen change for 70M users required separate iOS and Android app store releases. Even simple bug fixes took days to deploy through the app review process, and we had to coordinate releases across two platforms.
**Task:** I was one of the first two engineers selected to lead our server-driven UI migration - a year-long initiative to move all mobile app display logic to server-side control. I led the onboarding flow team.
**Action:** We researched Netflix and Airbnb's approaches and adopted Airbnb's sections-and-screens architecture. I transitioned from Python to TypeScript to enhance our Node.js Hapi API. I collaborated daily with cross-functional teams through async standups.
**Result:** We released on time in June. Feature velocity increased dramatically - what took days through app store review now takes hours. We can hotfix bugs immediately, iterate on onboarding without app releases, and maintain iOS/Android consistency from a single source.

## 3. Teammate proposed feature/implementation you disagreed with (STAR, 2 min)

**Situation:** At The Penny Hoarder, our DevOps engineer wanted to migrate our WordPress site from Docker to Kubernetes with orchestration.
**Task:** I needed to evaluate whether the added complexity was justified.
**Action:** I pushed back respectfully. I asked about our actual needs - we were a content site, not a high-transaction app. Our database was serverless on RDS, caching was solid. I explained my concerns about operational overhead. My manager gave him space for a POC. I offered to help review and test, but the deployment complexity became a blocker.
**Result:** In the end, we stayed with Docker - the right call for our scale. I learned to ask 'what problem does this solve?' before adopting new infrastructure. I'd now suggest writing down scaling concerns first, then evaluating if the solution addresses them.

## 4. Learning from a mistake (STAR, 2 min)

**Situation:** At The Penny Hoarder, we were converting our WordPress site to HTTPS when browsers were starting to require it. During one of the releases, there was an intermittent problem where pages would load without any CSS - they'd render, but look completely broken.
**Task:** I was the driver on this conversion, and I needed to figure out why some pages rendered correctly for everyone while other pages were broken for everyone.
**Action:** I traced it to a CloudFront caching issue with how stylesheets were being referenced. When a page didn't have a cache yet, CloudFront would generate one based on whichever device hit it first. Certain iOS versions would generate the cache with http:// stylesheet links, while others generated it with https://. Whichever device hit first determined the cache for everyone. So if a broken iOS version cached a page first, that page would have http:// stylesheet links for everyone - meaning the CSS wouldn't load on any device. I was apologizing profusely in Slack. Most people were supportive, but my boss called me that night and said "I'm here to tell you that it's not okay. That was a big deal."
**Result:** I appreciated his candor and directness. Since then, I double-check everything I do more than ever because I never want to be in that position again. I learned how to handle problems better, how to respond when things go wrong, and the importance of taking feedback seriously and learning from it.

## 5. Project that wasn't clearly defined - how did you make progress? (STAR, 2-3 min)

**Situation:** At The Penny Hoarder, I was approached about building a work-from-home jobs portal using ZipRecruiter's API. Zero planning - just 'we want this, you're the lead.'
**Task:** I needed to define requirements, choose the tech stack, and build something performant and maintainable. Our WordPress admin was struggling with 30-45 second save times.
**Action:** I documented all the unknowns: search requirements, performance targets, integration approach. I made initial technical decisions - I wanted something modular we could remove easily, not deeply integrated into the struggling WordPress system. I chose an SPA with React frontend and Node.js WebSocket backend for real-time search. I brought my proposal to the team's teaching Tuesday session for feedback before building.
**Result:** We launched a fast, responsive portal with sub-50ms search responses. Users got real-time results as they typed, no page reloads. It ran unchanged for 6+ years because the architecture was solid. In hindsight, WebSockets were overkill - a fast REST API would have worked. But the collaborative approach to defining ambiguous requirements worked well.

## 6. Received technical feedback you disagreed with - how did you respond? (STAR, 2 min)

**Situation:** During PR reviews at Headspace, I'd regularly get feedback from other engineers who'd point out areas where I was working in unfamiliar parts of the codebase.
**Task:** I needed to evaluate their feedback and decide how to respond - whether to push back or incorporate their suggestions.
**Action:** My approach was to assume they had context I didn't have. When they'd ask "why are you doing it this way? Did you know about this feature over here?" I'd treat it as knowledge sharing, not criticism. With a 500-engineer, 10-year-old codebase, nobody knows everything. I'd look at what they were pointing to, understand why their approach was better, and incorporate it. If their reasoning wasn't immediately clear, I'd ask questions to understand their perspective rather than defending my initial approach.
**Result:** This helped me learn the codebase faster and build stronger relationships with my peers. I'd take their suggestions and incorporate them into my workflows going forward. I learned that the best engineers don't defend their code - they're open to learning better ways, especially when working in a large system where everyone has different expertise.

## 7. Responding to an incident (STAR, 2 min)

**Situation:** At The Penny Hoarder, our WordPress site would hang randomly after 5-6 hours of any deployment. We couldn't isolate a pattern.
**Task:** As the senior engineer on the platform, I owned finding and fixing this before we had an extended outage.
**Action:** I checked filesystem activity during the hangs. I found PHP-FPM core files being touched right before the freeze. I searched GitHub issues for PHP memory leaks and found a known bug where after 10,000 files were added to memory, PHP wouldn't clear them, causing a cascading freeze. I tested the proposed solutions in staging.
**Result:** Site stability returned immediately. I set up alerts to catch similar resource exhaustion earlier. I learned to look at core dependencies when application-level debugging doesn't reveal patterns.

## 8. Solving technical problem with brand new tool/technology (STAR, 2 min)

**Situation:** I had a technical interview testing AI-assisted development. The requirement: build a native iOS feature request system with upvoting in 2.5 hours using only Claude Code. I'd never written native iOS code before.
**Task:** I needed to build a working iOS app with Django backend integration from zero iOS knowledge.
**Action:** While Xcode was downloading, I planned with Claude Code - outlined the architecture and core features. Once ready, I worked iteratively: generated iOS boilerplate, had it explain each piece, debugged the integration with my Django API, and handled the upvoting logic. I focused on functionality over styling.
**Result:** I delivered a functional iOS app with working backend in 2.5 hours - 30 minutes over target. Starting with zero iOS knowledge, this demonstrated effective AI use for unfamiliar territory. It validated my approach: I'm not dependent on knowing every language. I architect and direct, AI fills the knowledge gaps.

## 9. Django/API work examples (2 min)

"I've built Django REST APIs for 3+ years at Headspace and SpecialNeeds.com. At Headspace, I work with DRF daily on backend APIs serving mobile apps - extending authentication with JWT/Auth0, building onboarding APIs with GDPR consent, therapy intake endpoints with multi-step validation. At SpecialNeeds.com, built entire Django backend from scratch - data models for directory platform, RESTful endpoints for search/filtering/messaging, JWT auth with role-based permissions, custom API endpoints for LLM-powered content generation. I focus on developer experience - clear error messages, consistent response formats, proper HTTP status codes, API versioning, and documentation. For partner-facing APIs, reliability and clarity are critical."

## 10. When to build prototype vs long-lasting product? (2 min)

"I use a three-factor framework: source, scope, and surface area. **Source:** Developer-driven ideas get Friday afternoon prototypes to validate. Business-driven with customer complaints or revenue impact gets built properly from day one. **Scope:** How many systems does this touch? Internal admin features can prototype fast, refactor later. Customer-facing API endpoints need proper design because changing them breaks external integrations. **Surface area:** Internal tools can be messy prototypes. External-facing features need production quality immediately. **Risk:** Prototypes become permanent tech debt. So I document prototype shortcuts as tickets immediately. If we ship the prototype, we have clear list of what needs hardening."

## 11. How do you see AI evolving engineering in 3-5 years? How are you preparing? (2 min)

"AI is shifting engineering from writing every line to architecting systems and directing AI assistants. In 3-5 years, engineers who thrive will treat AI as a force multiplier. I'm preparing by using AI daily in production. At SpecialNeeds.com, I've architected LLM applications with Langchain for content generation - I'm thinking about prompt engineering, safety rails, and when to trust AI versus human review. I use Claude Code daily as a thought partner for debugging Django queries, mapping unfamiliar codebases, and prototyping. The role is evolving from 'code writer' to 'system architect who leverages AI,' and I'm already operating in that space."

## 12. Time you used AI to solve a problem (STAR, 2 min)

**Situation:** At SpecialNeeds.com, we needed to generate consistent, high-quality content across diverse special needs topics while maintaining voice and structure.
**Task:** I needed to build a content generation system that could produce human-quality articles at scale without manual oversight.
**Action:** I used Langchain to create a multi-step pipeline with 70 virtual authors, each with distinct expertise. I built structured validation - content had to follow HTML guidelines and hit quality thresholds. I set up cost-optimization: try the cheapest LLM first, quality-check the output, only escalate to expensive providers if the quality score was below 80%.
**Result:** The system now generates publication-ready content automatically. We went from zero to hundreds of articles. The multi-provider strategy keeps costs near-zero (free tiers handle most content), only paying premium models when necessary. The site now ranks for thousands of keywords.

---

## Questions to Ask Interviewer (Pick 2-3):

1. "What's the most interesting technical challenge your team is tackling right now?"
2. "You've been at [Company] X years - what's kept you here? What do you love most about the team?"
3. "How does [Company] approach technical mentorship and growth for senior engineers?"
4. "For the [specific role] work, what does the balance look like between building new features versus maintaining existing systems?"
5. "How are engineering teams incorporating AI into their development workflows day-to-day?"

---

**Key Reminders:**

-   Use STAR format (Situation → Task → Action → Result)
-   Add stakes and urgency to stories (user impact, timeline pressure, business consequences)
-   Always include quantified business impact in Results
-   Keep answers 2-3 minutes max
-   Pause 2 seconds before answering
-   Cut filler words: "you know," "kind of," "I think"
-   Ask confident questions about THEM, not about passing their interviews
