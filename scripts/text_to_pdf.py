#!/usr/bin/env python3
"""
Simple script to convert text files to PDF using reportlab
Usage: python text_to_pdf.py input.txt output.pdf
"""

import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def text_to_pdf(input_file, output_file):
    """Convert a text file to PDF"""

    # Read the text file
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text_content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return False

    # Create PDF document
    doc = SimpleDocTemplate(output_file, pagesize=letter, rightMargin=inch, leftMargin=inch, topMargin=inch, bottomMargin=inch)

    # Get styles
    styles = getSampleStyleSheet()
    story = []

    # Split text into paragraphs and convert each to PDF
    paragraphs = text_content.split("\n\n")

    for para_text in paragraphs:
        if para_text.strip():
            # Replace line breaks with <br/> tags for reportlab
            formatted_text = para_text.strip().replace("\n", "<br/>")
            story.append(Paragraph(formatted_text, styles["Normal"]))
            story.append(Spacer(1, 12))

    # Build PDF
    try:
        doc.build(story)
        print(f"PDF created successfully: {output_file}")
        return True
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python text_to_pdf.py input.txt output.pdf")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not Path(input_file).exists():
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)

    success = text_to_pdf(input_file, output_file)
    sys.exit(0 if success else 1)
