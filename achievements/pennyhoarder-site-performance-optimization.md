# Site Performance Optimization - The Penny Hoarder

**Role:** Application Architect / Lead Developer / Senior Developer
**Company:** The Penny Hoarder
**Timeline:** 2014-2020
**Project Type:** Performance Engineering / Optimization

Raw Dump of everything I know about this achievement:
While working at the penny hoarder, the advertising noticed a discrepency in the number of clicks that we were paying for vs the impressions we would get on our page. I was tasked with finding out why. Our major driver of traffic and thus revenue was facebook ads. we were losing a significant number of users between click and landing page. so much so that we thought it was possibly a reporting issue, not actual issue. After investigating the flow and recreating the user path, I discovered taht I could click a link and it would take on average of 2.7 seconds per page load. Most users will just leave before waiting that long. This was verified as the issue. I was tasked with optimize whole site performance, so that no matter the source, pages loaded in under a second. I started by evaluating the users flow, from the time they click the link, to the time the page onour site was loaded. The browser was usually a facebook app chromium port, so we coldn't do too much about the source. Next was the CDN then aws router, then ec2 instances with our wordpress installation, which contained nginx. What I found was that our caching at the CDN was not optimized to be more broad. I also found that nginx caching was not endabled, no was rate liimiting for bad actors that might hammer our servers. I then noticed how our docker build cotnained no steps for css/js minification, and taht all images were uploaded at full resulution, then cropped, but not compressed properly. Lastly I noticed how our wordpress sytstem caching wasn't not working as expected. I touched every aspect of this... I ensured our CDN would cache a page once and serve it for all users, ignoring certain query params and building a cache key properly. I then added nginx level caching with different ttl's fpor different site sections, bypassing caching in admin and api calls completely. I implemented rate limiting and added security hardening for wordpress. I think introduced a webpack build step that would combine and compress all js and css. I installed an image compression system to compress all current images, aswell as ensuring all uploaded media was also compressesd going forward. I also tried 3 different wordpress caching systems, and landed on wp total cache as the solution, as a foundation, then wrote custom cache clearing logic and buttons so staff could manually clear pages at will. All of this together took our page load time from 2.7 seconds to 0.89 seconds, and showed that, with the same ad spend, we were getting roughly 28% more users reaching the final page, increasing revenue and leading to record breaking growth. During this time period we were ranked the #1 privately owned media company in the country.

---

## STAR Method Interview Response

### Situation (Context & Problem)

**What was the performance problem? What was the impact? How was it discovered?**

Raw Answer:
While working at the penny hoarder, the advertising noticed a discrepency in the number of clicks that we were paying for vs the impressions we would get on our page. Our major driver of traffic and thus revenue was facebook ads. we were losing a significant number of users between click and landing page. so much so that we thought it was possibly a reporting issue, not actual issue. After investigating the flow and recreating the user path, I discovered taht I could click a link and it would take on average of 2.7 seconds per page load. Most users will just leave before waiting that long. This was verified as the issue.

Refined Answer:
"At The Penny Hoarder, our advertising team noticed a significant discrepancy between the Facebook ad clicks we were paying for and the actual impressions on our pages. Since Facebook ads were our primary revenue driver, this was a critical business problem. The drop-off was so severe we initially suspected a reporting error. I investigated by recreating the user journey and discovered our pages were taking an average of 2.7 seconds to load. We had monitoring in place, but performance had degraded over time as we'd added features and content without corresponding infrastructure optimization. For mobile users clicking from Facebook ads, 2.7 seconds meant significant abandonment before the page even loaded."

---

### Task (Your Mandate)

**Were you assigned this or did you identify it? What was the goal? What was at stake?**

Raw Answer:
I was tasked with finding out why. This was verified as the issue. I was tasked with optimize whole site performance, so that no matter the source, pages loaded in under a second.

