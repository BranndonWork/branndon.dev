#!/usr/bin/env python3
"""
Playwright Web Scraper
A general-purpose script to visit any URL and return content in a format that can be easily ingested.
"""

import asyncio
import argparse
import sys
import logging
from playwright.async_api import async_playwright
import json
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)


async def scrape_url(url: str, wait_time: int = 3, include_links: bool = True, 
                    include_images: bool = False, selector: str = None, javascript_enabled: bool = True) -> dict:
    """
    Scrape a URL and return structured content.
    
    Args:
        url: URL to scrape
        wait_time: Seconds to wait after page load
        include_links: Whether to extract links
        include_images: Whether to extract image URLs
        selector: Optional CSS selector to focus on specific content
    
    Returns:
        Dict with scraped content
    """
    async with async_playwright() as p:
        # Launch browser with anti-detection options
        browser = await p.chromium.launch(
            headless=False,  # Use headed mode to avoid detection
            args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-extensions',
                '--disable-dev-shm-usage',
                '--disable-web-security',
                '--no-first-run'
            ]
        )
        
        # Create context with realistic user agent and extra headers
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1680, 'height': 1050},  # Common 16:10 aspect ratio
            java_script_enabled=javascript_enabled,
            extra_http_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
        )
        
        # Add stealth measures
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            delete navigator.__proto__.webdriver;
        """)
        
        page = await context.new_page()
        
        # Bring window to front
        await page.bring_to_front()
        
        try:
            logging.info(f"Visiting: {url}")
            
            # Navigate to URL with shorter timeout
            logging.info("Loading page...")
            await page.goto(url, wait_until='domcontentloaded', timeout=15000)
            
            # Wait for additional content to load
            logging.info(f"Waiting {wait_time} seconds for content to load...")
            await asyncio.sleep(wait_time)
            
            # Get page title and check for protection screens
            logging.info("Getting page title...")
            title = await page.title()
            logging.info(f"Page title: {title}")
            
            # Check if we hit Cloudflare or similar protection
            if "just a moment" in title.lower() or "checking your browser" in title.lower():
                logging.warning("Detected protection screen, waiting longer...")
                await asyncio.sleep(10)  # Wait longer for protection to pass
                title = await page.title()
                logging.info(f"Updated page title: {title}")
            
            # Get main content
            logging.info("Extracting page content...")
            if selector:
                logging.info(f"Using selector: {selector}")
                content_element = await page.query_selector(selector)
                if content_element:
                    text_content = await content_element.inner_text()
                    html_content = await content_element.inner_html()
                    logging.info(f"Content extracted with selector, length: {len(text_content)}")
                else:
                    text_content = "Selector not found"
                    html_content = "Selector not found"
                    logging.warning(f"Selector '{selector}' not found")
            else:
                text_content = await page.inner_text('body')
                html_content = await page.inner_html('body')
                logging.info(f"Full page content extracted, length: {len(text_content)}")
            
            # Extract links if requested
            links = []
            if include_links:
                logging.info("Extracting links...")
                link_elements = await page.query_selector_all('a[href]')
                for link in link_elements:
                    href = await link.get_attribute('href')
                    text = await link.inner_text()
                    if href and text.strip():
                        links.append({
                            'url': href,
                            'text': text.strip()
                        })
                logging.info(f"Extracted {len(links)} links")
            
            # Extract images if requested
            images = []
            if include_images:
                img_elements = await page.query_selector_all('img[src]')
                for img in img_elements:
                    src = await img.get_attribute('src')
                    alt = await img.get_attribute('alt') or ''
                    if src:
                        images.append({
                            'src': src,
                            'alt': alt.strip()
                        })
            
            # Get page metadata
            logging.info("Getting metadata...")
            meta_description = await page.get_attribute('meta[name="description"]', 'content') or ''
            canonical_url = await page.get_attribute('link[rel="canonical"]', 'href') or url
            logging.info("Scraping completed successfully")
            
            result = {
                'url': url,
                'canonical_url': canonical_url,
                'title': title,
                'meta_description': meta_description,
                'text_content': text_content,
                'html_content': html_content,
                'links': links,
                'images': images,
                'scraped_at': datetime.now().isoformat(),
                'content_length': len(text_content),
                'status': 'success'
            }
            
            return result
            
        except Exception as e:
            logging.error(f"Error scraping {url}: {str(e)}")
            return {
                'url': url,
                'error': str(e),
                'status': 'error',
                'scraped_at': datetime.now().isoformat()
            }
        
        finally:
            await browser.close()


def format_output(data: dict, format_type: str = 'json') -> str:
    """Format the scraped data for output."""
    if format_type == 'json':
        return json.dumps(data, indent=2, ensure_ascii=False)
    elif format_type == 'text':
        if data.get('status') == 'error':
            return f"Error scraping {data['url']}: {data['error']}"
        
        output = []
        output.append(f"URL: {data['url']}")
        output.append(f"Title: {data['title']}")
        output.append(f"Meta Description: {data['meta_description']}")
        output.append(f"Content Length: {data['content_length']} characters")
        output.append(f"Scraped At: {data['scraped_at']}")
        output.append("\n--- TEXT CONTENT ---")
        output.append(data['text_content'])
        
        if data['links']:
            output.append(f"\n--- LINKS ({len(data['links'])}) ---")
            for link in data['links'][:20]:  # Limit to first 20 links
                output.append(f"[{link['text']}] {link['url']}")
        
        return '\n'.join(output)
    else:
        return str(data)


async def main():
    parser = argparse.ArgumentParser(
        description='Scrape any URL with Playwright browser automation',
        epilog='''Examples:
  %(prog)s "https://example.com"
  %(prog)s --wait 5 --no-javascript "https://protected-site.com"
  %(prog)s --format json --output data.json "https://api-docs.com"
  %(prog)s --selector ".reviews" --no-links "https://reviews-site.com"''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('url', help='URL to scrape')
    parser.add_argument('--wait', type=int, default=3, 
                        help='Seconds to wait after page load (default: 3)')
    parser.add_argument('--format', choices=['json', 'text'], default='text', 
                        help='Output format: json for structured data, text for readable (default: text)')
    parser.add_argument('--selector', 
                        help='CSS selector to focus on specific content (e.g., ".reviews", "#main-content")')
    parser.add_argument('--no-links', action='store_true', 
                        help='Don\'t extract links (faster, smaller output)')
    parser.add_argument('--include-images', action='store_true', 
                        help='Extract image URLs and alt text')
    parser.add_argument('--no-javascript', action='store_true', 
                        help='Disable JavaScript - useful when sites block automation or for faster loading')
    parser.add_argument('--output', '-o', 
                        help='Output file path (default: print to stdout)')
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'https://' + args.url
    
    # Scrape the URL
    result = await scrape_url(
        url=args.url,
        wait_time=args.wait,
        include_links=not args.no_links,
        include_images=args.include_images,
        selector=args.selector,
        javascript_enabled=not args.no_javascript
    )
    
    # Format output
    formatted_output = format_output(result, args.format)
    
    # Write to file or print
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(formatted_output)
        print(f"Output written to: {args.output}")
    else:
        print(formatted_output)


if __name__ == '__main__':
    asyncio.run(main())