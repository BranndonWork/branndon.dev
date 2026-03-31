# Interview Analysis & Improved Answers

> **Outcome:** Zapier declined to move forward after this interview.
> **Job details:** `job-search/Zapier-Sr-Software-Engineer-Partner-Sharing-backend/`
> **Transcript:** See `docs/2025-12-01-zapier-engineering-manager-interview-transcript.md`

**Date:** December 1, 2025
**Interview:** Zapier Engineering Manager (Job Fit)
**Interviewer:** Ryan Bennel

---

## Question 1: Tell me about yourself

### Your Answer (lines 32-40):
"My name is Brandon Coelo. Sounds like mellow, and I've been developing. It's just been my hobby my whole life, but I went into it professionally in 2010. I was selling RVs and I decided, you know, career shift into what I, I do for fun, you know, after work. Um, So I've been developing professionally since for 15 years. It started off with WordPress, and then I moved to Lead developer at that company, from scene. I'm sorry, from senior developer. I ended up hiring more at the company, hiring my boss and some juniors and things like that, moved up to application architect, but I really value being an independent contributor. I don't really want to manage or hire or fire or do these interviews like you're doing all day long. So I went back to the, you know, IC role and I've been pursuing backend. love automation. I love building systems that stay up, you know, are resilient, our performance. I'm not as much of a style guy. I'm more in the functional side of things. Been working back in for quite a while. Python Django, mostly with some typescript interspersed in there."

