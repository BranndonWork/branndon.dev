# Mock Interview Plan: Trajector Staff Engineer A&D Round

**Interview:** Monday, February 9th, 2026 at 1:00 PM EST
**Interviewers:** Kelly Peterson (Staff Data Scientist) + Matthew Purdon (Principal Software Engineer)
**Focus:** Architecture & Design

---

## Interviewer Personas

### Matthew Purdon (Principal Software Engineer)
- **Background:** 20+ years IT experience, scalable/secure systems focus
- **Style:** Will probe on infrastructure, AWS choices, operational concerns
- **Questions from him:** "How does this handle failure?", "What's the migration strategy?", "How do we monitor this?"

### Kelly Peterson (Staff Data Scientist)
- **Background:** NLP/ML focus, data pipelines
- **Style:** Will probe on ML architecture, model serving, data quality
- **Questions from her:** "How do we handle OCR quality variance?", "How do you ensure extraction accuracy across document types?"

---

## Problem Statement (Tailored to Trajector)

**The Setup:**
> "We have a legacy system that processes medical documents to extract patient history for disability claims. It's slow, unreliable, and uses outdated tech. We need to redesign it with modern ML/LLM capabilities, handle handwritten documents, ensure HIPAA compliance, and migrate with zero downtime. Walk us through your approach."

**Hidden requirements (candidate must extract):**
- Scale: 100K-1M docs/month
- Latency: Batch OK (results within hours, not real-time)
- Documents: PDFs, scans, faxes, handwritten notes
- Compliance: HIPAA, PII handling
- Constraint: Zero downtime migration from legacy
- LLM: Currently third-party, evaluating options

---

## Interview Flow (45-60 min)

### Phase 1: Requirements (10 min)
- Present vague problem, wait for clarifying questions
- **Matthew probes:** Scale, SLAs, current pain points
- **Kelly probes:** Document types, accuracy requirements, current ML approach

### Phase 2: High-Level Design (15 min)
- Candidate draws architecture
- **Matthew:** Infrastructure choices (ECS vs Lambda, queue strategy)
- **Kelly:** ML pipeline (OCR → preprocessing → LLM extraction)

### Phase 3: Deep Dive - Pick 2 Topics (20 min)
1. **Zero-downtime migration** (Matthew leads)
   - "How do you migrate without disrupting claims processing?"
   - Probe: Strangler pattern, parallel running, feature flags, rollback

2. **LLM for handwritten docs** (Kelly leads)
   - "How do you handle poor quality scans and handwriting?"
   - Probe: Preprocessing, confidence scores, human-in-the-loop, accuracy metrics

3. **HIPAA/PII handling** (Both)
   - "Walk me through data flow - where does PHI live?"
   - Probe: Encryption, access controls, audit logs, third-party LLM concerns

### Phase 4: Trade-offs & Evolution (10 min)
- "What would you change at 10x scale?"
- "How do we reduce LLM costs by 50%?"
- "What's the biggest risk in this design?"

---

## Key Probing Questions

**AWS/Infrastructure (Matthew):**
- "Why SQS over Kinesis for this workload?"
- "Jobs run 30+ minutes - ECS or Lambda?"
- "How do you handle a worker crash mid-processing?"

**ML/Data (Kelly):**
- "Third-party LLM vs self-hosted - what's your recommendation given HIPAA?"
- "How do you measure extraction accuracy?"
- "What's your strategy for model updates without downtime?"

**Migration (Both):**
- "Legacy system is processing claims right now. How do you cut over?"
- "How do you validate the new system produces same results?"
- "What's your rollback plan?"

---

## What They Want to Hear

| Topic | Signal They're Looking For |
|-------|---------------------------|
| **LLM + HIPAA** | "Can't use OpenAI - no BAA. SageMaker or self-hosted for compliance." |
| **Queue choice** | "SQS for durability over Redis - can't lose medical claims." |
| **30-min jobs** | "Fargate, not Lambda (15-min limit). Workers are idempotent." |
| **Handwritten docs** | "Textract for OCR, preprocessing for quality, confidence thresholds for human review." |
| **Migration** | "Strangler pattern - route new docs to new system, backfill historical, run parallel, compare results before cutover." |
| **Monitoring** | "Queue depth, processing latency, extraction accuracy, cost per doc." |

---

## Evaluation Criteria

**Strong signals:**
- Asks about compliance/HIPAA early
- Discusses migration strategy without prompting
- Mentions idempotency for long-running jobs
- Brings up monitoring and operational concerns
- Evaluates trade-offs with pros/cons

**Red flags:**
- Suggests OpenAI for medical data without mentioning HIPAA
- Ignores migration complexity
- No mention of failure handling
- Picks tech without explaining why

---

## Background: Model Drift (Know This, Don't Need to Design It)

**What is model drift?** When ML/LLM models degrade over time because:
- Input data changes (new document formats, handwriting styles)
- The world changes (new medical terminology, form layouts)
- Third-party models get updated

**How teams handle it (general knowledge):**
- Monitor extraction accuracy metrics over time
- Compare outputs against validated ground truth samples
- Set up alerts when accuracy drops below threshold
- Data science teams retrain/reconfigure when drift is detected

**Your role as Staff Engineer:** You architect the infrastructure that *enables* the data science team to detect and respond to drift - metrics pipelines, A/B testing infrastructure, model versioning - but you're not training models yourself.

---

## Files to Reference
- `.claude/commands/mock-interview.md` - Base mock interview command
- `job-search/Trajector-Staff-Engineer/job-posting.md` - Job requirements
- `docs/system-design-interview-cheatsheet.html` - Quick reference

---

## Verification

After mock interview:
1. Provide specific feedback on each phase
2. Rate performance on the 4 competencies: Problem navigation, Solution design, Technical excellence, Communication
3. Identify 2-3 areas to study before Monday
4. Offer to drill specific weak areas
