"""Utility functions to generate text embeddings using OpenAI API."""
from __future__ import annotations

import os
from typing import List

try:
    from openai import OpenAI
except ImportError:  # During type checks when deps aren't installed
    OpenAI = None  # type: ignore


MODEL_NAME = "text-embedding-3-small"

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if OpenAI is None:
            raise RuntimeError("openai package not installed")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY env var not set")
        _client = OpenAI(api_key=api_key)
    return _client


def embed_text(text: str) -> List[float]:
    """Return embedding vector for given text (truncated at 8K tokens)."""
    client = _get_client()
    # OpenAI 1.x expects list input for multiple embeddings
    response = client.embeddings.create(model=MODEL_NAME, input=[text[:8192]])
    return response.data[0].embedding  # type: ignore