"""Routes for triggering scraping tasks."""
from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, HttpUrl
from sqlmodel import Session, select

from backend.db import Company, get_session
from backend.tasks import scrape_company

router = APIRouter(prefix="/scrape", tags=["Scrape"])


class ScrapeRequest(BaseModel):
    careers_url: HttpUrl
    name: str | None = None


@router.post("/trigger", status_code=status.HTTP_202_ACCEPTED)
def trigger_scrape(req: ScrapeRequest, session: Session = Depends(get_session)):
    """Add/update company row and enqueue scraping task."""

    stmt = select(Company).where(Company.careers_url == str(req.careers_url))
    company = session.exec(stmt).first()
    if company is None:
        company = Company(
            id=uuid.uuid4(), name=req.name or req.careers_url.host, careers_url=str(req.careers_url)
        )
        session.add(company)
        session.commit()
        session.refresh(company)
    else:
        if req.name:
            company.name = req.name
            session.add(company)
            session.commit()

    task = scrape_company.delay(str(company.id))
    return {"task_id": task.id, "company_id": str(company.id)}