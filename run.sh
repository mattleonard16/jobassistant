#!/usr/bin/env bash
# AI Job‑App Assistant ‑ MVP scaffolding script
# ------------------------------------------------------------
# Run this from the repo root:
#   $ chmod +x scaffold.sh && ./scaffold.sh
# It will create a minimal FastAPI + React + Postgres project
# structure with stub files full of TODO markers so you can
# let Cursor generate the rest.
# ------------------------------------------------------------
set -euo pipefail

# --- directory tree ---------------------------------------------------------
mkdir -p ai-job-app/{backend/{scraper,models,__init__.py},frontend/src/components} \
         ai-job-app/db 2>/dev/null || true

# --- backend ---------------------------------------------------------------
cat > ai-job-app/backend/main.py <<'PY'
from fastapi import FastAPI, BackgroundTasks

app = FastAPI(title="AI Job‑App Assistant")

# TODO: wire Postgres (asyncpg or SQLModel) + pgvector
# TODO: mount routers: /jobs, /resume, /generate
# TODO: add CORS for the React dev server

@app.get("/health")
async def health():
    return {"status": "ok"}
PY

cat > ai-job-app/backend/models/__init__.py <<'PY'
"""Pydantic / SQLModel domain objects

Cursor TODOs:
* JobInDB(id, title, description, embedding, …)
* Resume(id, raw_text, embedding)
* Match(job_id, score, explanation)
* Generation(job_id, bullets, cover_letter)
"""
PY

cat > ai-job-app/backend/scraper/playwright_scraper.py <<'PY'
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
PY

cat > ai-job-app/backend/requirements.txt <<'REQ'
fastapi
uvicorn[standard]
openai
playwright
asyncpg
pgvector
python-dotenv
REQ

# --- frontend --------------------------------------------------------------
cat > ai-job-app/frontend/src/App.tsx <<'TSX'
import { useEffect, useState } from "react";
import JobTable from "./components/JobTable";

function App() {
  const [jobs, setJobs] = useState([]);

  // TODO: fetch jobs from `/jobs` endpoint and store in state
  useEffect(() => {
    // fetchJobs();
  }, []);

  return (
    <div className="p-6 font-sans">
      <h1 className="text-2xl font-bold mb-4">AI Job‑App Assistant</h1>
      {/* TODO: add Upload Résumé button + status */}
      <JobTable jobs={jobs} />
    </div>
  );
}
export default App;
TSX

cat > ai-job-app/frontend/src/components/JobTable.tsx <<'TSX'
interface Props { jobs: any[] }
export default function JobTable({ jobs }: Props) {
  // TODO: render rows with match % badge + Generate button
  return (
    <table className="w-full text-left border-collapse">
      <thead>
        <tr>
          <th className="border-b py-2">Title</th>
          <th className="border-b py-2">Company</th>
          <th className="border-b py-2">Match %</th>
          <th className="border-b py-2">Actions</th>
        </tr>
      </thead>
      <tbody>
        {/* TODO: map jobs to rows */}
      </tbody>
    </table>
  );
}
TSX

# --- docker & env ----------------------------------------------------------
cat > ai-job-app/docker-compose.yml <<'YML'
version: "3.9"
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
      POSTGRES_DB: appdb
    volumes:
      - db_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  api:
    build: ./backend
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/code
    environment:
      - DATABASE_URL=postgresql+asyncpg://app:app@postgres/appdb
      - OPENAI_API_KEY=
    depends_on:
      - postgres
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    command: npm run dev -- --host 0.0.0.0
    volumes:
      - ./frontend:/app
    ports:
      - "5173:5173"
    depends_on:
      - api

volumes:
  db_data:
YML

cat > ai-job-app/.env.example <<'ENV'
# Copy to .env and fill in real values
DATABASE_URL=postgresql+asyncpg://app:app@localhost/appdb
OPENAI_API_KEY=
ENV

# --- readme ----------------------------------------------------------------
cat > ai-job-app/README.md <<'MD'
# AI Job‑App Assistant – MVP

Scaffold generated via `scaffold.sh`. Follow the quick‑start:

```bash
# 1. spin everything up
$ docker compose up --build -d

# 2. seed a résumé (replace with your own)
$ curl -X POST -F "file=@resume.txt" http://localhost:8000/resume/upload

# 3. manual scrape example
$ poetry run python backend/scraper/playwright_scraper.py --url https://careers.example.com
```

Then open <http://localhost:5173> for the React UI.
MD

# --- gitignore -------------------------------------------------------------
cat > ai-job-app/.gitignore <<'GI'
.env
__pycache__/
node_modules/
.playwright/
db_data/
GI

echo "\n✅  Scaffold complete at $(pwd)/ai-job-app"