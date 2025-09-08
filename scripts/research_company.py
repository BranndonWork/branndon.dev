#!/usr/bin/env python3
"""
Company Research Automation
Automated company research using web scraping and search.
"""

import asyncio
import argparse
import os
import sys
from pathlib import Path
from datetime import datetime
import json
import re
import subprocess


class CompanyResearcher:
    def __init__(self, output_dir: str = None):
        """Initialize company researcher."""
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.script_dir = Path(__file__).parent
    
    def search_company_reviews(self, company_name: str) -> dict:
        """Search for company reviews and information."""
        search_queries = [
            f'"{company_name}" employee reviews glassdoor',
            f'"{company_name}" indeed company reviews',
            f'"{company_name}" company culture reddit',
            f'"{company_name}" glassdoor'
        ]
        
        results = {}
        
        print(f"Searching for company reviews: {company_name}")
        
        for query in search_queries:
            print(f"  Searching: {query}")
            try:
                # Use the WebSearch functionality (this would be replaced with actual web search)
                # For now, we'll create a placeholder that shows what should be searched
                results[query] = {
                    "query": query,
                    "status": "pending_search",
                    "note": "Manual search required - use WebSearch tool"
                }
            except Exception as e:
                print(f"    Error searching {query}: {e}")
                results[query] = {"error": str(e)}
        
        return results
    
    def scrape_company_page(self, url: str, company_name: str) -> str:
        """Scrape a specific company page using playwright_scraper."""
        try:
            # Use the existing playwright_scraper.py
            scraper_path = self.script_dir / "playwright_scraper.py"
            if not scraper_path.exists():
                raise FileNotFoundError("playwright_scraper.py not found")
            
            # Run the playwright scraper with generic filename
            if "indeed.com" in url:
                output_file = self.output_dir / "indeed-reviews.txt"
            else:
                output_file = self.output_dir / "company-research.txt"
                
            cmd = [
                sys.executable, str(scraper_path),
                url,
                "--no-links",
                "--output", str(output_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Successfully scraped {url}")
                if output_file.exists():
                    return output_file.read_text()
                return "Content saved to file"
            else:
                print(f"Error scraping {url}: {result.stderr}")
                return f"Scraping failed: {result.stderr}"
        
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return f"Scraping error: {e}"
    
    def analyze_company_reviews(self, review_content: str, company_name: str) -> dict:
        """Analyze company review content and extract key insights."""
        analysis = {
            "company": company_name,
            "analyzed_at": datetime.now().isoformat(),
            "insights": {
                "pros": [],
                "cons": [],
                "red_flags": [],
                "culture": [],
                "work_life_balance": [],
                "compensation": []
            },
            "raw_content_length": len(review_content)
        }
        
        # Basic keyword analysis
        content_lower = review_content.lower()
        
        # Look for common positive indicators
        positive_keywords = [
            "great culture", "excellent benefits", "work life balance", 
            "supportive management", "learning opportunities", "flexible"
        ]
        
        # Look for red flags
        negative_keywords = [
            "toxic", "overwork", "burnout", "poor management", 
            "layoffs", "underpaid", "no work life balance"
        ]
        
        for keyword in positive_keywords:
            if keyword in content_lower:
                analysis["insights"]["pros"].append(f"Mentions: {keyword}")
        
        for keyword in negative_keywords:
            if keyword in content_lower:
                analysis["insights"]["red_flags"].append(f"Mentions: {keyword}")
        
        # Try to extract ratings if present (basic regex)
        rating_matches = re.findall(r'(\\d\\.\\d)\\s*(?:out of|/|star)', content_lower)
        if rating_matches:
            analysis["insights"]["ratings"] = rating_matches[:3]  # First 3 ratings found
        
        return analysis
    
    def generate_research_report(self, company_name: str, search_results: dict, 
                               scraped_content: dict = None) -> str:
        """Generate a comprehensive research report."""
        report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# Company Research Report: {company_name}

**Generated**: {report_date}
**Researcher**: Automated Company Research Tool

## Search Queries Performed

"""
        
        for query, result in search_results.items():
            status = result.get("status", "unknown")
            report += f"- **{query}**: {status}\\n"
            if "note" in result:
                report += f"  - Note: {result['note']}\\n"
        
        report += "\\n## Review Analysis\\n\\n"
        
        if scraped_content:
            for site, content in scraped_content.items():
                if isinstance(content, dict) and "insights" in content:
                    insights = content["insights"]
                    report += f"### {site.title()} Analysis\\n\\n"
                    
                    if insights["pros"]:
                        report += "**Positive Mentions:**\\n"
                        for pro in insights["pros"]:
                            report += f"- {pro}\\n"
                        report += "\\n"
                    
                    if insights["red_flags"]:
                        report += "**⚠️ Red Flags:**\\n"
                        for flag in insights["red_flags"]:
                            report += f"- {flag}\\n"
                        report += "\\n"
                    
                    if insights.get("ratings"):
                        report += f"**Ratings Found**: {', '.join(insights['ratings'])}\\n\\n"
        
        report += """## Recommended Actions

1. **Manual Review Required**: This automated report should be supplemented with manual research
2. **Check Recent Reviews**: Focus on reviews from the last 6-12 months
3. **Look for Patterns**: Pay attention to recurring themes in reviews
4. **Verify Information**: Cross-reference information across multiple sources
5. **Consider Department**: Some issues may be department-specific

## Notes

- This is an automated research report
- Manual verification is strongly recommended
- Consider reaching out to current/former employees on LinkedIn
- Check for recent news about the company

---
*Report generated by automated company research tool*
"""
        
        return report
    
    def research_company_full(self, company_name: str, urls: list = None) -> str:
        """Perform full company research workflow."""
        print(f"\\n🔍 Starting research for: {company_name}")
        
        # Step 1: Search for company information
        search_results = self.search_company_reviews(company_name)
        
        # Step 2: Scrape specific URLs if provided
        scraped_content = {}
        if urls:
            for url in urls:
                print(f"\\n📄 Scraping: {url}")
                content = self.scrape_company_page(url, company_name)
                if content and len(content) > 100:  # Only analyze substantial content
                    analysis = self.analyze_company_reviews(content, company_name)
                    scraped_content[url] = analysis
        
        # Step 3: Generate report
        report = self.generate_research_report(company_name, search_results, scraped_content)
        
        # Step 4: Save report to generic filename
        report_file = self.output_dir / "company-research-report.md"
        report_file.write_text(report)
        
        print(f"\\n✅ Research report saved to: {report_file}")
        return str(report_file)


def main():
    parser = argparse.ArgumentParser(description="Research company information and reviews")
    parser.add_argument("company_name", help="Name of the company to research")
    parser.add_argument("--urls", nargs="*", help="Specific URLs to scrape (Glassdoor, Indeed, etc.)")
    parser.add_argument("--output-dir", default=".", help="Output directory for research files")
    
    args = parser.parse_args()
    
    try:
        researcher = CompanyResearcher(args.output_dir)
        report_file = researcher.research_company_full(args.company_name, args.urls)
        
        print(f"\\n📋 Research completed!")
        print(f"Report saved to: {report_file}")
        print(f"\\n💡 Next steps:")
        print("1. Review the generated report")
        print("2. Manually search for additional information")
        print("3. Check for recent company news")
        print("4. Consider reaching out to employees on LinkedIn")
        
    except Exception as e:
        print(f"Error during research: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())