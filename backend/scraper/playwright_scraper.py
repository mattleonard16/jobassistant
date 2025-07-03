"""Generic job scraper using Playwright.

Currently supports simple list-style career pages (e.g., Lever, Greenhouse).
Returns a list of dictionaries with the fields expected by DB layer.

Usage (sync):
    from backend.scraper.playwright_scraper import fetch_jobs_sync
    jobs = fetch_jobs_sync("https://boards.greenhouse.io/mycompany")
"""
from __future__ import annotations

import asyncio
import re
from datetime import datetime
from typing import List, Dict

from playwright.async_api import async_playwright

# ---------------------------------------------------------------------------
# Scraping helpers
# ---------------------------------------------------------------------------

JOB_LINK_PATTERNS = [
    re.compile(r"/jobs/\\d"),  # Lever style /jobs/1234567
    re.compile(r"/job\-details/"),  # generic
    re.compile(r"/positions/"),
]


async def _scrape_jobs(url: str) -> List[Dict]:
    """Open the careers URL and try to collect job postings."""
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        await page.wait_for_load_state("networkidle")

        anchors = await page.eval_on_selector_all(
            "a[href]",
            "(els) => els.map(el => ({href: el.href, text: el.textContent.trim()}))",
        )

        jobs: List[Dict] = []
        for a in anchors:
            href: str = a["href"]
            text: str = a["text"]
            if not text or len(text) < 3:
                continue
            if any(pat.search(href) for pat in JOB_LINK_PATTERNS):
                jobs.append({"url": href, "title": text})

        # Deduplicate by URL
        unique = {j["url"]: j for j in jobs}.values()

        # Attempt to enrich each posting by visiting page (lightweight)
        results: List[Dict] = []
        for j in unique:
            try:
                await page.goto(j["url"], timeout=60000)
                await page.wait_for_load_state("domcontentloaded")
                jd_html = await page.content()
                # Strip HTML tags crude
                jd_text = re.sub(r"<[^>]+>", " ", jd_html)
                jd_text = re.sub(r"\s+", " ", jd_text)
                results.append(
                    {
                        "title": j["title"],
                        "url": j["url"],
                        "description": jd_text[:4000],  # truncate
                        "posted_date": datetime.utcnow().date().isoformat(),
                    }
                )
            except Exception:
                continue  # skip bad postings

        await browser.close()
        return results


def fetch_jobs_sync(url: str) -> List[Dict]:
    """Blocking wrapper around async scrape."""
    return asyncio.run(_scrape_jobs(url))