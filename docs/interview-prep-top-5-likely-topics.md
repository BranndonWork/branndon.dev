# Top 5 Most Likely Interview Topics - Quick Reference

**For:** Today's technical interviews
**Focus:** Backend engineering roles (Python/Django/APIs)

---

## 1. Tell me about yourself (2 min) - ALWAYS COMES UP

"I'm Branndon Coelho (rhymes with "mello"), a senior software engineer with over 15 years of experience, currently at Headspace. I specialize in Python, Django, and building scalable API systems. My work spans architecting production LLM applications with Langchain to leading Headspace's server-driven UI migration that cut feature release cycles from days to hours. I'm passionate about AI, automation, performance, and building resilient systems."

**Key points:**
- Name pronunciation upfront
- 15 years experience
- Current role: Headspace
- Core skills: Python, Django, APIs
- Two impressive achievements: LLM apps, SDUI migration
- What drives you: AI, automation, performance, resilient systems

---

## 2. System Design/Architecture Question - HIGHLY LIKELY

**Example:** "How would you architect a movie goers app?"

### Framework to Use:

**Step 1: Clarify Requirements (3-5 min)**
- Who are the users? (consumers, admins, theater partners?)
- What are the core features? (search movies, book tickets, reviews, recommendations?)
- What's the scale? (how many users, requests/second, data volume?)
- What are the constraints? (latency requirements, budget, existing systems?)

**Step 2: High-Level Architecture (5 min)**
- Frontend: Web app (React/Next.js), Mobile apps (iOS/Android)
- API Layer: Django REST Framework or Node.js (depending on real-time needs)
- Database:
  - PostgreSQL for relational data (users, bookings, theaters)
  - Redis for caching (movie listings, user sessions)
  - Elasticsearch for search (movie titles, actors, genres)
- External integrations: Theater APIs, payment processing (Stripe)
- CDN: CloudFront for static assets (movie posters, trailers)

**Step 3: Data Model (3 min)**
```
Users (id, email, name, preferences)
Movies (id, title, description, release_date, genre, rating)
Theaters (id, name, location, capacity)
Showtimes (id, movie_id, theater_id, start_time, available_seats)
Bookings (id, user_id, showtime_id, seats, payment_status)
Reviews (id, user_id, movie_id, rating, comment)
```

**Step 4: Key Features & Trade-offs (5 min)**

**Search:**
- Use Elasticsearch for fast full-text search
- Index on: title, actors, directors, genres
- Cache popular searches in Redis

**Booking System:**
- Handle concurrency: use database transactions with row-level locking
- Problem: Two users booking same seat simultaneously
- Solution: Optimistic locking or seat reservation with timeout (5 min hold)

**Recommendations:**
- Start simple: "Users who liked X also liked Y" (collaborative filtering)
- Future: ML model trained on user viewing/booking history
- For now: Pre-compute recommendations nightly, cache in Redis

**Scalability:**
- Read-heavy workload (browsing >> booking)
- Cache aggressively: movie listings, theater info, popular searches
- Database read replicas for search queries
- Write to primary for bookings
- Consider: Separate booking service if it becomes bottleneck

**Step 5: Monitoring & Reliability (2 min)**
- Monitor booking success rate (critical metric)
- Alert on failed payments or booking errors
- Log all transactions for auditing
- Circuit breaker for external APIs (theater systems, payment)

**Key Questions to Ask:**
- "Is this consumer-facing only or do theaters need an admin panel?"
- "What's the expected traffic? Peak during new releases?"
- "Do we need real-time seat availability or is eventual consistency okay?"
- "Any geographic considerations? Multi-region deployment?"

---

## 3. Complex Project - SDUI Story (STAR, 2-3 min)

**Situation:** At Headspace, every screen change for 70M users required separate iOS and Android app store releases. Even simple bug fixes took days to deploy through the app review process, and we had to coordinate releases across two platforms.

**Task:** I was one of the first two engineers selected to lead our server-driven UI migration - a year-long initiative to move all mobile app display logic to server-side control. I led the onboarding flow team.

**Action:** We researched Netflix and Airbnb's approaches and adopted Airbnb's sections-and-screens architecture. I transitioned from Python to TypeScript to enhance our Node.js Hapi API. I collaborated daily with cross-functional teams through async standups, worked closely with a principal engineer who knew Headspace's systems, and partnered with iOS/Android teams, product, and legal for GDPR compliance.

**Result:** We released on time in June. Feature velocity increased dramatically - what took days through app store review now takes hours. We can hotfix bugs immediately, iterate on onboarding without app releases, and maintain iOS/Android consistency from a single source. Business impact: faster feature delivery, reduced coordination overhead, and ability to A/B test flows server-side.

