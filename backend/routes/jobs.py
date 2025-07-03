"""Job listing and generation routes."""
from __future__ import annotations

import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session
from sqlalchemy import text

from backend.db import get_session, Job, Company, Resume
from backend.generation import generate_application_text

router = APIRouter(prefix="/jobs", tags=["Jobs"])


class JobOut(BaseModel):
    id: uuid.UUID
    title: str
    company: str | None = None
    location: str | None = None
    url: str | None = None
    posted_date: str | None = None
    score: float | None = None


@router.get("/", response_model=List[JobOut])
def list_jobs(session: Session = Depends(get_session)):
    """Return jobs ordered by similarity with résumé embedding."""
    resume_row: Resume | None = session.query(Resume).first()
    if resume_row is None or resume_row.embedding is None:
        # Resume not uploaded yet; return latest jobs with score None
        rows = (
            session.query(Job, Company)
            .join(Company, Company.id == Job.company_id)
            .order_by(Job.posted_date.desc())
            .limit(50)
            .all()
        )
        return [
            JobOut(
                id=job.id,
                title=job.title,
                company=company.name,
                location=job.location,
                url=job.url,
                posted_date=job.posted_date,
                score=None,
            )
            for job, company in rows
        ]

    # Use raw SQL to compute cosine similarity via pgvector <=> operator
    sql = text(
        """
        SELECT j.id, j.title, j.location, j.url, j.posted_date,
               c.name AS company,
               (1 - (j.embedding <=> :resume_embedding)) AS score
        FROM jobs j
        JOIN companies c ON c.id = j.company_id
        ORDER BY score DESC NULLS LAST
        LIMIT 100;
        """
    )
    rows = session.execute(sql, {"resume_embedding": resume_row.embedding}).mappings().all()
    return [JobOut(**row) for row in rows]


class GenerationOut(BaseModel):
    bullets: str  # Markdown list
    cover_letter: str


@router.post("/generate/{job_id}", response_model=GenerationOut)
async def generate_application(job_id: uuid.UUID, session: Session = Depends(get_session)):
    resume_row: Resume | None = session.query(Resume).first()
    if resume_row is None:
        raise HTTPException(status_code=400, detail="Upload résumé first")

    job: Job | None = session.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    company: Company | None = session.get(Company, job.company_id) if job.company_id else None

    result = generate_application_text(resume_row.raw_text, job.description or "", company.name if company else "the company")

    return GenerationOut(**result)