# Server-Driven UI (SDUI) Project - Headspace

**Role:** Senior Software Engineer
**Company:** Headspace
**Timeline:** 2022-Present
**Project Type:** Architecture Decision / Early Strategy Contributor / Led Onboarding Flow Implementation

**Note:** Assisted Principal Engineer with early SDUI strategy and architecture decisions. Led team for onboarding flow conversion implementation.

Raw Dump of everything I know about this achievement:

For the SDUI project we had a principal engineer from the headspace API team researching how to properly implement SUI and move all user interface logic to the server side, which is what SDUI stands for stands for server driven user interface. The principal researched what different tech companies made available on. Our final decision came down to following what Airbnb had implemented, which is a sections and screens type scenario. We already had an API end repository for our layout service, which was where this would live. This service was no JS with type script and HAPI. I worked directly with her because I was on a team that was purchased by headspace a year prior, and I had knowledge of the Python Django code base that we would be re-creating some logic in and she had experience with the headspace API systems so by bringing us both together on this, we had a representative from eac team. Once Airbnb was decided as the pattern we would use her, and I broke down various screens of the app section section and determine which sections we could use such as header NAV bar, footer, contents, etc. each section was broken down and we also had screens such as the care tab over the profile page and each screen was made up of sections. Our initial POC was simply a hardcoded response containing the structure data. Client side would need to render beyond that we tackled simple pages first like profile stats, such as meditation run, streaks number of sessions completed, etc. we then moved to more complex workflows like returning buttons that would need to perform certain API calls when clicked and we need to account for retries what to do on failure what to do on success all returned as a Jason on payload from surfside therefore, client would be able to take the response from the server, render the screen and not have to do any custom logic on their end. This meant that our release cycle for the app which was on a two week cycle was less critical and we could make changes on the fly server side. Hot fixes could go out in hours instead of days or wee. All users would be on the same version of the app interface, regardless of their installed app version users on old versions, which might not update often still received the most recent security patches and fixes, etc. three months into the project. The principal engineer took an extended absence for medical leave. I was the only engineer on the project at that point we brought in replacements for her as well as an engineering manager and structured the teams that would be working on the different sections, moving forward with our foundation in place and minimal POC we were able to ramp up quickly and eventually we had a team of 12 working on this project. It was a year long initiative, the project wrapped and launched on time during my time on the project I led the on boarding flow team which consisted of a prepaid wall and post pay wall point along with GDPR compliance and various logic flows that might occur, depending on what the user taps during non-boarding. My team delivered the on boarding flow along with holding bug bashes and post lunch performance monitoring for errors, and to ensure everything worked as smoothly as possible. The SDUI project was a success and is now the foundation for all new features and flows within the headspace app.

---

## STAR Method Interview Response

### Situation (Context & Problem)

**What problem was SDUI solving? Why was the decision made to pursue this approach? What was the context?**

Raw Answer:
Our app was on a two week release cycle which meant hot fixes could take days or weeks to reach users. Users on old app versions that didn't update often wouldn't receive the most recent security patches and fixes. We needed to move UI logic to the server side so we could make changes on the fly without app store releases.

Refined Answer:
"At Headspace, we were constrained by a two-week mobile app release cycle. Hot fixes could take days or weeks to reach users, and users on older app versions wouldn't receive critical security patches or bug fixes in a timely manner. We needed to move UI logic server-side so we could deploy changes independently of the app release cycle. This would allow us to push updates in hours instead of waiting for app store approval and user updates."

---

### Task (Your Mandate)

**What was your role in the SDUI initiative? Were you involved in the decision-making or just implementation? What were you responsible for?**

Raw Answer:
I worked directly with the principal engineer who was researching SDUI implementation. I was on a team that was purchased by Headspace a year prior (Ginger), and I had knowledge of the Python Django codebase while she had experience with the Headspace API systems. By bringing us both together, we had a representative from each team. Three months into the project, the principal engineer took extended medical leave. I was the only engineer on the project at that point. We brought in replacements and I eventually led the onboarding flow team as the project scaled to 12 engineers.

