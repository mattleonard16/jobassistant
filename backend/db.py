"""Database configuration and utilities."""
from __future__ import annotations

import os
import uuid

from sqlalchemy import create_engine, text
from sqlmodel import SQLModel, Field, Session
from pgvector.sqlalchemy import Vector

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/app"
)

# Synchronous engine for simplicity; switch to async later if needed.
engine = create_engine(DATABASE_URL, echo=False)


class BaseModel(SQLModel):
    """Shared config for ORM models."""

    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False
    )


class Company(BaseModel, table=True):
    __tablename__ = "companies"

    name: str
    careers_url: str


class Job(BaseModel, table=True):
    __tablename__ = "jobs"

    company_id: uuid.UUID | None = Field(foreign_key="companies.id", index=True)
    title: str
    location: str | None = None
    url: str | None = None
    description: str | None = None
    posted_date: str | None = None  # ISO date string
    embedding: list[float] | None = Field(
        sa_column_kwargs={"nullable": True},
        sa_column=Vector(1536),
        default=None,
    )


class Resume(BaseModel, table=True):
    __tablename__ = "resume"

    raw_text: str
    embedding: list[float] | None = Field(
        sa_column_kwargs={"nullable": True},
        sa_column=Vector(1536),
        default=None,
    )


class Match(BaseModel, table=True):
    __tablename__ = "matches"

    job_id: uuid.UUID | None = Field(foreign_key="jobs.id", nullable=False, index=True)
    score: float | None = None
    explanation: dict | None = None


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------

def init_db() -> None:
    """Create pgvector extension if needed and generate tables."""
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:  # Dependency for FastAPI
    with Session(engine) as session:
        yield session