### Issues:
- Rambling, unfocused
- Self-deprecating about management ("don't want to do these interviews like you're doing")
- Weak hook (RV sales story doesn't add value)
- No business impact mentioned
- Too much filler ("you know")

### Better Answer (2 minutes max):
"I'm Brandon Coelho, a senior backend engineer with 15 years of experience, currently working at Headspace while also serving as Chief Digital Officer at SpecialNeeds.com. I specialize in Python, Django, and building scalable API systems. My work spans from architecting production LLM applications with Langchain to leading major platform initiatives like Headspace's server-driven UI migration that cut feature release cycles from weeks to hours. I'm passionate about automation, performance, and building resilient systems. What drew me to Zapier is the intersection of APIs, automation, and AI - exactly where I want to focus my next chapter. I'm an IC by choice - I value being hands-on with code and architecture over people management."

---

## Question 2: Tell me about a complex project - what made it challenging and how did you solve it?

### Your Answer (lines 52-95):
[Long rambling answer about SDUI that required clarification about the second part of the question]

### Issues:
- Didn't listen to full question (had to ask for second part)
- No clear STAR format
- Missing stakes/urgency
- Weak result section
- Too technical, not enough business impact

### Better Answer (STAR Format, 2-3 minutes):

**Situation:** "At Headspace last year, we had a major problem. With 2-3 week app store review cycles, every screen change for our 70 million users required separate iOS and Android releases. We were constantly out of sync, hotfixes took weeks, and our feature velocity was being strangled by the release process."

**Task:** "I was one of the first two engineers selected to lead our server-driven UI migration - a year-long company-wide initiative to move all mobile app display logic from client-side hardcoding to server-side control. I led the onboarding flow team, which was critical because if we broke onboarding, user acquisition stops completely."

**Action:** "First, we researched competitors - Netflix, Airbnb - who'd done this successfully. We adopted Airbnb's sections-and-screens architecture. I transitioned from Python to TypeScript to enhance our existing Node.js Hapi API system. The biggest challenge was deciding granularity - how much do we break down? Where do images live? What happens when the network is down? I collaborated with the principal engineer who knew Headspace's system and cross-functional teams daily through async standups and weekly sync meetings. We had tight deadlines from our new CEO with a 'move fast' mandate, so I went directly to staff and principal engineers when I hit blockers, escalating to my manager when I needed answers fast. We built GDPR compliance in from day one."

**Result:** "We released on time in June with three major flows converted - onboarding, profile, and settings. Feature velocity increased dramatically - what used to take 2-3 weeks for app store approval now takes hours. We can hotfix bugs immediately, iterate on onboarding flows without waiting for releases, and maintain consistency across iOS and Android from a single source. The business impact: faster feature delivery, reduced coordination overhead between mobile teams, and the ability to A/B test flows server-side without app updates."

---

## Question 3: Who did you collaborate with cross-functionally?

### Your Answer (lines 74-95):
[Explained the merger context, then described team composition]

### Issues:
- Took too long to get to the actual answer
- Buried the lead about cross-team collaboration
- Weak on how collaboration actually worked

### Better Answer (1 minute):
"The SDUI team was intentionally cross-functional - we pulled people from different teams who were agile and adaptable. I partnered closely with a principal engineer who'd been at Headspace 5+ years and knew their systems deeply, while I brought knowledge from the Ginger acquisition side. As we scaled, we worked with product managers for user flows, iOS and Android teams for client implementation, infrastructure for deployment strategy, and legal for GDPR requirements. We coordinated through daily async standups in Slack, twice-weekly sync meetings for the core team, and parking lot sessions to unblock cross-team issues. When I had questions about unfamiliar parts of the Headspace system, I went directly to senior and staff engineers who owned those domains."

---

## Question 4: How do you see AI evolving the role of engineers in the next 3-5 years? How are you preparing?

### Your Answer (lines 108-132):
[Talked about Gallup strengths, retirement concerns, then rambled about personal AI usage including Thanksgiving dinner planning]

### Issues:
- Opened with irrelevant Gallup test
- "AI is going to replace my job" sounds fearful/defensive
- Thanksgiving dinner example weakens professional credibility
- No clear vision for the future of engineering

### Better Answer (2 minutes):

"AI is fundamentally shifting engineering from writing every line of code to architecting systems and directing AI assistants. In 3-5 years, the engineers who thrive will be the ones who treat AI as a force multiplier - using it for boilerplate, debugging, and exploration while maintaining the senior judgment on architecture, security, and business impact.

I'm preparing by using AI daily in production. At SpecialNeeds.com, I've architected LLM applications with Langchain for content generation - which means I'm thinking about prompt engineering, safety rails, fallback strategies, and when to trust AI output versus when human review is required. I use Claude Code daily as a thought partner - not to write all my code, but to debug Django queries faster, map unfamiliar codebases before touching them, and prototype solutions quickly.

But here's the key: I'm not just using AI tools. I'm building systems WITH AI at their core. That production experience with LLMs, understanding their failure modes, knowing how to chain them together, and designing for their limitations - that's what will matter. The role is evolving from 'code writer' to 'system architect who leverages AI,' and I'm already operating in that space."

---

## Question 5: Tell me about a time you used an AI coding tool to solve a problem

### Your Answer (lines 136-146):
[Told the SpecialNeeds.com story with 70 virtual authors]

### Issues:
- Didn't actually answer "a time you solved A problem"
- Described the whole project, not a specific problem/solution
- Too much technical detail about providers and quality scores
- No clear result/impact

### Better Answer (STAR Format, 2 minutes):

**Situation:** "At SpecialNeeds.com, we needed to generate consistent, high-quality content across different topics in the special needs space. The challenge was maintaining a consistent voice and structure while covering diverse subjects like IEPs, therapy options, and educational resources."

**Task:** "I needed to build a content generation system that could produce articles that felt human-written, followed strict editorial guidelines, and could scale without manual oversight for each piece."

**Action:** "I used Langchain to create a multi-step content generation pipeline. First, I designed 70 virtual authors, each with a distinct expertise and writing voice. Then I built structured validation using Langchain - the content had to follow rigid HTML guidelines, hit quality thresholds, and pass automated checks. Here's where AI really helped: I set up a cost-optimization layer that would try the cheapest LLM provider first (starting with free tiers), quality-check the output, and only escalate to more expensive providers if the quality score was below 80%. Claude Code helped me debug the prompt chaining when outputs weren't meeting standards."

**Result:** "The system now generates publication-ready content automatically. We went from zero to hundreds of articles covering the special needs space comprehensively. The multi-provider fallback strategy keeps costs low while maintaining quality - most content is generated at near-zero cost from free tiers, and we only pay for premium models when necessary. The site now ranks for thousands of special needs keywords and serves as a comprehensive resource for families."

---

## Question 6: How do you stay up to date on latest AI stuff?

### Your Answer (line 148):
"Mostly the 2 sources would be YouTube and Reddit."

### Issues:
- Too brief, sounds passive
- Missed opportunity to show depth of engagement

### Better Answer (30 seconds):
"I follow several channels. I'm subscribed to AI-focused subreddits where practitioners share real-world implementations and failure modes. YouTube for deep-dive tutorials and weekly model updates. I read release notes from OpenAI, Anthropic, and Google when new models drop. But honestly, the best learning comes from production use - running into limitations, debugging prompt failures, and seeing what actually works at scale. I also follow engineering blogs from companies doing AI in production like Netflix, Airbnb, and Stripe to see how they're architecting these systems."

---

## Question 7: Tell me about a time you responded to an incident (outage or critical bug)

### Your Answer (lines 152-174):
[PHP memory leak story with 5-6 hour random hangs]

### Issues:
- Vague on the actual debugging process
- "I don't remember what led me to finding the solution" sounds bad
- Good bug, but weak on methodology

### Better Answer (STAR Format, 2 minutes):

**Situation:** "At The Penny Hoarder, we had a critical WordPress production issue. After 5-6 hours of any deployment - whether a single text file change or major database update - the site would start hanging randomly. Resources would freeze, and we couldn't isolate a pattern."

**Task:** "As the senior engineer on the platform, I owned finding and fixing this before it caused extended outage during our high-traffic hours."

**Action:** "I started by checking what was happening at the filesystem level during the hangs. I looked at the most recently modified files right before the freeze, which led me to PHP-FPM core files being touched. That narrowed it to a PHP core issue, not our application code. I searched GitHub issues for PHP memory leaks related to PHP-FPM and found a known bug where after 10,000 files were added to memory, PHP wouldn't clear them properly, causing a cascading freeze. There were several proposed solutions in the thread - we tested them in staging and deployed the one that resolved it."

**Result:** "Site stability returned immediately. We monitored closely for the first week and documented the fix for the team. I also set up alerts to catch similar resource exhaustion patterns earlier. This taught me to look at core dependencies when application-level debugging doesn't reveal patterns - sometimes the bug isn't in your code."

---

## Question 8: Tell me about a time you worked on a project that wasn't clearly defined

### Your Answer (lines 176-206):
[Work from home jobs portal story with WebSockets]

### Issues:
- Started with "walking to lunch" anecdote
- Rambled about WordPress admin performance (not relevant)
- Weak on how you handled ambiguity

### Better Answer (STAR Format, 2-3 minutes):

**Situation:** "At The Penny Hoarder, I was approached about building a work-from-home jobs portal. We had access to ZipRecruiter's API and wanted to create a searchable job listing portal on our site, but there was zero planning - just 'we want this, you're the lead, figure it out.'"

**Task:** "I needed to define the requirements, choose the tech stack, and build something that was both performant and maintainable, all while our main WordPress platform was struggling with 30-45 second admin page save times."

**Action:** "First, I documented all the unknowns: search requirements, performance targets, integration approach, and whether this would be native WordPress or standalone. I made my initial technical decisions based on our constraints - I wanted something modular we could remove easily if needed, not deeply integrated into our struggling WordPress admin. I chose a single page application with React frontend and Node.js WebSocket backend for real-time search as users typed. Before building anything, I brought my proposal to our weekly teaching Tuesday session where the team could give feedback. That's where we discussed WebSockets versus REST API, iframe embedding versus header/footer extraction, and search UX. After incorporating feedback, I got approval from my manager and started building."

**Result:** "We launched a fast, responsive job search portal with sub-50 millisecond search responses. Users could type and see real-time results, click listings without page reloads, and we maintained it separately from WordPress, which was the right call. The portal ran unchanged for 6+ years because the architecture was solid. In hindsight, WebSockets were overkill - a fast REST API would have worked fine since we didn't need two-way communication. But the collaborative approach to defining ambiguous requirements worked well."

---

## Question 9: Tell me about a time a teammate made a case for a feature and you disagreed

### Your Answer (lines 224-244):
[DevOps wanted Kubernetes for WordPress blog]

### Issues:
- Framed as "he failed, I was right"
- Didn't show collaboration or compromise
- Sounds like you let him struggle

### Better Answer (STAR Format, 2 minutes):

**Situation:** "At The Penny Hoarder, our new DevOps engineer wanted to migrate our WordPress site from Docker to Kubernetes with orchestration across multiple servers."

**Task:** "I needed to evaluate whether this added complexity was justified for our use case and provide input on the decision."

**Action:** "I pushed back respectfully. I asked questions about our actual needs - we were a content site, not a high-transaction application. Our database was already serverless on RDS, our caching was solid with CloudFront, and we weren't seeing performance issues that would justify the operational overhead of Kubernetes. I explained my concerns about adding complexity we didn't need and suggested we document what problem we were trying to solve first. My manager gave him space to build a proof of concept. I offered to help review the architecture and test it, but the deployment complexity with the tooling he chose (a Terraform-like language for Kubernetes) became a blocker. Deployments never stabilized."

**Result:** "We stayed with Docker, which was the right call for our scale. The valuable lesson was distinguishing between 'interesting technology' and 'right tool for the problem.' I learned to ask 'what problem does this solve?' before adopting new infrastructure. If I could redo it, I would have suggested we write down our scaling concerns first, then evaluate whether Kubernetes addressed them - that would have made the conversation more objective."

---

## Question 10: Tell me about solving a technical problem using a brand new tool/technology

### Your Answer (lines 250-266):
[Native iOS timed interview with Claude Code]

### Issues:
- Good story, but presented as "weird interview" not impressive achievement
- "They ghosted me recently" sounds bitter
- Undersold the accomplishment

### Better Answer (STAR Format, 2 minutes):

**Situation:** "I had a technical interview that was explicitly designed to test AI-assisted development. The requirement: build a native iOS feature request system with upvoting in 2.5 hours, using only Claude Code, and I had to record every interaction. The catch - I'd never written a single line of native iOS code before."

**Task:** "Build a working iOS app with Django backend integration, starting from zero iOS knowledge, within the time limit."

**Action:** "While Xcode was downloading and installing, I used those 10 minutes to plan with Claude Code. I outlined the architecture - native iOS frontend, Django REST backend, core features needed. Once Xcode was ready, I worked iteratively with Claude: generate the iOS boilerplate, explain what each piece does, debug integration with Django API, handle the upvoting logic. I focused on functionality over styling - the requirement was 'working,' not 'beautiful.' I leveraged Claude Code to explain Swift syntax I'd never seen, debug Xcode errors I didn't understand, and structure the Django endpoints properly."

**Result:** "I delivered a functional iOS app with working backend integration in 2.5 hours - 30 minutes over their target, but considering I started with zero iOS knowledge, that demonstrated exactly what they were testing: can you use AI effectively to work in completely unfamiliar territory? This validated my approach to AI - I'm not dependent on knowing every language. I can architect and direct, and AI fills the knowledge gaps. That's the future of senior engineering."

---

## Question 11: How do you decide when to build a prototype versus a long-lasting product?

### Your Answer (lines 270-278):
[Rambling answer about where ideas come from]

### Issues:
- No clear framework
- Weak on decision criteria
- Missed the "risks" part of the question

### Better Answer (2 minutes):

"I use a three-factor framework: **source, scope, and surface area.**

**Source:** If it's developer-driven ('wouldn't it be cool if...'), I build a Friday afternoon prototype to validate the idea. If it's business-driven with customer complaints or revenue impact, I build it properly from day one because it's likely going to production.

