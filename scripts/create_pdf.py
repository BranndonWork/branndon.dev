import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors

# New output file path with a unique name to avoid conflicts
output_file = "./docs/Branndon_Coelho_Resume_v1.pdf"
scrits_dir = os.path.dirname(os.path.abspath(__file__))
abs_output_file = os.path.join(scrits_dir, output_file)

# Create document
doc = SimpleDocTemplate(output_file, pagesize=LETTER, rightMargin=40, leftMargin=40, topMargin=30, bottomMargin=30)
styles = getSampleStyleSheet()

# Custom styles
header_style = ParagraphStyle("Header", parent=styles["Heading1"], fontSize=16, alignment=TA_CENTER, spaceAfter=10)
subheader_style = ParagraphStyle(
    "SubHeader", parent=styles["Heading2"], fontSize=11, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor("#333333")
)
body_style = ParagraphStyle("Body", parent=styles["Normal"], fontSize=10, leading=13, alignment=TA_LEFT, spaceAfter=6)
skill_style = ParagraphStyle(
    "Skill", parent=styles["Normal"], fontSize=10, leading=12, alignment=TA_LEFT, textColor=colors.HexColor("#333333")
)

# Elements container
elements = []

# Header
elements.append(Paragraph("Branndon Coelho", header_style))
elements.append(Paragraph("Senior Software Engineer | Application Architect | Technical Lead", styles["Normal"]))
elements.append(
    Paragraph(
        "📧 resume@branndon.dev | 🌐 branndon.dev | 💼 LinkedIn: branndon.dev/linkedin | 💻 GitHub: github.com/BranndonWork",
        styles["Normal"],
    )
)
elements.append(Spacer(1, 12))

# Professional Summary
elements.append(Paragraph("Professional Summary", subheader_style))
summary_text = """
Senior software engineer with 15+ years of experience building scalable, secure, and high-performing applications. Hands-on leader skilled in Python, Django, AWS, and DevOps, with a track record of driving performance improvements, mentoring teams, and delivering business-critical systems. Adept at balancing clean architecture with practical execution in fast-paced, high-growth environments.
"""
elements.append(Paragraph(summary_text, body_style))

# Core Skills
elements.append(Paragraph("Core Skills & Tools", subheader_style))
skills_text = """
<b>Backend:</b> Python, Django, Flask, Node.js, REST APIs<br/>
<b>Frontend:</b> JavaScript, React.js, HTML/CSS<br/>
<b>Cloud & DevOps:</b> AWS (EC2, S3, RDS, Lambda, API Gateway), Docker, CI/CD, Cloudflare<br/>
<b>Other:</b> Git/GitHub, Agile/Scrum, WordPress, TDD, Automation
"""
elements.append(Paragraph(skills_text, skill_style))

# Professional Experience
elements.append(Paragraph("Professional Experience", subheader_style))

# Headspace
elements.append(Paragraph("<b>Headspace</b> – Senior Software Engineer", body_style))
elements.append(Paragraph("Aug 2022 – Present", styles["Italic"]))
headspace_text = """
- Architect and maintain Django-based applications with focus on scalability, security, and performance.<br/>
- Implement CI/CD pipelines to accelerate delivery and improve reliability.<br/>
- Mentor junior engineers and lead code reviews to enforce best practices.<br/>
- Partner with cross-functional teams to deliver business-aligned features.<br/>
<b>Key Tech:</b> Django, Docker, Auth0, Braze, REST APIs, CI/CD, TDD, Agile
"""
elements.append(Paragraph(headspace_text, body_style))

# Webley Systems
elements.append(Paragraph("<b>Webley Systems</b> – Senior Software Engineer (Backend)", body_style))
elements.append(Paragraph("2020 – 2021", styles["Italic"]))
webley_text = """
- Designed and deployed Flask-based APIs integrated with AWS services for streaming video.<br/>
- Automated 20-year-old manual ticketing process via custom tooling, improving efficiency and reducing errors.<br/>
- Practiced TDD and built comprehensive tests across new and legacy systems.<br/>
<b>Key Tech:</b> Python, Flask, AWS (Lambda, API Gateway, S3, EC2), Selenium, React
"""
elements.append(Paragraph(webley_text, body_style))

# Penny Hoarder
elements.append(Paragraph("<b>The Penny Hoarder</b> – Application Architect / Lead Developer / Senior Developer", body_style))
elements.append(Paragraph("2014 – 2020", styles["Italic"]))
tph_text = """
- Scaled engineering from startup to enterprise (10 → 100+ staff, $4M → $40M revenue).<br/>
- Reduced site load time from 2.7s → 0.89s, driving measurable revenue impact.<br/>
- Designed ML-based email recommendation system.<br/>
- Led weekly code reviews, mentored developers, and partnered with executives on technology roadmap.<br/>
<b>Key Tech:</b> Python, Django, WordPress, JavaScript, PHP, AWS, Docker, Redis, MySQL, Postgres, Vue.js
"""
elements.append(Paragraph(tph_text, body_style))

# Strengths
elements.append(Paragraph("Strengths & Recognition", subheader_style))
strengths_text = """
- Known for mentorship, adaptability, and delivering reliable systems under pressure.<br/>
- CliftonStrengths: Strategic, Activator, Individualization, Achiever, Adaptability.
"""
elements.append(Paragraph(strengths_text, body_style))

# Build PDF
doc.build(elements)
output_file
