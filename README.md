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