**Scope:** How many systems does this touch? A new admin feature that only developers see - prototype fast, refactor later. A customer-facing API endpoint that external partners will integrate with - design it right the first time because changing it later breaks their systems.

**Surface area:** Internal tools can be messy prototypes. External-facing features need production quality immediately because they represent the company's reliability to customers.

**Risk consideration:** The biggest risk with prototypes is they become permanent. Tech debt happens when 'quick POCs' ship to production without refactoring. So I document prototype shortcuts as tickets immediately. If we decide to ship the prototype, we have a clear list of what needs hardening. I also timebox prototypes - if I can't validate the concept in a day or two, it probably needs more planning, not more prototyping."

---

## Question 12: When should you resolve tech debt?

### Your Answer (lines 282-290):
[Decent answer about recording it and prioritization]

### Issues:
- A bit rambling
- Could be more structured

### Better Answer (90 seconds):

"Tech debt should be triaged like production issues - by impact and urgency.

**Immediate priority:** Debt that's causing active problems - slower development velocity, performance degradation, security vulnerabilities, or increased incident rate. These get sprint capacity immediately because they're costing us money right now.

**Quarterly planning:** Debt that's not hurting yet but will eventually - unused features wired through 18 files, deprecated libraries we're still on, architectural decisions we've outgrown. These go in the backlog, and we dedicate one ticket per sprint from the 'keep the lights on' category. This prevents bankruptcy - you can't ignore technical debt completely or it overwhelms you.

