# Resume Generation Complete Workflow

**⚠️ STOP: This document is SELF-CONTAINED. Do not reference other docs. Everything needed is here.**

## Pre-Flight Checklist
Before proceeding, confirm you understand:
- [ ] Template location: `docs/resume-ats-template.json`
- [ ] Skills source: Only from Engineer Profile section below
- [ ] #1 Rule: NEVER fabricate skills or experience
- [ ] Workflow: Read ALL sections before starting

## Critical Rules (Memorize These First)

### The Golden Rule
**NEVER FABRICATE SKILLS, EXPERIENCE, OR ACHIEVEMENTS**
- Only reorganize and emphasize existing content
- If a job requirement doesn't match the Engineer Profile below, ignore it
- When in doubt, leave it out

### LLM-Specific Rules
1. **Use ONLY language from Engineer Profile below** - Don't paraphrase or create new terms
2. **Don't force job keywords** - Only use them if they naturally match existing experience
3. **Respect role scope** - Use "lead", "specialize", "develop" not "architect" unless actually an architect
4. **No buzzword inflation** - Keep technical descriptions clear and accurate
5. **Verify everything** - For every skill added, it must exist in Engineer Profile section below

## Complete Engineer Profile (Source of Truth)

### Overview
- **Years of Experience**: 15+ years (2007 - Present)
- **Current Role**: Senior Software Engineer at Headspace
- **Specialization**: Backend Development, Python, Django, Scalable Systems

### Technical Skills Inventory (ONLY use these)

#### Programming Languages
- **Python** (Strong - 95%) - Primary language, 10+ years
- **JavaScript** (Very Strong - 96%) - Full-stack development
- **TypeScript** (Learning) - Used in SDUI project at Headspace
- **PHP** (Experienced) - WordPress, legacy systems
- **HTML/CSS** (Very Strong - 99%) - Frontend development
- **SQL** (Experienced) - PostgreSQL, MySQL

#### Backend Technologies
- **Django** (Very Strong - 90%) - Primary framework at Headspace
- **Flask** (Proficient) - RESTful APIs at Webley Systems
- **Node.js** (Very Strong - 90%) - Backend services
- **Backend Development** - General backend architecture and design
- **RESTful APIs** - Design and implementation
- **ORM** - Django ORM, SQLAlchemy
- **Software Architecture** - System design, scalability

#### Databases
- **PostgreSQL** - Production use at The Penny Hoarder
- **MySQL** - WordPress, various projects
- **Redis** - Caching, session management
- **AWS RDS** - Managed database services
- **AWS Aurora** - Scalable database solutions
- **Database Management** - Queries, optimization (not schema design focus)

#### Cloud & Infrastructure
- **AWS EC2**, **Lambda**, **S3**, **API Gateway**, **Route53**, **CloudFront**, **Code Pipeline**
- **Cloudflare** - CDN, security
- **Docker** (Strong - 85%) - Containerization
- **Linux** (Good - 85%) - Server management
- **Nginx** - Web server configuration

#### AI/ML & Data
- **Machine Learning Implementation** - Built ML-based email recommendation system
- **AI Development Tools** - Claude Code, Cursor, ChatGPT, Google Gemini
- **Data Processing** - Large dataset handling, ETL pipelines
- **Computational Systems** - Complex algorithmic solutions

#### Development Practices
- **TDD**, **CI/CD**, **Git** (Very Strong - 95%)
- **Agile Methodologies** - Scrum, Kanban
- **Code Review** - Led weekly reviews at TPH
- **Mentoring** - Junior developer guidance
- **Remote Collaboration** - Async communication, distributed teams

#### Authentication & Security
- **JWT**, **Auth0**, **GDPR Compliance**, **Data Anonymization**

#### Tools & Platforms
- **WordPress** (Very Strong - 80%), **Braze**, **Jira**, **Confluence**
- **Selenium** - Automation, testing

#### Specialized Knowledge
- **Performance Optimization** - 2.7s to 0.89s at TPH
- **Scaling Systems** - $4M to $40M revenue growth support
- **DevOps** (Strong - 90%), **Automation** (Strong - 95%)

### Key Projects & Achievements

1. **Machine Learning Email Recommendation System** (The Penny Hoarder)
   - Designed and built entire system using Python
   - Personalized content delivery at scale

2. **Server-Driven UI Initiative** (Headspace)
   - TypeScript, Django, React Native
   - Led onboarding flow team, ensured GDPR compliance

3. **Platform Performance Optimization** (The Penny Hoarder)
   - 2.7 seconds → 0.89 seconds load time
   - Cloudflare, AWS, caching strategies

4. **SMS Consent Architecture Migration** (Headspace)
   - Braze API integration, data migration
   - Project lead role

### Work History

1. **Headspace** (2022-Present) - Senior Software Engineer
2. **The Penny Hoarder** (2015-2022) - Application Architect / Lead Developer / Senior Developer
3. **Webley Systems** (2020-2021) - Senior Software Engineer - Backend Focus

