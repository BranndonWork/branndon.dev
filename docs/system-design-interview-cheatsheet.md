# System Design Interview Cheat Sheet

**For Staff-Level A&D Interviews | Print This**

---

## The Framework (5 Steps)

1. **Clarify** (5 min) - Ask questions, don't assume
2. **Estimate** (2 min) - Quick math to justify scale
3. **Design** (15 min) - Draw boxes, explain flow
4. **Deep Dive** (15 min) - They probe, you explain trade-offs
5. **Wrap Up** (5 min) - Summarize, mention improvements

---

## What They Want to Hear

### When Asked About LLMs/AI for Sensitive Data
**They want:** Compliance thinking, not just tech
**Say:** "Medical data means HIPAA. Can't use OpenAI - no BAA. I'd use SageMaker or self-hosted for compliance, then optimize cost later."

### When Asked "Why X Over Y?"
**They want:** Trade-off analysis, not just a pick
**Say:** "X gives us [benefit] but costs [trade-off]. Y is better for [scenario]. Given our constraints, X wins because [reason]."

### When Asked About Scale
**They want:** Numbers, not "it scales"
**Say:** "At 1M docs/month, that's ~25/min peak. Each takes 30s processing, so we need ~12 workers in parallel."

### When Asked About Failures
**They want:** Production mindset
**Say:** "If the worker crashes mid-task, SQS visibility timeout returns it to queue. Workers are idempotent - they check if already processed before starting."

### When Asked About Monitoring
**They want:** Specific metrics, not "CloudWatch"
**Say:** "I'd track queue depth (alert >1000), error rate (alert >5%), processing latency p95, and cost per document."

---

## AWS Services: When to Use Each

### Compute
| Service | Use When | Avoid When |
|---------|----------|------------|
| **EC2** | Need full control, long-running, specific hardware | Simple workloads, variable traffic |
| **ECS/Fargate** | Containerized apps, auto-scaling workers | Very short tasks (<15min) |
| **Lambda** | Short tasks (<15min), event-driven, variable load | Long-running, high memory needs |

**Interview tip:** "Fargate for workers - no EC2 management, auto-scales on queue depth, pay only when processing."

### Queue/Messaging
| Service | Use When | Avoid When |
|---------|----------|------------|
| **SQS** | Task queues, decoupling, durability needed | Need real-time, <10ms latency |
| **SNS** | Fan-out to multiple subscribers, notifications | Point-to-point messaging |
| **Kinesis** | Real-time streaming, replay needed, ordering | Simple task queues |

**Interview tip:** "SQS over Redis for task queues - durable, managed, handles at-least-once with idempotent workers."

### Database
| Service | Use When | Avoid When |
|---------|----------|------------|
| **RDS/PostgreSQL** | Complex queries, ACID, joins needed | Massive write throughput |
| **DynamoDB** | Key-value access, infinite scale, simple queries | Complex joins, ad-hoc queries |
| **Aurora** | MySQL/Postgres at higher scale, multi-region | Simple use cases (overkill) |

**Interview tip:** "PostgreSQL for complex queries. If we hit scale limits, shard by customer_id or move hot paths to DynamoDB."

### Storage
| Service | Use When | Avoid When |
|---------|----------|------------|
| **S3** | Objects, backups, data lake, any size | Filesystem needs, low-latency |
| **EBS** | Block storage for EC2, databases | Shared access across instances |
| **EFS** | Shared filesystem across instances | Single instance, cost-sensitive |

### Cache
| Service | Use When | Avoid When |
|---------|----------|------------|
| **ElastiCache Redis** | Caching, sessions, need data structures | Simple cache, cost-sensitive |
| **ElastiCache Memcached** | Simple caching, multi-threaded | Persistence needed, complex types |

**Interview tip:** "Redis for caching, but NOT for task queues in production - in-memory means data loss on crash. SQS for durability."

---

## Common Probing Questions & Answers

**Q: "What if this crashes mid-processing?"**
A: "SQS visibility timeout returns message to queue. Worker checks idempotency key before processing. Worst case: duplicate work, not data loss."

**Q: "How do you handle 10x traffic?"**
A: "Auto-scale workers on queue depth. Database: add read replicas or partition. Cache hot data. Monitor costs - might need architecture changes at 100x."

**Q: "Why not just use [simpler solution]?"**
A: "Good point - start simple, add complexity when needed. [Simpler] works until [specific scale/requirement]. I'd start there, then migrate."

**Q: "What's the most expensive part?"**
A: "LLM inference. At scale, I'd evaluate self-hosted models - 60% cost savings vs managed, but adds ops burden."

**Q: "How do you ensure exactly-once processing?"**
A: "True exactly-once is hard. Use idempotency: hash document content as key, check DB before processing. At-least-once + idempotent = effectively exactly-once."

---

## Trade-Off Patterns (Use These Phrases)

### The Structure
> "For [decision], I'm choosing between [A] and [B].
> [A] gives us [benefit] but [drawback].
> [B] gives us [benefit] but [drawback].
> Given [constraint], I'd go with [choice] because [reason]."

### Quick Examples

**Queue:** "SQS for durability over Redis for speed - task loss is unacceptable"

**Compute:** "Fargate over Lambda - tasks run >15min, need consistent performance"

**Database:** "PostgreSQL over DynamoDB - need complex queries for reporting"

**LLM:** "SageMaker over OpenAI - HIPAA compliance, can't send PHI externally"

---

## Red Flags to Avoid

❌ Jumping to solution without asking questions
❌ "I'll use a database" (too vague - WHICH one and WHY)
❌ Ignoring compliance/security (especially for medical data)
❌ No mention of monitoring or failure handling
❌ "It scales" without explaining HOW
❌ Picking tech because "I know it" vs "it fits the requirements"

---

## Staff vs Senior: The Difference

| Senior Says | Staff Says |
|-------------|------------|
| "I'll use SQS" | "SQS for durability, workers are idempotent for at-least-once delivery" |
| "We need monitoring" | "CloudWatch tracking queue depth, error rate, latency p95" |
| "This scales" | "At 10x, we'd need to shard the DB by customer_id" |
| "I'd use PostgreSQL" | "PostgreSQL for joins, but might move to DynamoDB if writes exceed 10K/sec" |

---

## Day-Of Reminders

- [ ] **First 5 min:** Ask clarifying questions (scale, latency, compliance)
- [ ] **Think out loud** - they want your reasoning process
- [ ] **Draw as you talk** - boxes and arrows help
- [ ] **Say "trade-off"** - shows staff-level thinking
- [ ] **Mention monitoring** - production mindset
- [ ] **Be specific** - "PostgreSQL with index on (status, created_at)" not "a database"