**If they dig deeper:**
- Challenges: Deciding granularity, handling offline mode, GDPR compliance
- Team size: 2 leads (me + principal), expanded to ~8 engineers
- Timeline: 1 year project, delivered on time
- Tech stack: Node.js Hapi API, TypeScript, sections-and-screens architecture

---

## 4. Django/API Experience (2 min) - LIKELY FOR BACKEND ROLES

"I've built Django REST APIs for 3+ years at Headspace and SpecialNeeds.com. At Headspace, I work with DRF daily on backend APIs serving mobile apps - extending authentication with JWT/Auth0, building onboarding APIs with GDPR consent workflows, and creating therapy intake endpoints with multi-step validation. At SpecialNeeds.com, I built the entire Django backend from scratch - data models for a directory platform, RESTful endpoints for search/filtering/messaging, JWT auth with role-based permissions, and custom API endpoints for LLM-powered content generation. I focus on developer experience - clear error messages, consistent response formats, proper HTTP status codes, API versioning, and documentation. For partner-facing APIs, reliability and clarity are critical."

**Specific examples ready:**
- Authentication: JWT/Auth0 integration at Headspace
- Complex workflows: Multi-step onboarding with GDPR consent
- Greenfield: Entire Django backend for SpecialNeeds.com
- Performance: Database query optimization, N+1 query prevention
- API design: RESTful patterns, versioning, error handling

---

## 5. AI Experience & Future of Engineering (2 min) - VERY CURRENT TOPIC

**How I use AI:**
"I use AI in two ways: building systems WITH AI and using AI to build faster. At SpecialNeeds.com, I architected a Langchain-based content generation system with 70 virtual authors, multi-provider fallback (free tiers → paid models), and automated quality scoring. In my daily work, I use Claude Code as a thought partner for debugging Django queries, mapping unfamiliar codebases, and prototyping in languages I'm less familiar with - like when I built a native iOS app in 2.5 hours for a technical interview starting from zero iOS knowledge."

**Future of engineering (3-5 years):**
"AI is shifting engineering from writing every line to architecting systems and directing AI assistants. Engineers who thrive will treat AI as a force multiplier. I'm preparing by using AI daily in production - building LLM systems taught me about prompt engineering, safety rails, and when to trust AI versus requiring human review. The role is evolving from 'code writer' to 'system architect who leverages AI,' and I'm already operating in that space."

**Concrete example (STAR):**
- **Situation:** Needed consistent, high-quality content generation at SpecialNeeds.com
- **Task:** Build a system that produces publication-ready articles without manual oversight
- **Action:** Multi-step Langchain pipeline, 70 virtual authors, cost optimization (try cheap models first, escalate only if quality <80%)
- **Result:** Hundreds of articles generated, near-zero cost (free tiers handle most), site ranks for thousands of keywords

---

## Backup Topics (If Time)

### Learning from a Mistake (Better than the HTTPS story)
**Situation:** Pushed a Django migration during business hours without considering production scale differences.
**Task:** Add database index (worked fine in staging).
**Action:** Production table was 100x larger - index creation locked table for 3 minutes during peak traffic.
**Result:** Implemented migration checklist: check for locks, use CONCURRENTLY flag, run during off-hours, review execution plan. Built tool to analyze migrations and flag risky operations automatically.

### Disagreement with Teammate
**Situation:** DevOps wanted Kubernetes for WordPress content site.
**Task:** Evaluate if complexity was justified.
**Action:** Asked "what problem does this solve?" - we had serverless DB, solid caching, no performance issues. Offered to help with POC but suggested documenting scaling concerns first.
**Result:** Stayed with Docker (right call for our scale). Learned to start with the problem, not the technology.

---

## Questions to Ask Them (Pick 2-3)

1. **Technical curiosity:** "What's the most interesting technical challenge your team is tackling right now?"
2. **Culture fit:** "You've been at [Company] X years - what's kept you here? What do you love most about the team?"
3. **Growth:** "How does [Company] approach technical mentorship and growth for senior engineers?"
4. **Role-specific:** "For this role, what does the balance look like between building new features versus maintaining existing systems?"
5. **AI focus:** "How are engineering teams incorporating AI into their development workflows?"

**The rule:** Ask about THEM and their work, not about passing interviews. Show peer-level curiosity.

---

## Pre-Interview Checklist

- [ ] Pause 2 seconds before answering
- [ ] Use STAR format for stories
- [ ] Include business impact in results
- [ ] Cut filler: "you know," "kind of," "I think"
- [ ] Keep answers 2-3 minutes max
- [ ] Ask clarifying questions on system design
- [ ] Show curiosity, not desperation