### Work Contexts
- **Startup Experience**: The Penny Hoarder ($4M→$40M scaling, 10→100+ employees)
- **Enterprise Experience**: Headspace (millions of users globally)
- **Remote Work**: Fully remote at Headspace and Webley Systems
- **Leadership**: Led onboarding flow team, SMS consent migration, weekly code reviews

## Step-by-Step Workflow

### Step 1: Validate Prerequisites
```bash
# Check job directory exists
ls ./job-search/[Company-JobTitle]/

# Verify job-posting.md exists
cat ./job-search/[Company-JobTitle]/job-posting.md
```

### Step 2: Copy Template (NOT another resume)
```bash
# CRITICAL: Copy from template, not from another job's resume
cp docs/resume-ats-template.json ./job-search/[Company-JobTitle]/resume-branndon-coelho-[company]-ats.json
```

### Step 3: Create Missing Files
Copy these from example directory:
- `application-tracking.md`
- `interview-prep.md`

Create new based on job:
- `cover-letter.txt`
- `customization-analysis.md`

### Step 4: Analyze Job Requirements
Read job-posting.md and identify:
- Required skills that match Engineer Profile above
- Years of experience needed
- Technology stack mentioned
- Keywords to emphasize

### Step 5: Customize Resume Using MultiEdit

#### What to Customize:
1. **Positions array**: Fill in relevant role titles
2. **Summary**: 2-3 sentences with bolded keywords from job
3. **About descriptions**: 3 paragraphs emphasizing relevant experience
4. **Experience sections**: 
   - Keep original position titles (preserve career progression)
   - Customize descriptions to emphasize relevant work
   - Reorder technologies to match job requirements
   - Maximum 3 positions total

#### ATS Keyword Optimization:
- Bold key job keywords using `<strong>` tags
- Target: job title, primary technologies, key requirements
- Natural integration only - no keyword stuffing
- Maximum 8-10 bolded phrases per section

### Step 6: Generate PDF
```bash
# Copy to webroot
cp job-search/[Company-JobTitle]/resume-branndon-coelho-[company]-ats.json webroot/branndon-coelho-resume-ats.json

# Check if server is running
if curl -s http://localhost:8000 | grep -q "resume-wrapper"; then
    SERVER_URL="http://localhost:8000"
else
    # Start server on port 8001
    cd webroot && python3 -m http.server 8001 &
    sleep 2
    SERVER_URL="http://localhost:8001"
fi

# Generate PDF
poetry run python scripts/generate_resume_pdf.py --mode ats --output job-search/[Company-JobTitle]/resume.pdf --url $SERVER_URL

# CRITICAL: Delete ATS file immediately
rm webroot/branndon-coelho-resume-ats.json
```

### Step 7: Verify Output
- Confirm PDF was generated
- Provide file:// links to resume.pdf and cover-letter.txt
- List final directory contents

## Section Limits (2-3 Page Target)

### Professional Summary
- **Limit**: 2-3 sentences maximum
- **Focus**: Most relevant experience + key technologies

### About Section  
- **Descriptions**: Maximum 3 paragraphs, 2-3 sentences each
- **Paragraph 1**: Most relevant experience
- **Paragraph 2**: Current role and matching technologies
- **Paragraph 3**: Business impact and scaling

### Experience Section
- **Positions**: Maximum 3 (current + 2 most relevant)
- **Descriptions**: Maximum 3 bullet points per position
- **Achievements**: Maximum 3 bullet points per position
- **Technologies**: 10 for current, 8 for previous roles

### Sections to Remove
- **Fun Facts Section**: Remove entirely for ATS
- **Recommendations Section**: Keep (shows credibility)

## Quality Assurance Checklist

### Before Starting
- [ ] Read this ENTIRE document first
- [ ] Located template at `docs/resume-ats-template.json`
- [ ] Identified job requirements from job-posting.md
- [ ] Mapped requirements to Engineer Profile skills above

### During Customization
- [ ] Every skill exists in Engineer Profile above
- [ ] Using exact language from Engineer Profile
- [ ] Not forcing unmatched job keywords
- [ ] Preserving career progression titles
- [ ] Keeping descriptions truthful

### After Generation
- [ ] PDF generated successfully
- [ ] Total length 2-3 pages
- [ ] All content truthful to original experience
- [ ] Provided file:// verification links

## Common Mistakes to Avoid

1. **Copying another job's resume instead of template**
2. **Adding skills not in Engineer Profile**
3. **Inflating role scope** (architect vs developer)
4. **Creating technical nonsense** phrases
5. **Forgetting to delete ATS file from webroot**
6. **Not reading job-posting.md first**
7. **Skipping this document and referencing others**

---
*This document contains EVERYTHING needed for resume generation. Do not reference other docs.*