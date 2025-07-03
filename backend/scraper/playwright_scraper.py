"""Headless Playwright scraper.

Run with:
    python -m backend.scraper.playwright_scraper --url <careers_page>

Cursor TODOs:
* paginate career site
* extract job postings (id, title, location, description, url)
* return JSON / write directly to Postgres
* respect robots.txt + rate‑limits
"""
import asyncio, json, argparse
from pathlib import Path
# from playwright.async_api import async_playwright

async def scrape(url: str):
    # TODO: implement scraper logic
    raise NotImplementedError

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()
    asyncio.run(scrape(args.url))
