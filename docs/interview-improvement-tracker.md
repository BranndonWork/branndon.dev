# Interview Improvement Tracker

A living document to track interview performance patterns across multiple interviews.

---

## Strengths (Keep Doing These)

### Rapport & Communication
- [x] Natural conversation flow — interviewers stay engaged
- [x] Self-awareness about weaknesses without being self-deprecating
- [x] Mentoring philosophy resonates with senior interviewers
- [x] Career story (startup growth, trajectory from senior → lead → architect) is compelling

### Behavioral / Experience Questions
- [x] Real debugging stories with specific technical details
- [x] Can articulate trade-offs from past projects
- [x] MVP-first thinking — avoid over-engineering
- [x] Adaptability / context-switching framed as a strength

### System Design (Conceptual)
- [x] Asks about compliance (HIPAA, PII) early
- [x] Knows BAA requirements and compliant hosting options (Bedrock, self-hosted)
- [x] Token optimization strategies (caching, context trimming, input limits)
- [x] LLM router concept (simple → cheap model, complex → capable model)
- [x] User experience focus — "what does the customer see when things fail"
- [x] Fallback/graceful degradation thinking

---

## Weaknesses (Focus Areas)

### System Design Execution

| Issue | Pattern | Fix |
|-------|---------|-----|
| **No diagram drawn** | Talked concepts but never drew boxes/arrows | Open diagramming tool BEFORE the call. Draw while talking, even if ugly. |
| **Reactive, not proactive** | Responded to interviewer questions instead of driving | Use the data flow framework: Entry → Queue → Process → Storage → Output → Failure. Drive first 5 minutes. |
| **Skipped requirements gathering** | Jumped to solutions before understanding constraints | Always ask: Scale? Latency requirements? Real-time or batch? Existing systems? |
| **Stayed conceptual** | Discussed ideas but didn't name specific services | Name AWS services explicitly: SQS, DynamoDB, ECS, Fargate, S3, etc. |
| **"I would ask the team"** | Signals uncertainty, defers decision-making | Replace with: "My instinct is X because Y, but I'd validate before committing." |

### Time Management

| Issue | Pattern | Fix |
|-------|---------|-----|
| **Technical difficulties** | Lost ~7 min to audio/browser issues | Test audio/video 10 min before. Have backup browser ready. |
| **Ran out of time** | Design portion compressed, incomplete | Watch the clock. If 25 min for design, spend max 5 on requirements, 15 on architecture, 5 on trade-offs. |

### Confidence Signals

| Issue | Pattern | Fix |
|-------|---------|-----|
| **Deferring to interviewers** | "I would see how you guys do it" | State your position first, then acknowledge collaboration. |
| **Hedging too much** | "I don't know if..." "I'm not sure..." | Make a decision, state it, acknowledge trade-offs. Wrong + confident > uncertain. |

---

## Interview-by-Interview Log

### Interview #1: Architecture & Design (2026-02-09)

**Format:** 1hr — 30min behavioral, 25min system design, 5min Q&A

**What worked:**
- HIPAA/compliance question landed well
- Mentoring philosophy resonated
- User experience focus praised
- Career trajectory story was compelling

**What didn't:**
- No diagram drawn despite having Excalidraw open
- Didn't drive the system design — responded to prompts
- Said "I would ask how you guys do it" twice
- Technical issues ate 7 minutes
- Design felt incomplete when time ran out

**Result:** Awaiting feedback

---

## Pre-Interview Checklist

Use this before every system design interview:

```
[ ] Diagramming tool open and tested (Excalidraw, draw.io)
[ ] Audio/video tested 10 min before
[ ] Backup browser ready
[ ] Water nearby
[ ] Data flow framework memorized:
    Entry → Queue → Process → Storage → Output → Failure
[ ] AWS services ready to name:
    - Compute: ECS, Fargate, Lambda, EC2
    - Queue: SQS (FIFO vs Standard), SNS
    - Storage: S3, EFS, RDS, DynamoDB
    - Cache: ElastiCache (Redis)
    - ML: Bedrock, SageMaker, Textract
```

---

## Phrases to Avoid → Replace With

| Avoid | Replace With |
|-------|--------------|
| "I would ask how you guys do it" | "My approach would be X. I'd validate with the team before finalizing." |
| "I'm not sure if..." | "My instinct is... The trade-off is..." |
| "I haven't done that before" | "I haven't done exactly that, but my mental model is..." |
| "Does that make sense?" | "Let me know if you want me to go deeper on any part." |
| "I don't know" | "I'd need to research that, but my hypothesis is..." |

---

## Topics to Study

Based on interview gaps, prioritize studying:

- [ ] AWS service selection (when to use what)
- [ ] Drawing architectures quickly (practice with timer)
- [ ] Driving system design conversations (practice mock interviews)
- [ ] Stating opinions confidently with trade-off acknowledgment

---

*Last updated: 2026-02-09*
