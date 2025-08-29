# ATS Resume Section Limits (2-3 Page Target)

## Overview
To ensure job application resumes stay within 2-3 pages, follow these strict limits when customizing the ATS template.

## Section Limits

### Professional Summary
- **Limit**: 2-3 sentences maximum
- **Focus**: Most relevant experience + key technologies for the role
- **Example**: "Senior Software Engineer with 15+ years Python/Django experience specializing in scalable backend systems. Led technical initiatives scaling startups from $4M to $40M revenue while maintaining high-performance applications."

### About Section
- **Descriptions**: Maximum 3 paragraphs
- **Length**: 2-3 sentences each
- **Focus**: 
  - Paragraph 1: Most relevant experience and quantified achievements
  - Paragraph 2: Current role and technologies matching job requirements
  - Paragraph 3: Business impact and team scaling

### Experience Section
- **Positions**: Maximum 3 positions (current + 2 most relevant previous)
- **Descriptions**: Maximum 3 bullet points per position (2-3 for space)
- **Achievements**: Maximum 3 bullet points per position
- **Technologies**: 
  - Current role: Maximum 10 technologies
  - Previous role: Maximum 8 technologies
- **Priority Order**: Most relevant to job requirements first

### Sections to Remove for ATS Version
- **Fun Facts Section**: Remove entirely (not relevant for ATS)
- **Recommendations Section**: Keep

## Content Guidelines

### Position Titles
- **PRESERVE career progression** - Never flatten Lead/Architect/Principal titles to "Senior" just for keyword matching
- **Emphasize relevant aspects** within truthful titles while maintaining seniority level
- **Show growth trajectory** - Leadership titles demonstrate capability and advancement
- **GOOD Example**: "Application Architect / Lead Developer / Senior Developer" → Keep full title (shows career progression at company)
- **ACCEPTABLE**: "Senior Software Engineer" → "Senior Python Developer" (if Python is primary requirement)
- **NEVER**: "Application Architect / Lead Developer / Senior Developer" → "Senior Software Engineer" (this completely erases 7 years of career growth and leadership experience)

### Technology Lists
- **Prioritize**: Technologies from job posting first
- **Group**: Related technologies together
- **Limit**: Use only technologies from original resume
- **Order**: Most relevant to least relevant

### ATS Keyword Optimization
- **Bold Key Job Keywords**: Use `<strong>` HTML tags around exact keywords from job posting
- **Target Sections**: Professional Summary and About descriptions
- **Keywords to Prioritize**: 
  - Exact job title (e.g., `<strong>Senior Software Engineer</strong>`)
  - Primary technologies (e.g., `<strong>Python backend systems</strong>`)
  - Key requirements (e.g., `<strong>PostgreSQL</strong>`, `<strong>AI development tools</strong>`)
  - Work environment (e.g., `<strong>remote collaboration</strong>`, `<strong>complex SaaS environments</strong>`)
- **Natural Integration**: Keywords must flow naturally in sentences
- **Avoid Keyword Stuffing**: Maximum 8-10 bolded phrases per section

### Achievement Metrics
- **Always Include**: Specific numbers from original resume
- **Examples**: 
  - "2.7 seconds to 0.89 seconds" (performance)
  - "$4M to $40M" (business impact)
  - "10 to 100+ employees" (scaling)

## Template Structure
Use `docs/templates/resume-ats-template.json` as starting point:

```bash
# Copy template
cp docs/templates/resume-ats-template.json job-search/[Company-Role]/resume-branndon-coelho-[company]-ats.json

# Customize using MultiEdit

# Generate PDF (IMPORTANT: Always delete ATS file after PDF generation)
cp job-search/[Company-Role]/resume-branndon-coelho-[company]-ats.json webroot/branndon-coelho-resume-ats.json

# Check if server is running and start if needed
if curl -s http://localhost:8000 | grep -q "resume-wrapper"; then
    echo "Using existing server on port 8000"
else
    echo "Starting server on port 8001"
    cd webroot && python3 -m http.server 8001 &
    sleep 2
    SERVER_URL="http://localhost:8001"
fi

# Generate PDF (use port 8001 if we started it, otherwise default 8000)
poetry run python scripts/generate_resume_pdf.py --mode ats --output job-search/[Company-Role]/resume.pdf ${SERVER_URL:+--url $SERVER_URL}
rm webroot/branndon-coelho-resume-ats.json  # CRITICAL: Always delete after use
```

**SAFETY**: The ATS JSON file is gitignored to prevent accidental commits if you forget to delete it.

## Quality Checklist

Before generating PDF:
- [ ] Professional summary under 3 sentences
- [ ] Only 2 experience positions shown
- [ ] Maximum 3 achievements per position
- [ ] Technology lists prioritized by job requirements
- [ ] All content truthful to original resume
- [ ] Recommendations and Fun Facts sections removed
- [ ] Total expected length: 2-3 pages when rendered

## Page Length Estimation
- **Page 1**: Header, Summary, About (partial)
- **Page 2**: About (completion), Experience (current role)
- **Page 3**: Experience (previous role), Skills

If content exceeds 3 pages, reduce:
1. Remove technologies with least matches to job posting
2. Remove achievements with least relevance to job requirements
3. Shorten description bullet points that don't match job keywords
4. Condense summary to 2 sentences