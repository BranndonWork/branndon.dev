import asyncio
import os
from collections.abc import Coroutine
from typing import Any

from src.crawler import AsyncCrawlerEngine
# IMPORTANT: Embedding functionality disabled - DO NOT DELETE, may be re-enabled later
# from src.embeddings.embed_latest_crawled_data import embed_data
from src.models import ApiArgs, Bs4Args, RssArgs
from src.utils.logger_helper import get_custom_logger

# SQLite database path - no longer using PostgreSQL URL
DB_PATH = os.environ.get("DB_PATH", "data/jobs.db")

logger = get_custom_logger(__name__)

async def run_strategy(args: RssArgs | ApiArgs | Bs4Args) -> Coroutine[Any, Any, None] | None:
    engine = AsyncCrawlerEngine(args)
    await engine.run()

async def run_crawlers(is_test: bool = False) -> Coroutine[Any, Any, None] | None:
    start_time = asyncio.get_event_loop().time()

    strategies = [
        (RssArgs(test=is_test)),
        (ApiArgs(test=is_test)),
        (Bs4Args(test=is_test)),
    ]

    tasks = [run_strategy(args) for args in strategies]

    try:
        await asyncio.gather(*tasks)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)

    elapsed_time = asyncio.get_event_loop().time() - start_time
    logger.info(f"All strategies completed in {elapsed_time:.2f} seconds")

async def main():
    logger.info("Running all the crawlers...")

    # Run crawlers and wait for them to complete
    await run_crawlers()

    # IMPORTANT: Embedding disabled - DO NOT DELETE, may be re-enabled later
    # This requires PyTorch, transformers, and pgvector (~5GB of dependencies)
    # await asyncio.to_thread(embed_data, embedding_model="e5_base_v2")

    logger.info("Crawling completed successfully. Embeddings disabled.")


if __name__ == "__main__":
	asyncio.run(main())