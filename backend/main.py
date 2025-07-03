from fastapi import FastAPI
from backend.db import init_db
from backend.routes import resume as resume_router
from backend.routes import scrape as scrape_router
from backend.routes import jobs as jobs_router

app = FastAPI(title="AI Job-App Assistant")


@app.get("/health", tags=["Misc"])
async def health() -> dict[str, str]:
    """Simple liveness probe."""
    return {"status": "ok"}


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(resume_router.router)
app.include_router(scrape_router.router)
app.include_router(jobs_router.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)