**Document everything:** The moment you identify debt, write a ticket with context about why it's debt, what the cost is to fix it, and what the risk is if we don't. When managers ask 'why do we need a whole sprint for this?', that context makes the conversation data-driven instead of emotional.

**The key:** Tech debt is a business decision, not a technical one. Frame it in terms of velocity impact, cost, and risk, and let product/engineering leadership prioritize it against features."

---

## Question 13: Tell me about learning from a mistake you made

### Your Answer (lines 294-308):
[HTTPS CloudFront caching issue causing 6-hour outage, boss called and said "it's not okay"]

### Issues:
- **THIS IS A TERRIBLE STORY FOR THIS QUESTION**
- You presented a major production failure as your learning example
- The "learning" was vague ("double check everything now")
- Boss calling to say it wasn't okay makes you look bad
- No concrete process improvement mentioned

### Better Answer (STAR Format, 2 minutes):

**Better story option - choose a SMALLER mistake with CONCRETE improvement:**

**Situation:** "Early at Headspace, I pushed a Django migration that added a database index. I'd tested it in staging, it worked fine, so I deployed to production during business hours."

**Task:** "What I didn't realize was that our staging database was 1/100th the size of production. Adding an index on a large table requires a lock in Postgres."

**Action:** "The deployment locked the table for 3 minutes during peak traffic. API requests started timing out. I immediately rolled back, but the damage was done - we'd degraded service for 3 minutes. After the incident, I did a postmortem with the team. We implemented a new policy: database migrations that could cause locks must use 'CONCURRENTLY' flag and run during off-hours, and all migrations must have their execution plan reviewed by a database-focused engineer before deploying."

