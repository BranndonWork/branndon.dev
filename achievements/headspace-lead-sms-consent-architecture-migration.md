# SMS Consent Architecture Migration - Headspace

**Role:** Senior Software Engineer
**Company:** Headspace
**Timeline:** 2022-Present
**Project Type:** System Architecture / Backend Migration

---

## STAR Method Interview Response

### Situation (Context & Problem)

**What was the dual-source synchronization issue? What pain was this causing? How did you notice it?**

Raw Answer:
We had a legal model in our django system that recorded when users granted SMS consent, so that we could track the consent that they agreed to, the date, and the version, etc. We then put them in a certain group in Braze, where the users in the group have consented to SMS messages. The issue that I identified is that 1. our legal model only recorded "yes" consent and never a "no" consent, so we didn't track which users opted in and then later opted out, we would just have to delete the record. 2. users would be able to reply to an SMS with "unsubscribe" and braze would automatically unsubscribe them. while working on accepting SMS consent for a new feature, I noticed thisee inconsistancies in how we managed the consent and suggested that we use a single source of truth.

Refined Answer:
"At Headspace, we had a dual-source system for SMS consent - a Django legal model tracking consent grants with timestamps and versions, plus a Braze subscription group for messaging. While implementing SMS consent for a new feature, I identified critical synchronization issues. Our Django database only tracked opt-ins, never opt-outs - we'd simply delete records. Meanwhile, users could text 'unsubscribe' and Braze would immediately remove them from the group, leaving our systems out of sync. This created data integrity problems and potential compliance risks."

---

### Task (Your Mandate)

**What was your mandate? Were you assigned this or did you propose it? What was the scope?**

Raw Answer:
I asked the stakeholders where they accessed the data, and what the legal requirements were. I recommended storing all SMS consent directly in braze, since it had an unsubscribe feature, and activity traile, we could tell when a user subscribed/unsubscribed easier. The django db was redundant and out of sync, and if not an absolute necessity for legal compliance, Braze would be a better location. after talking to all the right people, it was agreed that braze was the solution.

Refined Answer:
"I proactively identified this as a problem that needed solving. Rather than just implementing a workaround for my immediate feature work, I consulted with stakeholders across legal, product, and engineering to understand our compliance requirements and data access patterns. I proposed consolidating to Braze as our single source of truth - it already had unsubscribe functionality, audit trails, and better tracking. After getting buy-in, I took ownership of leading the full architecture migration."

---

### Action (Your Approach & Execution)

**What research did you do? What alternatives did you consider? Why Braze API single-source vs other options? What was the technical implementation approach? Any challenges during execution?**

Raw Answer:
I lead the migration, including backfilling sms consent into braze where necessary, backing up the legal database model, and updating all aspects of the django codebase to use a new service based sstructure for managing sms consent, making a single location that we can use to manage all sms consent, check status, etc. it was a braze api wrapper with many checks and balances and caches since this is someting that doesn't change all that often.

Refined Answer:
"I led the complete migration from dual-source to single-source architecture. First, I backed up our legal database model for audit purposes, then backfilled existing SMS consent records into Braze where needed. The core technical work was refactoring our Django codebase to use a service-based architecture - I built a Braze API wrapper that became the single point of control for all SMS consent operations. This service handled consent status checks, opt-ins, opt-outs, and included intelligent caching since consent state doesn't change frequently. The wrapper also had multiple validation checks to ensure data integrity throughout the migration."

---

### Result (Outcome & Impact)

**Specific metrics: reduced failures by X%? Eliminated Y sync errors? System reliability improvement? Team/business impact?**

Raw Answer:
In the end, we eliminated the dual-source synchronization problems, improving system reliability and reducing compliance risk. The new single-source architecture simplified our codebase, made consent tracking more transparent, and provided an accurate, auditable record of user consent preferences.

Refined Answer:
"We completely eliminated the dual-source synchronization issues - no more data inconsistencies between systems. The migration improved system reliability by removing a major source of potential compliance risk in our healthcare platform. Beyond fixing the immediate problem, the new service-based architecture simplified our codebase and made consent tracking completely transparent with full audit trails. Any engineer on the team can now work with SMS consent through a single, well-defined interface rather than navigating two separate systems."

---

## Technical Details for Deep Dives

### Architecture Before

### Architecture After

### Key Technical Decisions

### Technologies Used

-   Braze API
-   [Add others as needed]

---

## Interview Tips for This Story

-   **Length:** 2-3 minutes for full STAR
-   **Emphasis:** Focus on Action (50% of time) and proactive problem identification
-   **Follow-up questions to prep for:**
    -   Why did you choose Braze over alternatives?
    -   What was the migration strategy?
    -   How did you handle rollback scenarios?
    -   What would you do differently?
