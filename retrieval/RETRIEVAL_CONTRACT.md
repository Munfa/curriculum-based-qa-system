# Person A — Retrieval Contract

Everything Person A provides is implemented in `retrieval/retrieval.py` and exposed through the `retrieval` package. Import from it directly:

```python
from retrieval import (
    list_classes,
    list_subjects,
    list_chapters,
    retrieve_passage,
    retrieve,           # optional envelope-shaped variant
)
```

Person A never calls an LLM and never generates answers. This module only
returns textbook metadata and passages. Person C consumes it for QA / MCQ /
CQ generation and grading; Person D gets the metadata (for dropdowns) through
Person C.

---

## Setup (one-time, per machine)

The module expects two things to exist in the project folder:

- `index_v1/` — the Chroma vector index (built by `retrieval/build_index.py`)
- `cleaned/chunks_v1.jsonl` — the cleaned chunks (built by `retrieval/clean_corpus.py`)

Override paths with env vars if needed:
`BANGLA_QA_INDEX` (default `index_v1`) and `BANGLA_QA_CHUNKS`
(default `cleaned/chunks_v1.jsonl`).

The first call to `retrieve_passage` loads the embedding model (a few seconds).
Metadata functions do NOT load the model — they read the JSONL and return
instantly.

---

## Metadata functions (for dropdowns)

### `list_classes() -> list`
All available class levels, ordered.
```python
list_classes()
# [1, 2, 3, 4, 5, 6, 7, 8, "9-10"]
```

### `list_subjects(class_) -> list[str]`
Subjects available for a class, alphabetical. Empty list if class not found.
```python
list_subjects(6)
# ["BGS", "Bangla", "Bangla_grammar", "Bangla_rapidreader",
#  "English", "English_grammar", "Science"]
```

### `list_chapters(class_, subject) -> list[dict]`
Chapters for a class + subject, ordered by chapter number. Empty list if not
found.
```python
list_chapters(6, "Science")
# [{"chapter_no": 1, "chapter_title": "বৈজ্ঞানিক প্রক্রিয়া ও পরিমাপ"},
#  {"chapter_no": 2, "chapter_title": "জীবজগৎ"},
#  ... ]
```

---

## Retrieval function (for facts)

### `retrieve_passage(class_, subject, chapter, query, top_k=5) -> list[dict]`

Returns the `top_k` most relevant passage chunks for `query`. Any of
`class_` / `subject` / `chapter` may be `None` to leave that dimension
unfiltered. Returns an **empty list** if the filters match nothing (filters
are never silently dropped).

Each result dict:
```python
{
    "text":          "…passage text…",
    "class":         6,
    "subject":       "Science",
    "chapter_no":    5,
    "chapter_title": "সালোকসংশ্লেষণ",
    "chunk_id":      "6-Science-5-11",
    "score":         0.7312,     # cosine similarity in [0,1], higher = better
}
```

Examples:
```python
# scoped to one chapter
retrieve_passage(6, "Science", 5, "সালোকসংশ্লেষণ কী", top_k=3)

# subject-wide (no chapter filter)
retrieve_passage(7, "Science", None, "উদ্ভিদের খাদ্য")

# whole corpus (all None)
retrieve_passage(None, None, None, "মুক্তিযুদ্ধ")
```

### `retrieve(class_, subject, chapter, query, top_k=5) -> dict`
Same retrieval, wrapped in the team-plan envelope shape:
```python
{
  "query": ..., "class": ..., "subject": ..., "chapter": ...,
  "passages": [ {text, class, subject, chapter_no, chapter_title,
                 chunk_id, score}, ... ]
}
```

---

## Known limitations (please read)

- **No `page` field.** The NCTB-SchoolText dataset has no page numbers, so
  passages cannot carry a `page`. Citations use `chunk_id` + `chapter_no` /
  `chapter_title` instead. The team plan's example showed a `page` field — it
  is not available and has been dropped.
- **v1 scope is text-heavy subjects only.** Math, Higher_math, Physics, and
  Arabic are excluded from the index because their OCR quality is poor
  (55–66% of their chunks flagged as likely garbled). They will not appear in
  `list_subjects` and cannot be retrieved. Adding them later requires
  re-cleaning those subjects and rebuilding the index.
- **Class 9–10 is combined** as `"9-10"` (a string, not an int) — the SSC book
  set covers both grades together. Handle it as a string in any class logic.