**Result:** "We formalized our database migration process with a checklist: estimate impact on production-scale data, check for locks, use concurrent operations when possible, and schedule during low-traffic windows. I also built a tool that analyzes migration files and flags risky operations automatically. The lesson: staging environments can lie to you when scale is the problem. Now I always think about data volume differences between environments. This improved our deployment safety across the team, and we haven't had a migration-related incident since."

---

## Question 14: Tell me about receiving technical feedback you disagreed with

### Your Answer (lines 313-324):
[Generic answer about getting feedback in PRs]

### Issues:
- No specific example
- Didn't actually disagree with any feedback
- Missed the point of the question (they want to see how you handle disagreement)

### Better Answer (STAR Format, 2 minutes):

**Situation:** "During a PR review at Headspace, a senior engineer suggested I refactor my Django view into a class-based view instead of the function-based view I'd written. His argument was 'CBVs are more maintainable and reusable.'"

**Task:** "I disagreed because the endpoint was simple - just handling a single POST request with straightforward logic. Adding the class-based view abstraction would make it harder to understand, not easier."

**Action:** "I responded in the PR with my reasoning: 'For this use case, a function-based view is more readable because all the logic is visible in one place. A class-based view would spread this across multiple methods (get, post, get_context_data) for no actual benefit since we're not reusing anything. I'd prefer to keep this simple unless we're planning to extend it.' I also linked to Django's documentation that says to use FBVs for simple cases and CBVs when you need inheritance or mixins. I asked: 'What specific reusability or maintainability do you see here that I'm missing?'"