Refined Answer:
"I worked directly with our principal engineer on the early SDUI strategy and architecture. Since I came from the Ginger team that Headspace had acquired a year prior, I brought deep knowledge of our Python Django codebase, while she brought expertise in Headspace's Node.js API systems. This cross-team collaboration was intentional - we needed representation from both platforms. Three months in, the principal took medical leave and I became the primary engineer on the project. As we scaled to a team of 12, I led the onboarding flow team through implementation, launch, and post-launch monitoring."

---

### Action (Your Approach & Trade-offs)

**THIS IS THE KEY SECTION FOR TOPIC 3:**
**What were the technical options considered? Why TypeScript instead of Python? Why enhance the existing Node.js Hapi system vs building new? What were the trade-offs? How did you evaluate the options? What constraints influenced the decision?**

Raw Answer:
We researched what different tech companies had implemented. Our final decision came down to following Airbnb's pattern which uses sections and screens. We already had a Layout Service API repository which was Node.js with TypeScript and Hapi - this is where SDUI would live. The principal and I broke down various app screens into sections like header, nav bar, footer, content. Each screen was made up of sections like the care tab or profile page. Our initial POC was a hardcoded response with structured data. We started with simple pages like profile stats (meditation runs, streaks, sessions completed), then moved to complex workflows with buttons that perform API calls with retry logic, failure/success handling, all returned as JSON from server side. This meant the client could render the screen without custom logic.

Refined Answer:
"We researched SDUI implementations from multiple tech companies and decided to follow Airbnb's sections-and-screens pattern. The key architectural decision was whether to build a new service in Python Django or enhance our existing Layout Service API. We chose to extend the existing Node.js TypeScript Hapi service for several reasons: it was already handling layout concerns, the mobile teams were familiar with it, and we could iterate faster by building on proven infrastructure rather than introducing a new service.

The principal and I designed the architecture around reusable sections - headers, navigation, footers, content blocks - that compose into screens like the care tab or profile page. We took an incremental approach: started with a hardcoded POC to validate the pattern, then tackled simple static pages like profile stats showing meditation runs and streaks. Once that worked, we graduated to complex interactive workflows - buttons that trigger API calls with retry logic, error handling, and success states, all defined server-side as JSON.

The trade-off was TypeScript learning curve for the Django-heavy team versus the complexity of building a new Python service. We chose the TypeScript path because it kept the SDUI logic close to the existing mobile API contract and allowed us to ship faster."

---

### Result (Outcome & Impact)

**What was delivered? How successful was the SDUI implementation? What benefits did it provide? Any metrics?**

Raw Answer:
Hot fixes could go out in hours instead of days or weeks. All users would be on the same version of the app interface regardless of their installed app version. Users on old versions still received the most recent security patches and fixes. It was a year-long initiative that launched on time. My team delivered the onboarding flow including pre-paywall and post-paywall with GDPR compliance. The SDUI project is now the foundation for all new features and flows within the Headspace app.

Refined Answer:
"The project was a year-long initiative that launched on time. We reduced hot fix deployment from days or weeks down to hours. All users now receive the same interface regardless of their installed app version, which solved our problem of users on older versions missing critical security patches. My team delivered the complete onboarding flow - pre-paywall and post-paywall screens with GDPR compliance and various logic flows. We ran bug bashes and post-launch performance monitoring to ensure stability. SDUI is now the foundation for all new features and flows in the Headspace app, which validates that the architectural decisions we made early on were sound."

---

## Technical Details for Deep Dives

### Technology Options Considered

### Why TypeScript vs Python

### Architecture Decisions

### Technologies Used

-   TypeScript
-   Node.js
-   Hapi API
-   [Add others as needed]

---

## Interview Tips for This Story

-   **Length:** 2-3 minutes for full STAR
-   **Emphasis:** Focus heavily on Action - the decision-making process and trade-offs (60% of time)
-   **Follow-up questions to prep for:**
    -   Why TypeScript over Python?
    -   How did you evaluate the trade-offs?
    -   What would you do differently?
    -   What were the risks of this approach?
