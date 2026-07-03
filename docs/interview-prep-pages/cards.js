// ═══════════════════════════════════════════════════════════════════
// INTERVIEW PREP CARDS DATA
// To add a question: push a new object to this array.
// To remove one: delete the object.
// sidebar: null = no sidebar box
// quote: null = no quote box
// sidebar items: { label: "Situation", text: "..." }
//                { label: null, text: "..." }  ← no bold label
// ═══════════════════════════════════════════════════════════════════

const CARDS_DEFAULT = [
    {
        id: 1,
        navLabel: "1. Tell me about yourself",
        navSubtitle: "2 min intro",
        color: "blue",
        heading: "1. Tell me about yourself (2 min)",
        points: [
            'I\'m Branndon Coelho (rhymes with "mello"), a senior software engineer with over 15 years of experience, most recently at Headspace.',
            "I specialize in Python, Django, and building scalable API systems on the backend.",
            "I've worked with React, Next.js and various frontend technologies.",
            "My work spans architecting production LLM applications with Langchain to leading Headspace's server-driven UI migration that cut feature release cycles from days to hours.",
            "I'm passionate about AI, automation, performance, and building resilient systems.",
        ],
        sidebar: null,
        quote: null,
    },
    {
        id: 2,
        navLabel: "2. Tell me about a big project",
        navSubtitle: "SDUI migration story",
        color: "purple",
        heading: "2. Tell me about a time you led a big project (STAR, 2 min)",
        points: [
            "At Headspace, every screen change for our 70M users required separate iOS and Android app store releases, and even bug fixes took days through the app store review process.",
            "I was one of the first two engineers selected to lead our server-driven UI migration, a year-long initiative to move all mobile app display logic to server-side control.",
            "We researched Netflix, Airbnb, and other approaches, eventually landing on Airbnb's sections-and-screens architecture.",
            "For the project I transitioned from Python to TypeScript to integrate the server-side changes into the Node.js API.",
            "We released on time, and feature velocity increased dramatically. What took days to release now takes minutes to hours.",
            "We can hotfix bugs immediately, release UI changes without app store delays, and maintain iOS/Android consistency on a level that wasn't possible before.",
        ],
        sidebar: {
            title: "STAR breakdown:",
            items: [
                {
                    label: "Situation",
                    text: "Every screen change required iOS/Android app store releases, bug fixes took days",
                },
                {
                    label: "Task",
                    text: "Lead server-driven UI migration, year-long initiative for 70M users",
                },
                {
                    label: "Action",
                    text: "Researched approaches, adopted Airbnb architecture, learned TypeScript, ensured GDPR compliance",
                },
                {
                    label: "Result",
                    text: "Released on time, feature velocity from days to hours, immediate hotfixes",
                },
            ],
        },
        quote: null,
    },
    {
        id: 3,
        navLabel: "3. Tell me about pushing back",
        navSubtitle: "Kubernetes vs Docker",
        color: "indigo",
        heading: "3. Tell me about a time you pushed back (STAR, 2 min)",
        points: [
            "At The Penny Hoarder, our DevOps engineer wanted to migrate our WordPress site from pure Docker to Kubernetes with full orchestration.",
            "I pushed back respectfully by asking what problem this solved . We were a content site with a serverless database on RDS, not a high-transaction app needing Kubernetes complexity.",
            "I explained my concerns about adding unnecessary complexity when we didn't need orchestration at our scale, but suggested my manager give him space for a proof of concept.",
            "In the end, the implementation and deployment complexity became a blocker, and we stayed with Docker.",
        ],
        sidebar: {
            title: "STAR breakdown:",
            items: [
                {
                    label: "Situation",
                    text: "DevOps engineer wanted to migrate WordPress from Docker to Kubernetes",
                },
                {
                    label: "Task",
                    text: "Evaluate if complexity justified for content site needs",
                },
                {
                    label: "Action",
                    text: "Asked what problem it solved, explained unnecessary complexity, suggested POC",
                },
                {
                    label: "Result",
                    text: "Implementation complexity became blocker, stayed with Docker",
                },
            ],
        },
        quote: null,
    },
    {
        id: 4,
        navLabel: "4. Tell me about a mistake",
        navSubtitle: "HTTPS migration issue",
        color: "red",
        heading: "4. Tell me about a production mistake (STAR, 2 min)",
        points: [
            "At The Penny Hoarder, I was leading the HTTP to HTTPS conversion when pages started loading without CSS intermittently. They'd render but look completely broken.",
            "I traced it to a CloudFront caching issue where certain iOS versions would cache pages with http:// stylesheet links, and whichever device hit first determined the cache for everyone.",
            "I fixed it by correcting the server-level cache before it reached CloudFront, ensuring all devices got proper HTTPS references, then invalidated CloudFront to clear the bad cache.",
            "Now I always test cross-device caching behavior before any protocol or CDN changes.",
        ],
        sidebar: {
            title: "STAR breakdown:",
            items: [
                {
                    label: "Situation",
                    text: "Leading HTTP to HTTPS conversion, pages loading without CSS intermittently",
                },
                {
                    label: "Task",
                    text: "Figure out why some pages broken for everyone, others fine",
                },
                {
                    label: "Action",
                    text: "Traced to CloudFront caching issue, fixed server-level cache, invalidated CDN",
                },
                {
                    label: "Result",
                    text: "Issue resolved, now always test cross-device caching before protocol changes",
                },
            ],
        },
        quote: null,
    },
    {
        id: 5,
        navLabel: "5. Critical production problem",
        navSubtitle: "Therapy matching during peak traffic",
        color: "teal",
        heading: "5. Tell me about a critical production problem (STAR, 2 min)",
        points: [
            "During Mental Health Awareness Month at Headspace, our therapy matching system was taking 8+ seconds under 3x normal traffic, and 23% of users were abandoning the flow.",
            "I led a small team to stabilize it quickly. We investigated and found complex unoptimized database queries and redundant calculations in the matching algorithm.",
            "I tackled the database optimization myself, rewrote Django queries to eliminate N+1 issues, added indexes that dropped query time from 6 seconds to under 1 second, while another engineer added Redis caching for therapist availability.",
            "The tricky part was working with product. The matching had 8+ factors adding computational complexity, so I presented data showing performance cost versus user value and we simplified to 5 core criteria with optional refinement.",
            "Within two weeks we got matching time down to 1.2 seconds, abandonment dropped to 8%, and the system handled peak load without issues for the rest of the month.",
        ],
        sidebar: {
            title: "STAR breakdown:",
            items: [
                {
                    label: "Situation",
                    text: "Mental Health Awareness Month, 8+ second matching time, 23% abandonment rate",
                },
                {
                    label: "Task",
                    text: "Lead team to stabilize system quickly under 3x traffic load",
                },
                {
                    label: "Action",
                    text: "Optimized Django queries, added Redis caching, simplified matching criteria with product",
                },
                {
                    label: "Result",
                    text: "1.2 second matching, 8% abandonment, system stable rest of month",
                },
            ],
        },
        quote: null,
    },
    {
        id: 6,
        navLabel: "6. Mentoring philosophy",
        navSubtitle: "Show don't tell, PR reviews, build judgment",
        color: "purple",
        heading: "6. What is your philosophy on mentoring? (2 min)",
        points: [
            "A good mentor spots a problem, says \"I've seen this before, here's how we solved it\", and shows you what to do going forward instead of just pointing out that something is wrong.",
            "The best mentoring I've received came through PR reviews. By someone pointing out that we had a function that already did what I was reinventing, or a way to collapse three database calls into one. That kind of feedback made me genuinely better.",
            "At Headspace with 500 engineers, nobody knows a 10-year-old system end to end. You can't learn about those things unless someone is willing to take a moment and show you.",
            "I mentor the same way: I look for patterns, not one-off mistakes. If someone's variable naming is vague or they're duplicating something that already exists, I share the standard or the existing solution.",
            "At The Penny Hoarder I ran weekly release during our Teaching Tuesdays lunch meeting. At Headspace I mentored junior engineers and promoted best practices across the team.",
            "I want the person I'm mentoring to walk away knowing why, not just what, so they can make the right call on their own next time.",
        ],
        sidebar: {
            title: "Key themes to hit:",
            items: [
                {
                    label: "Show, don't just tell",
                    text: "Point to the existing solution, don't only flag the problem",
                },
                {
                    label: "Context matters",
                    text: "Large systems mean nobody knows everything. Mentors fill that gap",
                },
                {
                    label: "PR reviews as mentoring",
                    text: "Real-world example from Headspace",
                },
                {
                    label: "Track record",
                    text: "Penny Hoarder weekly reviews, Headspace junior engineers",
                },
                {
                    label: "Goal",
                    text: "Build judgment, not just compliance",
                },
            ],
        },
        quote: {
            text: "\"That's what I think a good mentor is... saying 'I see a problem where this could be better, I've seen this before, here's how we solved for it, and this is probably what you should do going forward instead of recreating it.'\"",
            note: "Memorize this as your natural close.",
        },
    },
    {
        id: 7,
        navLabel: "7. Why are you looking?",
        navSubtitle: "Laid off, restructuring, what's next",
        color: "orange",
        heading: "7. Why are you looking? / Why did you leave Headspace? (30 sec)",
        points: [
            "I was laid off in October 2025 as part of a company restructuring.",
            "I've been intentional about the search since then. I'm looking for a senior role where I can own meaningful backend systems and stay close to the work, not just coordinate it.",
            "What draws me to opportunities like this one is the chance to build things that have a real impact, not just internal tooling or growth features, but systems that matter to users.",
        ],
        sidebar: {
            title: "Key points:",
            items: [
                {
                    label: null,
                    text: "Lead with the fact: laid off, restructuring, then move on immediately",
                },
                {
                    label: null,
                    text: "Don't dwell on it, one sentence and move on",
                },
                {
                    label: null,
                    text: "Pivot to what you're looking for, not what you're running from",
                },
                {
                    label: null,
                    text: "Close on something genuine about why this role/company interests you",
                },
            ],
        },
        quote: null,
    },
    {
        id: 8,
        navLabel: "8. Conflicting priorities",
        navSubtitle: "SDUI + GDPR deadline collision",
        color: "green",
        heading: "8. Conflicting priorities (STAR, 2 min)",
        points: [
            "While I was leading the SDUI onboarding flow migration at Headspace (a year-long initiative) a GDPR compliance requirement came in with a hard regulatory deadline that couldn't move.",
            "I was the person who knew both the onboarding systems and the GDPR data flows, so I couldn't hand it off cleanly. The SDUI work had its own timeline with downstream mobile teams depending on it.",
            "I sat down with both PMs to map out the actual hard blockers versus the flexible milestones. The SDUI work had a two-week window where mobile was in a code freeze anyway, so I used that to focus entirely on the GDPR implementation (data anonymization workflows and DSAR request handling) without losing real time on SDUI.",
            "Both shipped on time. The key was being upfront early about the conflict rather than trying to silently carry both, and finding the natural slack in one timeline to absorb the pressure from the other.",
        ],
        sidebar: {
            title: "STAR breakdown:",
            items: [
                {
                    label: "Situation",
                    text: "Leading SDUI migration when a hard-deadline GDPR compliance requirement landed",
                },
                {
                    label: "Task",
                    text: "Deliver both without slipping either timeline",
                },
                {
                    label: "Action",
                    text: "Mapped hard blockers vs flexible milestones with both PMs, used mobile code freeze window to absorb GDPR work",
                },
                {
                    label: "Result",
                    text: "Both shipped on time; learned to surface conflicts early and find natural timeline slack",
                },
            ],
        },
        quote: null,
    },
];