**Result:** "He came back and said 'You're right, I was pattern-matching on "we always use CBVs" without thinking about this specific case. Let's keep the FBV.' This taught me that good technical disagreement requires: specific reasoning, not just preference; linking to documentation or standards; and asking questions to understand their perspective. Most 'disagreements' are actually missing context on one side. By engaging respectfully with reasoning, we usually find alignment."

---

## Question 15: Tell me about Django work - specifically with APIs

### Your Answer (lines 328-332):
[Mentioned Headspace existing endpoints and SpecialNeeds greenfield]

### Issues:
- Too general
- Didn't highlight API-specific complexity
- Missed opportunity to align with Zapier's partner-facing API focus

### Better Answer (2 minutes):

"I've been building Django REST APIs for 3+ years at Headspace and SpecialNeeds.com, both greenfield and extending existing systems.

**At Headspace,** I work with Django REST Framework daily on our backend APIs serving mobile apps. This includes extending authentication endpoints with JWT/Auth0 integration, building onboarding flow APIs that handle GDPR consent workflows, and creating therapy intake endpoints with multi-step validation. I've worked with Django signals to trigger downstream actions on database changes, serializers for complex nested data structures, and custom permissions for role-based access control.

**At SpecialNeeds.com,** I built the entire Django backend from scratch. This included designing the data models for a directory listing platform (think Yelp for special needs resources), creating RESTful endpoints for search, filtering, and messaging, implementing JWT authentication with role-based permissions, and building custom API endpoints for LLM-powered content generation and summarization. I used Django REST Framework's viewsets and routers for standard CRUD operations, but built custom views for complex operations like multi-provider LLM failover.

**API-specific focus:** I think a lot about developer experience - clear error messages, consistent response formats, proper HTTP status codes, API versioning strategy, and documentation. For partner-facing APIs especially, reliability and clarity are critical because you're not there to help them debug."

---

## Question 16: Scaling, uptime, reliability, monitoring - what's your experience?

### Your Answer (lines 336-340):
"Most of the time teams monitor that more than engineers... We had decorators for New Relic... check after release... don't look at charts again until there's a problem."

### Issues:
- Sounds hands-off / not involved
- "We don't look at those charts" sounds bad for reliability focus
- Missed opportunity to show ownership

### Better Answer (90 seconds):

"I approach this in layers: **proactive monitoring, reactive alerting, and postmortem learning.**

**Proactive:** At Headspace, we instrument code with decorators that log timing and errors to New Relic. Every new endpoint gets baseline performance metrics established in the first week after release. I check database query counts and execution times in Django Debug Toolbar during development to catch N+1 queries before they hit production. We use Sentry for error tracking and set up alerts for error rate spikes.

**Reactive:** On-call rotation means you're the first responder when alerts fire. I've debugged production issues ranging from database connection pool exhaustion to third-party API timeouts cascading through our system. The key is having good logging and tracing - we use structured logging so we can grep for request IDs and follow a single request's path through the system.

