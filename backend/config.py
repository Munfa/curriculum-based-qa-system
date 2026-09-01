"""Central application configuration and project paths."""

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def _project_path(environment_name: str, default: str) -> Path:
    configured = Path(os.getenv(environment_name, default))
    return configured if configured.is_absolute() else PROJECT_ROOT / configured


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("gemini_api_key")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
INDEX_DIR = _project_path("BANGLA_QA_INDEX", "index_v1")
CHUNKS_FILE = _project_path("BANGLA_QA_CHUNKS", "cleaned/chunks_v1.jsonl")
QUESTION_PATTERN_DIR = PROJECT_ROOT / "question_pattern"
