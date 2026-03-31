# Staff-Level System Design Interview Guide

**The Complete Playbook for Architecture & Design Interviews**

---

## What This Guide Covers

This guide teaches you HOW to answer system design questions at the staff engineer level, not just WHAT to answer. It's based on real interview patterns and what senior interviewers actually look for.

**You'll learn:**
- The exact framework to structure your answers (REAADS)
- What signals interviewers are looking for at staff level
- How to think about trade-offs (the #1 skill they test)
- Common mistakes that fail otherwise strong candidates
- Real example: Medical document processing system walkthrough

---

## The Core Problem: Why Smart Engineers Fail These Interviews

**You know the technology.** You've built production systems. You can debug complex issues.

**But you're failing interviews because:**
1. You jump to solutions without understanding requirements
2. You miss the "what they're really asking" layer
3. You don't demonstrate trade-off thinking
4. You answer like a senior engineer, not a staff engineer

**Staff level is different.** It's not about knowing AWS services. It's about demonstrating:
- Strategic thinking
- Production mindset
- Cross-team impact awareness
- Cost consciousness
- Operational maturity

---

## The REAADS Framework

Use this structure for EVERY system design question. Interviewers expect this flow.

### **R - Requirements** (5-10 minutes)

**What they're testing:** Can you drive the conversation? Do you ask smart questions?

**Two types of requirements:**

**Functional Requirements** (What does it do?)
- Core features and capabilities
- User workflows
- Key use cases

**Non-Functional Requirements** (How well does it do it?)
- **Scale**: Users, requests/second, data volume
- **Performance**: Latency requirements (p50, p95, p99)
- **Availability**: Uptime requirements (99.9%, 99.99%?)
- **Consistency**: Strong vs eventual consistency
- **Durability**: Data loss tolerance

**Smart questions to ask:**
- "What's the expected scale? Current users? Growth projection?"
- "What are the latency requirements? Are we optimizing for reads or writes?"
- "What's our availability SLA? Can we have downtime?"
- "Are there compliance requirements? (HIPAA, SOC2, GDPR?)"
- "What's the budget constraint? Are we cost-optimizing or performance-optimizing?"
- "What's already built? Are we designing from scratch or integrating?"

**Staff-level signal:** You proactively ask about constraints and trade-offs, not just features.

---

### **E - Estimation** (2-3 minutes)

**What they're testing:** Can you do back-of-napkin math? Do you understand scale?

**Calculate:**
- **Storage needed**: Documents × size × retention period
- **Bandwidth**: Requests/sec × payload size
- **QPS (Queries Per Second)**: Daily users ÷ 86400 × peak multiplier
- **Database size**: Rows × row size × growth rate

**Example:**
```
Medical document system:
- 1M documents/month
- Average document: 2MB
- Storage: 1M × 2MB = 2TB/month = 24TB/year
- Peak processing: 1M docs/month ÷ 30 days ÷ 24 hours = ~1,400 docs/hour = ~25/min
```

**Staff-level signal:** You justify your architecture with numbers, not just "it scales."

---

### **A - API Design** (Optional, 5 minutes)

**What they're testing:** Can you design clean interfaces?

**Skip this if time is tight.** Focus on architecture instead.

**If you do it:**
```
POST /api/v1/documents
  - Upload document for processing
  - Returns: document_id, status

GET /api/v1/documents/{id}/status
  - Check processing status
  - Returns: status, extracted_data, confidence_scores

GET /api/v1/documents/{id}/results
  - Retrieve extraction results
  - Returns: structured_data, metadata
```

**Staff-level signal:** You think about versioning, idempotency, error responses.

---

### **A - Architecture** (15-20 minutes)

**What they're testing:** Can you design scalable systems? Do you explain your reasoning?

**High-Level Components:**
1. Start with major building blocks
2. Show data flow with arrows
3. Explain why each component exists
4. Identify communication patterns (sync/async)

**Example Architecture (Medical Documents):**
```
┌─────────────────┐
│  Upload API     │ ← REST/GraphQL
│  (API Gateway)  │
└────────┬────────┘
         │
         ├─────────────────────────┐
         ↓                         ↓
┌─────────────────┐      ┌─────────────────┐
│  Document Queue │      │  Batch Ingest   │
│  (SQS)          │      │  (S3 + Lambda)  │
└────────┬────────┘      └────────┬────────┘
         │                        │
         └────────┬───────────────┘
                  ↓
         ┌─────────────────┐
         │  Worker Pool    │
         │  (ECS Fargate)  │
         └────────┬────────┘
                  │
         ┌────────┴────────┐
         ↓                 ↓
┌─────────────────┐  ┌─────────────────┐
│  OCR Service    │  │  LLM Service    │
│  (Textract)     │  │  (SageMaker)    │
└─────────────────┘  └─────────────────┘
         │                 │
         └────────┬────────┘
                  ↓
         ┌─────────────────┐
         │  Results Store  │
         │  (PostgreSQL)   │
         └─────────────────┘
```

**As you draw, say out loud:**
- "I'm putting a queue here because we need to decouple upload from processing"
- "Workers pull from SQS to process documents asynchronously"
- "For OCR, I'm using Textract because medical documents have complex layouts"
- "Results go to PostgreSQL for structured querying"

**Staff-level signal:** You explain WHY, not just WHAT. "I chose X because Y."

---

### **D - Data Model** (5-10 minutes)

**What they're testing:** How do you structure data for this system?

**Think about:**
- Database choice (SQL vs NoSQL)
- Schema design
- Indexing strategy
- Partitioning/sharding

**Example (Medical Documents):**

```sql
-- Documents table
CREATE TABLE documents (
  id UUID PRIMARY KEY,
  source VARCHAR(255),
  status VARCHAR(50), -- pending, processing, completed, failed
  uploaded_at TIMESTAMP,
  processed_at TIMESTAMP,
  s3_location TEXT,
  INDEX idx_status_created (status, uploaded_at)
);

-- Extraction results
CREATE TABLE extraction_results (
  id UUID PRIMARY KEY,
  document_id UUID REFERENCES documents(id),
  field_name VARCHAR(255),
  field_value TEXT,
  confidence FLOAT,
  extracted_at TIMESTAMP,
  INDEX idx_document (document_id)
);
```

**Staff-level signal:** You consider query patterns and explain your indexing choices.

---

### **S - Scale & Deep Dive** (15-20 minutes)

**What they're testing:** THIS IS THE STAFF-LEVEL DIFFERENTIATOR.

**They will pick 1-2 components and drill:**

#### **Bottleneck Analysis**
- "What's the slowest part of this system?"
- "Where would this break at 10x scale?"
- "How do you handle traffic spikes?"

#### **Failure Scenarios**
- "What happens if the worker crashes mid-processing?"
- "How do you handle duplicate uploads?"
- "What if the database goes down?"

#### **Monitoring & Operations**
- "How do you monitor this in production?"
- "What metrics matter?"
- "How do you debug processing failures?"

#### **Cost Optimization**
- "What's the most expensive part?"
- "How would you reduce costs by 50%?"

---

## Trade-Off Thinking: The #1 Staff-Level Skill

**This is what separates staff from senior.**

Every decision has trade-offs. You must articulate them.

### **Example 1: LLM Choice (Medical Documents)**

**Scenario:** Need to extract data from medical documents with an LLM.

**Bad Answer (Senior Level):**
> "I'll use OpenAI's API because it's good at text extraction."

**Good Answer (Staff Level):**
> "For the LLM, we have three options:
>
> **Option 1: OpenAI API**
> - ✅ Fast to implement, no infrastructure
> - ✅ Latest models, best quality
> - ❌ HIPAA compliance nightmare - can't send PHI to third parties
> - ❌ Cost scales linearly with volume ($$$)
> - **Verdict: Non-starter due to compliance**
>
> **Option 2: Self-hosted open model (Llama 3)**
> - ✅ Full control, HIPAA compliant
> - ✅ Fixed infrastructure cost
> - ❌ Lower quality than GPT-4
> - ❌ Need GPU infrastructure (expensive upfront)
> - **Verdict: Good for cost at scale, if quality acceptable**
>
> **Option 3: AWS SageMaker with private model**
> - ✅ HIPAA compliant (BAA with AWS)
> - ✅ Managed infrastructure
> - ✅ Can use fine-tuned models
> - ❌ More expensive than self-hosted
> - ❌ Vendor lock-in
> - **Verdict: Best balance for production launch**
>
> **My recommendation:** Start with SageMaker for compliance and speed. Once we hit 10K docs/day, evaluate cost savings of self-hosted."

**See the difference?**
- Senior: Picks a solution
- Staff: Evaluates options, explains trade-offs, recommends with reasoning

---

### **Example 2: Queue Choice**

**Scenario:** Need a message queue for task distribution.

**Bad Answer:**
> "I'll use SQS because it's managed and scales well."

**Good Answer:**
> "For the queue, I'm choosing between SQS and Redis:
>
> **SQS:**
> - ✅ Fully managed, zero infrastructure
> - ✅ Infinite scale
> - ✅ Durable (multi-AZ persistence)
> - ❌ Higher latency (~30-100ms)
> - ❌ At-least-once delivery (need idempotent workers)
> - ❌ No priority queues
>
> **Redis (ElastiCache):**
> - ✅ Lower latency (~1-5ms)
> - ✅ Priority queues, more features
> - ❌ In-memory = data loss on crash
> - ❌ Need to manage failover
> - ❌ Capacity planning required
>
> **Decision:** SQS, because task loss is unacceptable and we can handle the latency. We'll make workers idempotent to handle at-least-once delivery."

---

### **Example 3: Database Choice**

**Bad Answer:**
> "I'll use PostgreSQL because I know it well."

**Good Answer:**
> "For storage, I'm evaluating:
>
> **PostgreSQL (RDS):**
> - ✅ ACID guarantees, strong consistency
> - ✅ Complex queries, joins
> - ✅ Familiar SQL
> - ❌ Vertical scaling limits
> - ❌ More expensive at massive scale
>
> **DynamoDB:**
> - ✅ Infinite horizontal scale
> - ✅ Lower latency for key-value access
> - ✅ Pay per request model
> - ❌ Eventual consistency by default
> - ❌ Limited query flexibility
>
> **Decision:** PostgreSQL initially because:
> 1. We need complex queries for reporting
> 2. Scale (25 docs/min) fits single instance
> 3. Can migrate to DynamoDB later if needed
>
> I'll monitor query patterns and shard by customer_id if we hit limits."

---

## Common Failure Patterns (And How to Avoid Them)

### **❌ Mistake 1: Jumping to Solutions**

**What you do:**
> Interviewer: "Design a system to process medical documents."
> You: "I'll use Lambda, SQS, and DynamoDB..."

**What you should do:**
> "Let me start by understanding the requirements. What's the volume of documents we're processing? What's the latency requirement? Are there compliance constraints?"

**Fix:** Force yourself to spend 5-10 minutes on requirements BEFORE designing.

---

### **❌ Mistake 2: Over-Engineering**

**What you do:**
> "I'll set up Kubernetes with 5 microservices, Kafka for event streaming, separate read/write databases, Redis caching layer, Elasticsearch for search..."

**What you should do:**
> "For the initial design, I'll keep it simple: API Gateway → SQS → ECS workers → PostgreSQL. We can add complexity when we see bottlenecks."

**Fix:** Start simple, explain what you'd add later when needed.

---

### **❌ Mistake 3: Not Asking Clarifying Questions**

**What you do:**
> Make assumptions and design based on them

**What you should do:**
> "Before I proceed, can you clarify: Are these documents arriving in real-time or batch? What's our error budget for extraction accuracy?"

**Fix:** Ask questions throughout, not just at the start.

---

### **❌ Mistake 4: Ignoring Operational Concerns**

**What you do:**
> Design the happy path, don't mention monitoring or failures

**What you should do:**
> "For monitoring, I'd track: queue depth, processing latency, error rates, and cost per document. We'd alert on queue depth > 1000 or error rate > 5%."

**Fix:** Proactively mention monitoring, alerting, disaster recovery.

---

### **❌ Mistake 5: Being Vague**

**What you do:**
> "I'll use a database to store results."

**What you should do:**
> "I'll use PostgreSQL with a documents table partitioned by upload_month, with an index on (status, uploaded_at) for efficient polling of pending documents."

**Fix:** Be specific. Say WHY you chose it.

---

## Staff vs Senior: Key Differences

| Aspect | Senior Engineer | Staff Engineer |
|--------|----------------|----------------|
| **Focus** | Technical depth | Technical depth + strategic thinking |
| **Scope** | "How do I build this?" | "Should we build this? What's the ROI?" |
| **Scale** | "This works for our use case" | "This works now and at 10x scale" |
| **Trade-offs** | Picks a solution | Evaluates 3 options, explains trade-offs |
| **Cost** | Rarely mentioned | "This costs $X/month, alternatives cost..." |
| **Ops** | "We'll monitor it" | "CloudWatch dashboard tracking X, Y, Z with alerts on..." |
| **Failures** | Handles when asked | Proactively discusses failure modes |
| **Impact** | "This solves the problem" | "This solves the problem AND unblocks the data team" |

---

## Real Interview Example: Medical Document Processing

Let's walk through a complete interview using everything we've learned.

### **The Question**

> "Design a system to process medical documents at scale. Documents come from various sources and need analysis to extract relevant information."

---

### **Phase 1: Requirements Gathering (You drive this)**

**You ask:**
> "Let me clarify the requirements. Can you elaborate on 'various sources' - are we receiving via API pushes, or pulling from external systems?"

**Interviewer:**
> "Mix of both - some partners push via API, and we pull batches from S3."

**You ask:**
> "What's the expected volume? Current and projected?"

**Interviewer:**
> "Currently 100K docs/month, expecting 1M/month in a year."

**You ask:**
> "What's the quality of these documents? Clean PDFs or varied formats?"

**Interviewer:**
> "Mix - some clean PDFs, some scanned images, faxes, even handwritten notes."

**You ask:**
> "For the extraction - are we using an external LLM or building in-house?"

**Interviewer:**
> "We'd like your thoughts on that as part of the design."

**You ask:**
> "Any compliance requirements? These are medical documents..."

**Interviewer:**
> "Yes, HIPAA compliant. Good catch."

**You ask:**
> "What's our latency requirement? Real-time or batch is fine?"

**Interviewer:**
> "Batch is fine - results within 1 hour is acceptable."

---

### **Phase 2: Quick Estimation**

**You say:**
> "Let me do some quick math:
> - 1M docs/month = ~33K/day = ~1,400/hour at peak
> - At 2MB average: 1M × 2MB = 2TB/month storage
> - Processing: If each doc takes 30 seconds (OCR + LLM), we need ~12 workers running in parallel at peak
> - This shapes my architecture - we need async processing with auto-scaling workers."

---

### **Phase 3: Architecture Design**

**You draw and explain:**

> "Here's my high-level design:
>
> **Ingestion Layer:**
> - API Gateway for partner uploads
> - S3 + EventBridge for batch ingestion
> - Both write to SQS queue (standard, not FIFO - we don't need ordering)
>
> **Processing Layer:**
> - ECS Fargate workers pulling from SQS
> - Auto-scaling based on queue depth (target: queue age < 5 min)
> - Workers are idempotent (handle duplicate processing)
>
> **Extraction Pipeline:**
> - Step 1: Document classification (is it a lab report? prescription?)
> - Step 2: OCR using AWS Textract (handles handwriting better than open-source)
> - Step 3: LLM extraction using SageMaker with a HIPAA-compliant model
>
> **Storage:**
> - Raw documents: S3 with versioning
> - Processing metadata: PostgreSQL (RDS)
> - Extracted data: PostgreSQL (same instance initially)
>
> **Monitoring:**
> - CloudWatch for queue depth, processing latency, error rates
> - Dead letter queue for failed documents
> - SNS alerts when error rate > 5%"

---

### **Phase 4: Deep Dive - LLM Choice (They probe)**

**Interviewer asks:**
> "Walk me through your decision on the LLM component. Why not use OpenAI?"

**You answer:**
> "Great question. This is actually the most critical trade-off in the system.
>
> **OpenAI API:**
> - Would be fastest to implement
> - Best quality (GPT-4)
> - But: HIPAA compliance is a dealbreaker. We can't send PHI to a third party without a BAA, and OpenAI's terms don't allow medical data
> - Cost: At 1M docs/month, assuming 2K tokens per doc, that's ~$4K-8K/month ongoing
>
> **Self-hosted open model (Llama 3.1 70B):**
> - HIPAA compliant - everything on our infrastructure
> - Fixed cost - ~$2K/month for GPU instances
> - But: Quality is ~80% of GPT-4, need to benchmark on our data
> - Also: We own the ops burden - model updates, scaling, monitoring
>
> **AWS SageMaker with Bedrock or private endpoint:**
> - HIPAA compliant (AWS has BAA)
> - Managed infrastructure
> - Can fine-tune on our medical data
> - Cost: ~$3K-5K/month, scales with usage
> - Faster to production than self-hosted
>
> **My recommendation:**
> Start with SageMaker for speed to market and compliance. Once we validate the business value and hit 10M docs/month, we can justify the engineering investment in self-hosted to cut costs by 60%."

**Interviewer:**
> "What about the at-least-once delivery with SQS? How do you handle that?"

**You answer:**
> "Good catch. SQS gives at-least-once delivery, so documents might process multiple times.
>
> **Mitigation:**
> - Generate a deterministic document_id from S3 key or upload metadata
> - Workers check if document_id exists in DB before processing
> - If exists and status = 'completed', skip and delete message
> - If exists and status = 'failed', retry processing
> - Use database transactions to ensure atomicity
>
> **Alternative I considered:**
> SQS FIFO queues give exactly-once, but:
> - Limited to 300 TPS (we need ~400 at peak)
> - More expensive
> - Harder to scale workers
> - Not worth it since idempotency is straightforward here"

---

### **Phase 5: Scaling Questions**

**Interviewer:**
> "What happens when you hit 10x scale - 10M docs/month?"

**You answer:**
> "At 10M/month, we'd be processing ~14K docs/hour peak. Here's what breaks and how I'd fix it:
>
> **1. Database becomes bottleneck:**
> - Current: Single PostgreSQL instance
> - Fix: Partition by upload_month, add read replicas
> - Consider: Move extracted data to DynamoDB (faster writes, infinite scale)
>
> **2. Textract API limits:**
> - Current: Textract has soft limits
> - Fix: Request limit increase from AWS, add retry backoff
> - Consider: Hybrid - Textract for complex docs, open-source OCR (Tesseract) for simple text
>
> **3. Cost becomes significant:**
> - Current: ~$10K/month all-in
> - At 10x: ~$60K/month (LLM costs dominate)
> - Fix: This justifies self-hosted LLM investment, saves ~$35K/month
>
> **4. Worker scaling speed:**
> - Current: Fargate cold starts take 60s
> - Fix: Maintain warm pool of 10 workers, use Lambda for quick bursts
>
> I'd also add:
> - Regional failover (multi-region S3 replication)
> - Dedicated VPC endpoints to reduce NAT gateway costs
> - Spot instances for workers (70% cost savings, we can handle interruptions)"

---

## How to Practice

### **1. Mock Interviews (Use /mock-interview command)**

Run realistic mock interviews with the system. It will:
- Give you vague problems (like real interviews)
- Force you to drive requirements gathering
- Probe your decisions with follow-up questions
- Provide feedback on your performance

### **2. Study These Real Systems**

Design these from scratch using the REAADS framework:

**Easy:**
- URL shortener (bit.ly)
- Pastebin
- Rate limiter

**Medium:**
- Distributed cache (Redis)
- Task queue (Celery/SQS)
- Image storage service (Imgur)

**Hard:**
- Notification service (Push/Email/SMS at scale)
- Real-time analytics pipeline
- ML model serving infrastructure
- Video streaming platform (Netflix/YouTube)

**For Trajector specifically:**
- Medical document OCR pipeline (we just did this!)
- ML training orchestration system
- Real-time model inference API
- Data pipeline for compliance reporting

### **3. Record Yourself**

- Pick a problem
- Record yourself designing it out loud
- Watch the recording - did you:
  - Ask clarifying questions?
  - Explain trade-offs?
  - Think about failures?
  - Mention monitoring/cost?

### **4. Read System Design Content**

**Books:**
- "System Design Interview" by Alex Xu
- "Designing Data-Intensive Applications" by Martin Kleppmann

**Blogs:**
- High Scalability (highscalability.com)
- AWS Architecture Blog
- Netflix Tech Blog
- Uber Engineering Blog

**YouTube:**
- Gaurav Sen (System Design)
- Success in Tech (System Design Interview)

### **5. AWS Service Deep-Dives**

For AWS-heavy roles like Trajector, know these cold:

**Compute:**
- EC2 vs ECS vs Lambda vs Fargate (when each?)
- Auto Scaling Groups configuration

**Storage:**
- S3 (storage classes, lifecycle policies)
- EBS vs EFS (when each?)

**Database:**
- RDS (Multi-AZ, read replicas)
- DynamoDB (partition keys, GSIs)
- Aurora (when vs RDS?)

**Queue/Stream:**
- SQS (standard vs FIFO, visibility timeout)
- SNS (fan-out pattern)
- Kinesis (vs SQS, when?)

**ML Services:**
- SageMaker (training, inference endpoints)
- Bedrock (vs SageMaker)
- Textract (OCR)

**Monitoring:**
- CloudWatch (metrics, logs, alarms)
- X-Ray (distributed tracing)

---

## Interview Day Checklist

### **30 Minutes Before**

- [ ] Review the job description and company tech stack
- [ ] Have pen and paper ready (draw as you talk)
- [ ] Water nearby
- [ ] Close all other tabs/apps
- [ ] Take 5 deep breaths

### **First 5 Minutes**

- [ ] Listen carefully to the problem
- [ ] Repeat it back to confirm understanding
- [ ] Ask if there's anything specific they want you to focus on
- [ ] Start with clarifying questions (don't jump to solution)

### **During the Interview**

- [ ] Think out loud - they want to hear your process
- [ ] Draw diagrams - visual helps both you and them
- [ ] Ask for feedback: "Does this make sense so far?"
- [ ] State assumptions: "I'm assuming X, let me know if wrong"
- [ ] Explain trade-offs for every major decision
- [ ] Check time periodically - don't spend 30 min on one thing

### **When Stuck**

- [ ] Don't panic - think out loud about what you're considering
- [ ] Ask for a hint: "I'm thinking through X vs Y, any guidance?"
- [ ] Start simple, add complexity later
- [ ] Talk about what you'd research if you had time

### **Last 5 Minutes**

- [ ] Summarize your design
- [ ] Mention what you'd improve with more time
- [ ] Ask about their system: "How do you actually handle this?"
- [ ] Thank them for their time

---

## Key Takeaways

### **The Formula for Staff-Level Success**

1. **Drive the conversation** - You're leading, not following
2. **Ask smart questions** - Show you understand the problem space
3. **Think in trade-offs** - Every decision has pros/cons
4. **Be specific** - "PostgreSQL with read replicas" not "a database"
5. **Explain WHY** - "I chose X because Y, considering Z"
6. **Consider operations** - Monitoring, alerting, cost, failures
7. **Think beyond the tech** - Team impact, timelines, ROI

### **What Staff Engineers Do Differently**

**Senior says:** "This works"
**Staff says:** "This works NOW, scales to 10x, costs $X/month, and unblocks the analytics team"

**Senior says:** "I'll use PostgreSQL"
**Staff says:** "PostgreSQL for complex queries, DynamoDB for high-write workload, Redis for caching - here's why each"

**Senior says:** "We need monitoring"
**Staff says:** "CloudWatch dashboard tracking queue depth (alert > 1000), error rate (alert > 5%), cost per document, with runbooks for common failures"

### **Remember**

You already know how to build systems. This interview is about demonstrating:
- **Strategic thinking**: Why this approach vs others?
- **Production maturity**: What could go wrong?
- **Communication**: Can you explain complex ideas clearly?
- **Leadership**: Can you drive technical decisions?

**You've got this.** Use the framework, think out loud, and show them how you reason about systems.

---

## Additional Resources

**System Design Primers:**
- [System Design Primer on GitHub](https://github.com/donnemartin/system-design-primer)
- [Grokking the System Design Interview](https://www.educative.io/courses/grokking-the-system-design-interview)

**AWS Resources:**
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Architecture Center](https://aws.amazon.com/architecture/)

**Practice Problems:**
- [LeetCode System Design](https://leetcode.com/discuss/interview-question/system-design)
- [Pramp (Free Mock Interviews)](https://www.pramp.com/)

---

**Version:** 1.0
**Last Updated:** February 2026
**For:** Staff Engineer Interview Preparation (Trajector & similar roles)
