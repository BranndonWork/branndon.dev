"""
Generate ATS-friendly PDF from resume HTML
"""

import asyncio
import sys
import argparse
from playwright.async_api import async_playwright


async def generate_resume_pdf(url="http://localhost:8000", output="branndon-coelho-resume.pdf", ats_mode=False):
    """Generate PDF from local resume site"""

    # Add ATS mode parameter to URL if requested
    if ats_mode and "?" not in url:
        url += "?mode=ats"
    elif ats_mode:
        url += "&mode=ats"

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(url)
        await page.wait_for_selector(".resume-wrapper")
        await page.wait_for_selector(".resume-header")
        await page.wait_for_timeout(2000)  # Wait for React and data loading

        # ATS-optimized PDF settings
        pdf_options = {
            "path": output,
            "format": "A4",
            "margin": (
                {"top": "0.5in", "right": "0.5in", "bottom": "0.5in", "left": "0.5in"}
                if ats_mode
                else {"top": "0.75in", "right": "0.75in", "bottom": "0.75in", "left": "0.75in"}
            ),
            "print_background": False,
            "prefer_css_page_size": True,
        }

        await page.pdf(**pdf_options)
        await browser.close()

        mode_text = "ATS-optimized" if ats_mode else "standard"
        print(f"{mode_text.capitalize()} PDF generated: {output}")


def main():
    parser = argparse.ArgumentParser(description="Generate PDF from resume website")
    parser.add_argument("--url", default="http://localhost:8000", help="Resume website URL")
    parser.add_argument("--output", default="branndon-coelho-resume.pdf", help="Output PDF filename")
    parser.add_argument("--mode", choices=["full", "ats"], default="full", help="Resume mode: full or ats")

    args = parser.parse_args()

    # Determine output filename if not specified
    if args.output == "branndon-coelho-resume.pdf" and args.mode == "ats":
        args.output = "branndon-coelho-resume-ats.pdf"

    ats_mode = args.mode == "ats"
    asyncio.run(generate_resume_pdf(args.url, args.output, ats_mode))


if __name__ == "__main__":
    main()
