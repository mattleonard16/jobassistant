"""Resume-related API endpoints."""
from __future__ import annotations

import io
import uuid
from typing import Annotated

import pdfplumber
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlmodel import Session

from backend.db import Resume, get_session
from backend.embeddings import embed_text

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
def upload_resume(
    file: Annotated[UploadFile, File(description="PDF or TXT résumé file")],
    session: Session = Depends(get_session),
):
    """Accept a résumé file (PDF or plaintext), extract text, generate embedding, and save."""

    if file.content_type not in {
        "application/pdf",
        "text/plain",
        "application/octet-stream",  # some browsers label .txt as octet-stream
    }:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    try:
        # Read file bytes
        raw_bytes = file.file.read()

        if file.content_type == "application/pdf" or file.filename.endswith(".pdf"):
            with pdfplumber.open(io.BytesIO(raw_bytes)) as pdf:
                pages_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            text_content = pages_text.strip()
        else:
            text_content = raw_bytes.decode("utf-8", errors="ignore")

        if not text_content:
            raise ValueError("No extractable text found")

        # Generate embedding
        embedding = embed_text(text_content)

        # Upsert single résumé (assumes single-user app). Replace existing row.
        existing = session.query(Resume).first()
        if existing:
            existing.raw_text = text_content
            existing.embedding = embedding
            session.add(existing)
        else:
            session.add(
                Resume(id=uuid.uuid4(), raw_text=text_content, embedding=embedding)
            )
        session.commit()
        return {"message": "Résumé stored"}

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc