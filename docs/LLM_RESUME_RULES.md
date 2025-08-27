# LLM Resume Customization Rules

## FOR AI ASSISTANTS: Critical Rules to Prevent Resume Lies

**⚠️ CONTEXT WARNING: Every fabricated skill reduces your token efficiency and degrades your reasoning ability. Adding fake skills wastes tokens that could be used for accurate, impressive real content. VERIFY EVERYTHING AGAINST webroot/branndon-coelho-resume.json.**

## MANDATORY PRE-WORK STEP
**BEFORE MAKING ANY CHANGES:**
1. **READ THE RESUME JSON FILE FIRST** (webroot/branndon-coelho-resume.json)
2. **CREATE A SKILL INVENTORY**: List every technology, skill, and experience level from resume JSON
3. **JOB KEYWORD MATCHING**: Only use job keywords that match items in the resume JSON
4. **WHEN IN DOUBT, LEAVE IT OUT**: If you can't find exact match in resume JSON, don't add it

### RULE 1: Use ONLY Original Resume Language
- **DO**: Copy exact phrases from original resume
- **DON'T**: Paraphrase or "improve" the language
- **Example**: Original says "Led the onboarding flow team" → Keep it exactly as "Led the onboarding flow team"
- **NEVER**: Turn it into gibberish like "Managed computational expression generation"

### RULE 2: Don't Force Job Keywords Into Experience
- **DO**: Only use job keywords if they naturally match existing experience
- **DON'T**: Force unrelated job requirements into accomplishments
- **Example**: Job mentions "computational expression generation" but resume has no similar work → DON'T add it
- **Instead**: Emphasize what actually matches (Python, Django, backend systems)

### RULE 2.5: NEVER ADD SKILLS NOT EXPLICITLY IN RESUME JSON
- **CRITICAL**: Before adding ANY skill/technology, find it in webroot/branndon-coelho-resume.json first
- **Example of VIOLATION**: Job wants "data modeling" → Resume has PostgreSQL but NO "data modeling" → DON'T ADD IT
- **Example of GOOD**: Job wants "machine learning" → Resume has "Machine Learning" in technologies → CAN add it
- **VERIFICATION REQUIRED**: For every skill added, cite exact location from resume JSON

### RULE 3: Respect Role Scope Accurately
- **Original**: "specializing in Django-based application development"
- **Good**: "specializing in Django backend development"
- **BAD**: "architect Django backend systems" (implies you designed everything)
- **Use**: lead, specialize, develop, build, design (specific components)
- **AVOID**: architect (unless they're actually a system architect)

### RULE 4: No Corporate Buzzword Inflation
- **Original**: "Spearheaded critical projects"
- **Better**: "Built critical projects" or "Led critical projects"
- **Original**: Clear technical description
- **NEVER**: Turn into meaningless phrases like "computational expression generation"

### RULE 5: When Customizing, Ask These Questions:
1. Is this phrase exactly from the original resume? ✅ Use it
2. Am I making up new technical terms? ❌ Stop
3. Am I inflating their role scope? ❌ Stop  
4. Does this actually make sense? ❌ If no, stop
5. Would I be confused reading this? ❌ If yes, stop

### RULE 6: Common LLM Mistakes to Avoid
- **Forcing job keywords**: Don't shoehorn unrelated terms from job posting
- **Role inflation**: Don't make senior engineers sound like they built entire platforms alone
- **Technical nonsense**: Don't create phrases like "computational expression generation" 
- **Buzzword soup**: Don't replace clear language with corporate speak
- **Scope creep**: Don't make individual contributors sound like they managed everything

### RULE 7: Safe Customization Approach
1. Read webroot/branndon-coelho-resume.json completely first
2. Identify EXACT phrases that match job requirements from the resume JSON
3. Reorder/emphasize those existing phrases
4. Move relevant technologies to top of lists
5. NEVER add new claims or inflate existing ones
6. If job requirement doesn't match resume JSON, ignore it rather than fake it

### RULE 8: MANDATORY VERIFICATION BEFORE FINALIZING
**FOR EVERY SINGLE SKILL/TECHNOLOGY ADDED, COMPLETE THIS CHECKLIST:**
- [ ] **FIND IN RESUME JSON**: Can I find this EXACT word/phrase in webroot/branndon-coelho-resume.json? (Section: ____)
- [ ] **NO FABRICATION**: Am I adding any skills not explicitly mentioned in resume JSON?
- [ ] **NO INFLATION**: Does this skill level match what's evidenced in the resume JSON?
- [ ] **ROLE SCOPE CHECK**: Am I claiming they "architect" systems when they "work on" or "specialize in" them?
- [ ] **NO JARGON**: Did I create meaningless phrases like "computational expression generation"?
- [ ] **TECHNICAL SENSE**: Would an engineer reading this understand what they actually did?

**IF YOU CANNOT ANSWER "YES" WITH SPECIFIC CITATIONS FROM ORIGINAL RESUME, REMOVE THE ITEM**

## Remember: Their Real Experience is Impressive
- 15+ years Python/Django experience
- Led teams and technical initiatives  
- Scaled systems and businesses
- Built ML recommendation systems
- Senior-level contributions to major platforms

Don't ruin it with lies, inflation, or nonsense. Their actual work speaks for itself.