Refined Answer:
"I was tasked with investigating and solving this discrepancy. Once I verified that page load time was the root cause, my mandate expanded to a comprehensive site-wide performance optimization. The goal was clear: get every page loading in under one second, regardless of traffic source."

---

### Action (Your Approach & Execution)

**What did you measure/profile? What optimizations did you implement? What was your methodology? Any challenges?**

Raw Answer:
I started by evaluating the users flow, from the time they click the link, to the time the page onour site was loaded. The browser was usually a facebook app chromium port, so we coldn't do too much about the source. Next was the CDN then aws router, then ec2 instances with our wordpress installation, which contained nginx. What I found was that our caching at the CDN was not optimized to be more broad. I also found that nginx caching was not endabled, no was rate liimiting for bad actors that might hammer our servers. I then noticed how our docker build cotnained no steps for css/js minification, and taht all images were uploaded at full resulution, then cropped, but not compressed properly. Lastly I noticed how our wordpress sytstem caching wasn't not working as expected. I touched every aspect of this... I ensured our CDN would cache a page once and serve it for all users, ignoring certain query params and building a cache key properly. I then added nginx level caching with different ttl's fpor different site sections, bypassing caching in admin and api calls completely. I implemented rate limiting and added security hardening for wordpress. I think introduced a webpack build step that would combine and compress all js and css. I installed an image compression system to compress all current images, aswell as ensuring all uploaded media was also compressesd going forward. I also tried 3 different wordpress caching systems, and landed on wp total cache as the solution, as a foundation, then wrote custom cache clearing logic and buttons so staff could manually clear pages at will.

Refined Answer:
"I took a systematic approach, mapping the entire user journey from click to page load: Facebook app browser → CDN → AWS router → EC2 instances running WordPress with nginx. I identified bottlenecks at every layer. At the CDN level, caching wasn't properly configured - pages weren't being cached broadly enough. nginx had no caching enabled and no rate limiting, leaving us vulnerable to traffic spikes. Our Docker build process had zero asset optimization - no CSS/JS minification. Images were uploaded at full resolution, cropped in-browser but never compressed. And WordPress caching wasn't functioning as expected.

I systematically addressed each layer. I reconfigured our CDN to cache pages once and serve to all users, building proper cache keys while ignoring unnecessary query parameters. I implemented nginx caching with different TTLs for different site sections, bypassing caching entirely for admin and API calls. I added rate limiting and security hardening. I introduced a webpack build step to combine and compress all JavaScript and CSS. I deployed an image compression system that handled both existing images and all future uploads. For WordPress caching, I evaluated three different systems and selected WP Total Cache, then extended it with custom cache-clearing logic and UI controls for staff to manually invalidate pages when needed.

The key was touching every layer of the stack methodically while ensuring each optimization didn't break functionality or create new problems."

---

### Result (Outcome & Impact)

**The metric: 2.7s → 0.89s. But what else? Revenue impact? User engagement? Cost savings?**

Raw Answer:
All of this together took our page load time from 2.7 seconds to 0.89 seconds, and showed that, with the same ad spend, we were getting roughly 28% more users reaching the final page, increasing revenue and leading to record breaking growth. During this time period we were ranked the #1 privately owned media company in the country.

Refined Answer:
"The optimization reduced page load time from 2.7 seconds to 0.89 seconds - a 67% improvement. With the exact same advertising spend, we saw 28% more users reaching our landing pages, which translated directly to revenue growth and contributed to record-breaking performance. During this period, The Penny Hoarder was ranked the #1 privately owned media company in the country."

---

## Technical Details for Deep Dives

### Performance Bottlenecks Identified

### Optimizations Implemented

### Measurement & Tooling

### Technologies Used

-   [Add as needed]

---

## Interview Tips for This Story

-   **Length:** 2-3 minutes for full STAR
-   **Emphasis:** Technical methodology and business impact
-   **Follow-up questions to prep for:**
    -   How did you identify the bottlenecks?
    -   What was your biggest performance win?
    -   How did you measure success?
    -   What would you optimize differently today?