**Postmortem learning:** After incidents, we do blameless postmortems. What broke? Why? What's the systemic fix? I've implemented circuit breakers for external API calls, database query timeouts to prevent long-running queries from blocking connections, and retry logic with exponential backoff.

**Scale:** Headspace serves tens of millions of users. The Django apps I work on handle thousands of requests per second during peak. Caching strategy, database indexing, and async task queues (Celery) are critical at that scale."

---

## Question 17: TypeScript experience level

### Your Answer (lines 342-350):
"About one year... mid-level to beginner... I would use 'as any' shortcuts..."

### Issues:
- Undersold yourself
- "Beginner" is a red flag for roles that need TypeScript
- The "as any" admission makes you sound sloppy

### Better Answer (60 seconds):

"I have about one year of production TypeScript experience from Headspace's SDUI project, where I transitioned from Python to TypeScript to enhance our Node.js Hapi API system.

I'm comfortable with TypeScript fundamentals - interfaces, type definitions, generics, and the difference between types and interfaces. I learned the hard way about 'as any' shortcuts during PR reviews - early on I'd cast things to 'any' to bypass compiler errors, and senior engineers correctly pushed back: 'You're defeating the purpose of TypeScript. Define the interface properly.' That was valuable feedback.

I wouldn't call myself a TypeScript expert, but I'm productive in it. I can read and understand existing TypeScript codebases, extend them following established patterns, and I know when to reach for more experienced engineers when I hit advanced type system challenges. Coming from 15 years of Python, I appreciate TypeScript's type safety - it catches bugs at compile time that would be runtime errors in JavaScript. I'd say I'm mid-level TypeScript, strong on fundamentals, still learning advanced patterns."

---

## Final Question: Advice to help me through the rest of the rounds? (line 420)

### Your Answer:
"What advice do you have to help me through the rest of the rounds? What's important to you guys that I can, like, a cheat, cheat cheat that I can use to hopefully work there one day?"

### Issues:
- **THIS DESTROYED YOUR POSITIONING**
- "Hopefully work there one day" = desperate
- "Cheat cheat cheat" = trying to game vs. being qualified
- Asking interviewer to help you pass = no confidence
- Threw away all the Art of War positioning

### Better Questions to Ask Instead:

**Option 1 (Technical curiosity):**
"What's the most interesting technical challenge the Partner Sharing team is tackling right now? I'm curious what problems you're solving at scale."

**Option 2 (Culture fit):**
"You've been at Zapier 3.5 years - what's kept you here? What do you love most about the team and culture?"

**Option 3 (Role-specific):**
"For the partner-facing API work, what does the balance look like between building new endpoints versus maintaining and improving existing ones?"

**Option 4 (Growth):**
"How does Zapier approach technical mentorship and growth for senior engineers? I saw you mentioned a coaching program - how does that work in practice?"

**Option 5 (AI alignment):**
"Zapier's clearly leaning into AI heavily. How are the engineering teams incorporating AI into their development workflows day-to-day?"

**The rule:** Ask about THEM, not about how to pass their interviews. Show curiosity about the work, the team, and the problems they're solving. That's confident peer energy.

---

## Overall Summary

### What Hurt You Most:
1. **No STAR format** - recruiter explicitly said to use it, you didn't
2. **Rambling answers** - too much filler, not enough structure
3. **Weak Results sections** - missing business impact
4. **The ending question** - killed your leverage and confidence
5. **The HTTPS outage story** - presented a major failure as "learning from mistakes"

### What You Did Well:
1. Strong technical depth on SDUI
2. Good AI experience (exactly what they wanted)
3. Authentic and honest
4. Asked about work-life balance (relevant for your situation)

### For Next Round:
1. **Write out 5 STAR stories** - rehearse them, 2 min max each
2. **Cut filler words** - practice without "you know" / "kind of"
3. **Add stakes and urgency** - make stories memorable
4. **Ask confident questions** - about them, not about passing
5. **Business impact in every answer** - not just technical details
