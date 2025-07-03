"""Generate tailored bullets and cover letter using OpenAI chat completions."""
from __future__ import annotations

import os
from typing import Dict

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # type: ignore

MODEL = "gpt-4o-mini"  # or gpt-4o if available

_client = None

def _get_client():
    global _client
    if _client is None:
        if OpenAI is None:
            raise RuntimeError("openai package not installed")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY env var not set")
        _client = OpenAI(api_key=api_key)
    return _client


def generate_application_text(resume_text: str, jd_text: str, company_name: str) -> Dict[str, str]:
    """Return markdown bullets and cover letter strings."""
    client = _get_client()

    system_prompt = "You are an expert technical recruiter writing concise, high-impact résumé bullets and cover letters."
    user_prompt = f"""
Résumé:
{resume_text}

Job Description:
{jd_text}

Return exactly:\n1. Four bullet points (start each with •, <= 25 words, include metrics if present).\n2. A 140-160 word cover letter mentioning {company_name} once.\nFormat as Markdown.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        temperature=0.7,
    )
    content = response.choices[0].message.content  # type: ignore
    # Split bullets and cover letter
    if content is None:
        raise RuntimeError("Empty response from OpenAI")
    parts = content.split("\n\n", 1)
    bullets = parts[0].strip()
    cover_letter = parts[1].strip() if len(parts) > 1 else ""
    return {"bullets": bullets, "cover_letter": cover_letter}