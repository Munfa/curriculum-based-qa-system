"""Temporary in-memory answer stores.

Replace these dictionaries with shared persistent storage before using
multiple backend workers or deploying across multiple instances.
"""

mcq_answer_store: dict[str, dict[str, str]] = {}
cq_answer_store: dict[str, dict[str, dict[str, str]]] = {}
