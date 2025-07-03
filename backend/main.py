from fastapi import FastAPI
import os
from backend.db import init_db, get_session
from fastapi import Depends
from sqlmodel import Session

app = FastAPI(title="AI Job-App Assistant")


@app.get("/health", tags=["Misc"])
async def health() -> dict[str, str]:
    """Simple liveness probe."""
    return {"status": "ok"}


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/jobs", tags=["Jobs"])
def list_jobs(session: Session = Depends(get_session)):
    """Temporary endpoint to verify DB connectivity."""
    from backend.db import Job

    jobs = session.query(Job).limit(10).all()
    return jobs


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)