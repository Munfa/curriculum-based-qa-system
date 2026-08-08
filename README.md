# Bangla Curriculum QA

A curriculum-grounded study assistant over the NCTB (Bangladesh) textbook
corpus. Students pick a class / subject / chapter and can ask questions or
practice exam-style questions, all grounded in the actual textbook text.

## Team & modules

| Person | Module | Owns |
|--------|--------|------|
| A | `retrieval.py` | Corpus cleaning, vector index, passage + metadata retrieval |
| B | (pattern library) | MCQ / CQ example sets that teach the LLM exam style |
| C | (generation) | QA, MCQ/CQ generation, grading — calls Person A for facts |
| D | (frontend) | Streamlit/Next.js UI — calls Person C only |

Only one knowledge base exists: the NCTB textbook corpus, served by Person A.

## Repo layout

```
clean_corpus.py          # cleaning + quality filtering (Person A)
build_index.py           # embedding + Chroma index build (Person A)
retrieval.py             # the retrieval contract others import (Person A)
RETRIEVAL_CONTRACT.md    # how to use retrieval.py (read this)
```

Large data folders are NOT in git (see `.gitignore`) — get them separately:

```
cleaned/                 # cleaned corpus (chunks_v1.jsonl is used at runtime)
index_v1/                # Chroma vector index (required to run retrieval)
NCTB-SchoolText.../       # raw dataset (download from Mendeley, not redistributed)
```

## Setup

```bash
pip install sentence-transformers chromadb torch pandas

# Option A (fast): get prebuilt index_v1/ and cleaned/ from the team's
# shared drive, drop them in the project root. Skip to "Use it".

# Option B (rebuild from scratch — needs the raw NCTB dataset):
python clean_corpus.py --root "NCTB-SchoolText.../NCTB-SchoolText" --out cleaned
#   then filter to the v1 (text-heavy) subjects:
python3 -c "import json; keep={'Bangla','Bangla_rapidreader','Bangla_grammar','English','English_grammar','Science','BGS','History','Geography','Civics','Biology','Biology_secondary','Science_secondary'}; \
[open('cleaned/chunks_v1.jsonl','w').write(''.join(l for l in open('cleaned/chunks_clean.jsonl') if json.loads(l).get('subject') in keep))]"
python build_index.py --input cleaned/chunks_v1.jsonl --out_dir index_v1 --model intfloat/multilingual-e5-large
```

Rebuilding the index uses your Mac GPU (MPS) automatically if available —
make sure that fix is in `build_index.py` or it will fall back to CPU and be
very slow.

## Use it (Person C / anyone needing textbook facts)

```python
from retrieval import list_classes, list_subjects, list_chapters, retrieve_passage

list_classes()                 # [1, 2, ..., 8, "9-10"]
list_subjects(6)               # ["BGS", "Bangla", ..., "Science"]
list_chapters(6, "Science")    # [{"chapter_no": 1, "chapter_title": "..."}, ...]

retrieve_passage(6, "Science", 5, "সালোকসংশ্লেষণ কী", top_k=5)
# -> list of {text, class, subject, chapter_no, chapter_title, chunk_id, score}
```

Full details and the envelope-shaped `retrieve()` variant are in
`RETRIEVAL_CONTRACT.md`.

## Scope notes (v1)

- Text-heavy subjects only. Math / Higher_math / Physics / Arabic are excluded
  (poor OCR quality) and won't appear in retrieval.
- No page numbers in the dataset — citations use chunk_id + chapter.
- Class 9–10 is the combined SSC set, represented as the string `"9-10"`.