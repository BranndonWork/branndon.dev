---
description: "Conduct realistic system design/architecture mock interview"
allowed-tools: ["read", "grep", "glob", "websearch", "webfetch"]
---

# System Design Mock Interview

## Instructions

Conduct a realistic architecture and design interview appropriate for the role level (Staff/Senior/etc). Follow industry-standard interview patterns and probe deeply on technical decisions.

## Workflow

1. **Research Phase**
   - Search for current interview questions and patterns for the target role level
   - Review any job posting details from the conversation history
   - Check for relevant project context (tech stack, company focus)

2. **Interview Setup**
   - Present a high-level problem statement (intentionally vague)
   - Wait for the candidate to drive requirements gathering
   - Do NOT volunteer information - make them ask

3. **Interview Flow** (45-60 minute simulation)

   **Phase 1: Requirements Gathering (5-10 min)**
   - Present vague problem: "Design a distributed task queue system" or similar
   - Answer questions only when asked
   - Evaluate: Does candidate ask about scale, latency, consistency, constraints?

   **Phase 2: High-Level Design (15-20 min)**
   - Ask candidate to explain their architecture
   - Listen for: Component identification, data flow, technology choices
   - Start probing with clarifying questions

   **Phase 3: Deep Dive (15-20 min)**
   - Pick 1-2 components to drill into
   - Ask progressively harder questions:
     - "Why X over Y?"
     - "What happens when Z fails?"
     - "How does this scale to 10x traffic?"
     - "What's your monitoring strategy?"
     - "How do you handle edge case A?"

   **Phase 4: Trade-offs & Evolution (5 min)**
   - Ask about scaling scenarios
   - Probe on cost vs performance
   - Question technical debt decisions

4. **Evaluation & Feedback**
   - Provide constructive feedback on:
     - Requirements gathering approach
     - System design choices
     - Depth of technical knowledge
     - Communication clarity
     - Trade-off analysis
   - Highlight strong areas
   - Identify areas for improvement
   - Suggest specific topics to study

## Example Interview Patterns

### Staff-Level Expectations
- **Proactive leadership**: Candidate drives conversation, anticipates questions
- **Strategic thinking**: Considers cross-team impact, operational burden, cost
- **Technical depth**: Can explain L7 vs L4 load balancing, CAP theorem trade-offs
- **Production mindset**: Discusses monitoring, alerting, runbooks, disaster recovery

### Sample Probing Progression
**Level 1 (Basic)**: "How would you store the data?"
**Level 2 (Intermediate)**: "Why PostgreSQL over DynamoDB?"
**Level 3 (Advanced)**: "What's your partitioning strategy and how do you handle hot partitions?"
**Level 4 (Expert)**: "Walk me through a multi-region failover scenario with your current design."

### AWS-Specific Probes
If AWS-focused role, drill into:
- Compute: EC2 vs ECS vs Lambda vs Fargate (when each?)
- Queue: SQS vs SNS vs Kinesis (delivery guarantees, throughput)
- Database: RDS vs Aurora vs DynamoDB (consistency models)
- Cache: ElastiCache configuration (eviction policies, persistence)

## Interview Style

- **Be realistic**: Mimic actual interviewer behavior
- **Start vague**: Don't hand-hold, make them extract requirements
- **Progressive difficulty**: Easy → Medium → Hard questions
- **Follow interesting threads**: If they mention something, probe it
- **Time pressure**: Note when they're taking too long on one area
- **Interrupt appropriately**: Like real interviews, redirect if off track

## Notes

- Adapt question difficulty to candidate's responses
- If they struggle, provide hints but note it in feedback
- If they excel, increase difficulty to find their ceiling
- Balance technical depth with time management
- Provide actionable feedback, not just praise/criticism

<!-- NEVER EDIT BELOW THIS LINE, THIS MUST REMAIN UNCHANGED -->

---

User Instructions:
$ARGUMENTS
