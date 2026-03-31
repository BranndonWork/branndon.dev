# Leadership Interview Answer: Scaling Therapy Matching Algorithm

**Question:** "Tell me about a time where you led a team on an important project, and how did it turn out?"

## STAR Method Response

### Situation

During Mental Health Awareness Month last May, our therapy matching system started experiencing significant performance issues. We were seeing 3x normal traffic, but our matching algorithm was taking 8+ seconds to return therapist recommendations. 23% of users were abandoning the flow.

### Task

I was asked to lead a small team to stabilize the system quickly and figure out a sustainable solution. We had to understand the bottleneck and fix it while the system was under load. We also had to coordinate with the product team because some of the matching logic itself was contributing to the slowdown.

### Action

First, I got the team together and we investigated the matching pipeline to identify exactly where time was being spent. We discovered two main issues: complex database queries that weren't optimized for scale, and the matching algorithm making redundant calculations for each request.

From there, we split the work - I tackled the database optimization, rewriting the Django queries (Used select_related() and prefetch_related() to eliminate N+1 queries) and adding indexes that reduced query time from 6 seconds to under 1 second. Meanwhile, I had another engineer implement a Redis caching layer for therapist availability data.

The tricky part was working with product. The matching criteria included 8+ factors, and each added significant computational complexity. I presented them with data showing which criteria had the biggest performance cost versus user value (Exact timezone matching → broader timezone regions & Highly specific therapeutic approach subcategories → consolidated into main approaches). We agreed to simplify the initial match to 5 core criteria, with the option for users to refine afterward.

### Result

Within two weeks, we got matching time down from 8 seconds to 1.2 seconds average. The system handled peak load for the rest of the month without degradation, and abandonment rates dropped from 23% to 8%.

We also documented the performance characteristics and created a playbook for future load spikes. The architectural improvements are still in place today and have proven valuable for similar issues during subsequent high-traffic periods.
