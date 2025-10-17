#!/usr/local/bin/python3
import json
import sqlite3
from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

import aiohttp
import pandas as pd

from config import SKIP_TITLE_KEYWORDS, AUTO_SKIP_REASON
from src.utils.FollowLink import async_follow_link, async_follow_link_echojobs
from src.utils.handy import link_exists_in_db
from src.utils.logger_helper import get_custom_logger

logger = get_custom_logger(__name__)

@dataclass
class ApiElementPath:
    dict_tag: str
    title_tag: str
    link_tag: str
    description_tag: str
    pubdate_tag: str
    location_tag: str
    location_default: str


def clean_postgre_api(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if col == "description":
            if not df[col].empty:  # Check if the column has any rows
                df[col] = df[col].astype(str)  # Convert the entire column to string
                df[col] = df[col].str.replace(
                    r'<.*?>|[{}[\]\'",]', "", regex=True
                )  # Remove html tags & other characters
        elif col == "location":
            if not df[col].empty:  # Check if the column has any rows
                df[col] = df[col].astype(str)  # Convert the entire column to string
                df[col] = df[col].str.replace(
                    r'<.*?>|[{}[\]\'",]', "", regex=True
                )  # Remove html tags & other characters
                # df[col] = df[col].str.replace(r'[{}[\]\'",]', '', regex=True)
                df[col] = df[col].str.replace(
                    r"\b(\w+)\s+\1\b", r"\1", regex=True
                )  # Removes repeated words
                df[col] = df[col].str.replace(
                    r"\d{4}-\d{2}-\d{2}", "", regex=True
                )  # Remove dates in the format "YYYY-MM-DD"
                df[col] = df[col].str.replace(
                    r"(USD|GBP)\d+-\d+/yr", "", regex=True
                )  # Remove USD\d+-\d+/yr or GBP\d+-\d+/yr.
                df[col] = df[col].str.replace("[-/]", " ", regex=True)  # Remove -
                df[col] = df[col].str.replace(
                    r"(?<=[a-z])(?=[A-Z])", " ", regex=True
                )  # Insert space between lowercase and uppercase letters
                pattern = r"(?i)\bRemote Job\b|\bRemote Work\b|\bRemote Office\b|\bRemote Global\b|\bRemote with frequent travel\b"  # Define a regex patter for all outliers that use remote
                df[col] = df[col].str.replace(pattern, "Worldwide", regex=True)
                df[col] = df[col].replace(
                    "(?i)^remote$", "Worldwide", regex=True
                )  # Replace
                df[col] = df[col].str.strip()  # Remove trailing white space

    logger.info("Finished API crawlers. Results below ⬇︎")

    return df

def __class_json_strategy(data, api_config: Any) -> list | dict:
    """

    Given that some JSON requests are either
    dict or list we need to access the 1st dict if
    needed.

    """
    if api_config.class_json == "dict":
        element_path = ApiElementPath(**api_config.elements_path)
        jobs = data[element_path.dict_tag]
        return jobs
    elif api_config.class_json == "list":
        return data
    else:
        raise ValueError("The class json is unknown.")


async def __get_jobs_data(
    cur,
    jobs: dict | list,
    session: aiohttp.ClientSession,
    api_config: Any,
    test: bool = False,
):
    total_jobs_data = {
        "title": [],
        "link": [],
        "description": [],
        "pubdate": [],
        "location": [],
        "timestamp": [],
    }

    element_path = ApiElementPath(**api_config.elements_path)

    for job in jobs:
        # Apply filters if configured
        if api_config.filters:
            # Check is_remote filter
            if "is_remote" in api_config.filters:
                if job.get("is_remote") != api_config.filters["is_remote"]:
                    continue

            # Check description_contains filter (case-insensitive)
            if "description_contains" in api_config.filters:
                description_text = str(job.get(element_path.description_tag, "")).lower()
                search_term = api_config.filters["description_contains"].lower()
                if search_term not in description_text:
                    continue

        title_element = job.get(element_path.title_tag, "NaN")

        title_lower = str(title_element).lower()
        should_skip = any(keyword.lower() in title_lower for keyword in SKIP_TITLE_KEYWORDS)

        if should_skip:
            logger.info(f"Auto-skipping job: {title_element} - matches excluded keyword")
            continue

        link = job.get(element_path.link_tag, "NaN")

        if await link_exists_in_db(
            link=link, cur=cur, test=test
        ):
            logger.debug(
                f"Link {element_path.link_tag} already found in the db. Skipping..."
            )
            continue

        default = job.get(element_path.description_tag, "NaN")
        description = ""
        if api_config.follow_link == "yes":
            if api_config.name == "echojobs.io":
                description = await async_follow_link_echojobs(
                    session=session,
                    url_to_follow=link,
                    selector=api_config.inner_link_tag,
                    default=default,
                )
            else:
                description = await async_follow_link(
                    session=session,
                    followed_link=link,
                    description_final=description,
                    inner_link_tag=api_config.inner_link_tag,
                    default=default,
                )
        else:
            description = default

        today = date.today()

        location = (
            job.get(element_path.location_tag, "NaN") or element_path.location_default
        )

        timestamp = datetime.now()

        for key, value in zip(
            total_jobs_data.keys(),
            [title_element, link, description, today, location, timestamp],
        ):
            total_jobs_data[key].append(value)

    return total_jobs_data


async def async_api_requests(
    fetch_func: Callable[[aiohttp.ClientSession], Coroutine[Any, Any, str]],
    session: aiohttp.ClientSession,
    api_config: Any,
    cur: sqlite3.Cursor,
    test: bool = False,
) -> dict[str, list[str]]:
    rows = {
        key: []
        for key in ["title", "link", "description", "pubdate", "location", "timestamp"]
    }

    logger.info(f"{api_config.name} has started")
    logger.debug(f"All parameters for {api_config.name}:\n{api_config}")

    try:
        response = await fetch_func(session)
        logger.debug(f"Successful request on {api_config.url}")
        data = json.loads(response)
        jobs = __class_json_strategy(data, api_config)

        new_rows = await __get_jobs_data(cur, jobs, session, api_config, test)
        if new_rows:
            for key in rows:
                rows[key].extend(new_rows.get(key, []))
    except Exception as e:
        logger.error(
            f"{type(e).__name__} occurred before deploying crawling strategy on {api_config.url}.\n\n{e}",
            exc_info=True,
        )
        pass
    return rows
