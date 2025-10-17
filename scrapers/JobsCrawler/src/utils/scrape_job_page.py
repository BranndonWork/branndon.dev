"""
Scrape individual 4dayweek.io job pages to extract additional metadata not available in the API.
"""

import aiohttp
from bs4 import BeautifulSoup
from src.utils.logger_helper import get_custom_logger

logger = get_custom_logger(__name__)


async def scrape_location_restriction(session: aiohttp.ClientSession, job_url: str) -> str | None:
    """
    Scrape a 4dayweek.io job page to extract location restriction warnings.

    Args:
        session: aiohttp client session
        job_url: Full URL to the job posting

    Returns:
        Location restriction text if found, None otherwise
        Example: "New York, USA" or "Newcastle, UK"
    """
    try:
        async with session.get(job_url) as response:
            if response.status != 200:
                logger.warning(f"Failed to fetch {job_url}: HTTP {response.status}")
                return None

            html = await response.text()
            soup = BeautifulSoup(html, 'lxml')

            main_container = soup.select_one('.main-container-wrapper .hero-left')
            if not main_container:
                logger.debug(f"No main container found for {job_url}")
                return None

            apply_warning = main_container.select_one('p.apply-warning')
            if not apply_warning:
                return None

            warning_text = apply_warning.get_text(strip=True)

            if "Only considering candidates eligible to work in" in warning_text:
                strong_tag = apply_warning.select_one('strong')
                if strong_tag:
                    location = strong_tag.get_text(strip=True)
                    logger.info(f"Location restriction found for {job_url}: {location}")
                    return location

            return None

    except Exception as e:
        logger.error(f"Error scraping {job_url}: {str(e)}")
        return None


async def scrape_job_metadata(session: aiohttp.ClientSession, job_url: str) -> dict:
    """
    Scrape a 4dayweek.io job page to extract all additional metadata.

    Args:
        session: aiohttp client session
        job_url: Full URL to the job posting

    Returns:
        Dictionary with extracted metadata:
        {
            'location_restriction': str | None,
            'posted_date': str | None,
            'pto_days': str | None,
        }
    """
    metadata = {
        'location_restriction': None,
        'posted_date': None,
        'pto_days': None,
    }

    try:
        async with session.get(job_url) as response:
            if response.status != 200:
                logger.warning(f"Failed to fetch {job_url}: HTTP {response.status}")
                return metadata

            html = await response.text()
            soup = BeautifulSoup(html, 'lxml')

            main_container = soup.select_one('.main-container-wrapper')
            if not main_container:
                return metadata

            apply_warning = main_container.select_one('.hero-left p.apply-warning')
            if apply_warning:
                warning_text = apply_warning.get_text(strip=True)
                if "Only considering candidates eligible to work in" in warning_text:
                    strong_tag = apply_warning.select_one('strong')
                    if strong_tag:
                        metadata['location_restriction'] = strong_tag.get_text(strip=True)

            posted = main_container.select_one('.job-posted')
            if posted:
                metadata['posted_date'] = posted.get_text(strip=True).replace('Posted ', '')

            pto_tag = main_container.select_one('.job-tags li.reduced-hours')
            if pto_tag:
                metadata['pto_days'] = pto_tag.get_text(strip=True)

        return metadata

    except Exception as e:
        logger.error(f"Error scraping metadata from {job_url}: {str(e)}")
        return metadata
