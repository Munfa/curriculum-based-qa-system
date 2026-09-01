"""Backward-compatible Uvicorn entry point.

Prefer ``uvicorn backend.app:app`` for new development.
"""

from backend.app import app

__all__ = ["app"]
