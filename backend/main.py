from fastapi import FastAPI, BackgroundTasks

app = FastAPI(title="AI Job‑App Assistant")

# TODO: wire Postgres (asyncpg or SQLModel) + pgvector
# TODO: mount routers: /jobs, /resume, /generate
# TODO: add CORS for the React dev server

@app.get("/health")
async def health():
    return {"status": "ok"}
