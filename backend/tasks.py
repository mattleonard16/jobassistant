"""Celery tasks for the application."""
from __future__ import annotations

import logging
import uuid

from sqlmodel import Session, select

from backend.celery_app import celery_app
from backend.db import engine, Company, Job
from backend.embeddings import embed_text
from backend.scraper.playwright_scraper import fetch_jobs_sync

logger = logging.getLogger(__name__)


@celery_app.task
def scrape_company(company_id: str):
    """Scrape jobs for a single company row."""
    with Session(engine) as session:
        company = session.get(Company, uuid.UUID(company_id))
        if not company:
            logger.error("Company %s not found", company_id)
            return 0
        jobs_data = fetch_jobs_sync(company.careers_url)
        inserted = 0
        for jd in jobs_data:
            # Upsert by url
            stmt = select(Job).where(Job.url == jd["url"])
            existing = session.exec(stmt).first()
            if existing:
                continue  # skip duplicates for now
            embedding = embed_text(jd["description"])
            job = Job(
                company_id=company.id,
                title=jd["title"],
                url=jd["url"],
                description=jd["description"],
                posted_date=jd.get("posted_date"),
                embedding=embedding,
            )
            session.add(job)
            inserted += 1
        session.commit()
        logger.info("Scraped %d new jobs for %s", inserted, company.name)
        return inserted


@celery_app.task
def scrape_all_companies():
    """Periodic job to scrape all companies."""
    with Session(engine) as session:
        ids = [str(c.id) for c in session.exec(select(Company.id))]
    for cid in ids:
        scrape_company.delay(cid)  # schedule subtask
    return len(ids)


# Beat schedule
celery_app.conf.beat_schedule = {
    "scrape-every-6-hours": {
        "task": "backend.tasks.scrape_all_companies",
        "schedule": 60 * 60 * 6,
    }
}