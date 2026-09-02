"""
retrieval.py
Passage retrieval for the Bangla Curriculum QA system.

This is the CONTRACT other team members build against. The public function is:

    retrieve_passage(class_, subject, chapter, query, top_k=5) -> list[dict]

Each returned dict has these keys :
    text          : the passage chunk text
    class         : grade level (e.g. 6, 7, "9-10")
    subject       : subject name (e.g. "Science")
    chapter_no    : chapter number
    chapter_title : chapter title
    chunk_id      : unique chunk identifier
    score         : cosine similarity in [0, 1], higher = more relevant

Any of class_ / subject / chapter may be None to leave that dimension unfiltered.
If the filters match nothing, an EMPTY LIST is returned (filters are never
silently dropped) — callers decide what to do with no results.

Usage:
    from retrieval import retrieve_passage

    # scoped to one chapter
    hits = retrieve_passage(6, "Science", 5, "সালোকসংশ্লেষণ কী", top_k=3)

    # subject-wide, no chapter filter
    hits = retrieve_passage(7, "Science", None, "উদ্ভিদের খাদ্য")

    # fully open search across the whole corpus
    hits = retrieve_passage(None, None, None, "মুক্তিযুদ্ধ")
"""

import json
import os
import functools
import requests  
import time  

# Path to the index directory produced by build_index.py.

INDEX_DIR = os.environ.get("BANGLA_QA_INDEX", "index_v1")
COLLECTION_NAME = "nctb_schooltext"

# Path to the cleaned chunks the index was built from. Metadata lookups

CHUNKS_FILE = os.environ.get("BANGLA_QA_CHUNKS", "cleaned/chunks_v1.jsonl")

HF_API_TOKEN = os.environ.get("HF_API_TOKEN")
HF_API_URL = "https://router.huggingface.co/hf-inference/models/intfloat/multilingual-e5-large"


@functools.lru_cache(maxsize=1)
def _load():
    """
    Load the embedding model and Chroma collection ONCE and cache them.
    First call is slow (loads the model); later calls are instant.
    Returns (embedder, collection).
    """
    with open(os.path.join(INDEX_DIR, "config.json")) as f:
        cfg = json.load(f)

    # from sentence_transformers import SentenceTransformer
    # import torch
    # device = "mps" if torch.backends.mps.is_available() else "cpu"
    # model = SentenceTransformer(cfg["model"], device=device)
    model_name = cfg["model"]

    import chromadb
    client = chromadb.PersistentClient(path=os.path.join(INDEX_DIR, "chroma_db"))
    collection = client.get_collection(COLLECTION_NAME)

    # return model, model_name, collection
    return model_name, collection


# def _embed_query(text):
#     model, model_name, _ = _load()
#     # e5 models want a "query: " prefix for best retrieval quality
#     if "e5" in model_name.lower():
#         text = "query: " + text
#     vec = model.encode([text], normalize_embeddings=True)
#     return vec[0].tolist()

def _embed_query(text):
    model_name, _ = _load()
    
    # e5 models want "query: " prefix
    if "e5" in model_name.lower():
        text = "query: " + text

    if not HF_API_TOKEN:
        raise RuntimeError("HF_API_TOKEN environment variable is not set.")

    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {"inputs": text}

    # Free HF API sometimes needs a warm-up; retry once
    for attempt in range(2):
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            # HF returns [[vec]] for single input
            return response.json()[0]
        
        if response.status_code == 503 and attempt == 0:
            time.sleep(3)  # wait for model warm-up
            continue
            
        response.raise_for_status()

    raise RuntimeError("HF Inference API failed after retry.")


def _build_where(class_, subject, chapter):
    """
    Build a Chroma `where` filter from whichever fields are provided.
    Chroma needs {"$and": [...]} when there is more than one condition,
    and a single {field: value} dict when there is exactly one.
    Returns None when nothing is filtered.
    """
    conditions = []
    if class_ is not None:
        conditions.append({"class": str(class_)})
    if subject is not None:
        conditions.append({"subject": subject})
    if chapter is not None:
        conditions.append({"chapter_no": chapter})

    if not conditions:
        return None
    if len(conditions) == 1:
        return conditions[0]
    return {"$and": conditions}


def retrieve_passage(class_, subject, chapter, query, top_k=5):
    """
    Retrieve the top_k most relevant passage chunks for `query`, optionally
    scoped by class_ / subject / chapter (any of which may be None).

    Returns a list of dicts (see module docstring for keys). Empty list if
    nothing matches the filters.
    """
    # _, _, collection = _load()
    _, collection = _load()
    where = _build_where(class_, subject, chapter)
    q_vec = _embed_query(query)

    res = collection.query(
        query_embeddings=[q_vec],
        n_results=top_k,
        where=where,  # None means no filter
    )

    
    ids = res["ids"][0] if res["ids"] else []
    docs = res["documents"][0] if res["documents"] else []
    metas = res["metadatas"][0] if res["metadatas"] else []
    dists = res["distances"][0] if res["distances"] else []

    results = []
    for cid, doc, meta, dist in zip(ids, docs, metas, dists):
        results.append({
            "text": doc,
            "class": meta.get("class"),
            "subject": meta.get("subject"),
            "chapter_no": meta.get("chapter_no"),
            "chapter_title": meta.get("chapter_title"),
            "chunk_id": cid,
            "score": round(1.0 - dist, 4),  # cosine distance -> similarity
        })
    return results


# ---------------------------------------------------------------------------
# Metadata lookups (for Person D's dropdowns, via Person C).
# These read the cleaned JSONL, NOT the vector DB, so they're instant and
# don't need the embedding model loaded.
# ---------------------------------------------------------------------------
@functools.lru_cache(maxsize=1)
def _load_metadata_index():
    """
    Scan the chunks file once and build a nested lookup:
        { class: { subject: { chapter_no: chapter_title } } }
    Cached so the file is only read once per process.
    """
    tree = {}
    with open(CHUNKS_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            c = r.get("class")
            s = r.get("subject")
            ch_no = r.get("chapter_no")
            ch_title = r.get("chapter_title")
            tree.setdefault(c, {}).setdefault(s, {})[ch_no] = ch_title
    return tree


def _sort_classes(classes):
    
    def key(c):
        s = str(c)
        
        head = s.split("-")[0]
        try:
            return (0, int(head))
        except ValueError:
            return (1, s)  # non-numeric classes sort last, alphabetically
    return sorted(classes, key=key)


def list_classes():
    
    tree = _load_metadata_index()
    return _sort_classes(tree.keys())


def list_subjects(class_):
    
    tree = _load_metadata_index()
    subjects = tree.get(class_, {})
    return sorted(subjects.keys())


def list_chapters(class_, subject):
    
    tree = _load_metadata_index()
    chapters = tree.get(class_, {}).get(subject, {})
    return [
        {"chapter_no": ch_no, "chapter_title": chapters[ch_no]}
        for ch_no in sorted(chapters.keys(), key=lambda x: (x is None, x))
    ]



def retrieve(class_, subject, chapter, query, top_k=5):
   
    passages = retrieve_passage(class_, subject, chapter, query, top_k=top_k)
    return {
        "query": query,
        "class": class_,
        "subject": subject,
        "chapter": chapter,
        "passages": passages,
    }



if __name__ == "__main__":
    import sys

    # --- metadata sanity check ---
    #print("Classes:", list_classes())
    #classes = list_classes()
    #if classes:
        #c = 6 if 6 in classes else classes[0]
        #subs = list_subjects(c)
        #print(f"\nSubjects for class {c}:", subs)
        #if "Science" in subs:
            #chs = list_chapters(c, "Science")
            #print(f"\nChapters for class {c} Science ({len(chs)}):")
            #for ch in chs[:5]:
                #print(f"  {ch['chapter_no']}: {ch['chapter_title']}")

    # --- retrieval check (loads the model) ---
    q = sys.argv[1] if len(sys.argv) > 1 else "সালোকসংশ্লেষণ কী"
    print(f"\nQuery: {q!r}\n")
    for r in retrieve_passage(None, None, None, q, top_k=3):
        print(f"[{r['score']}] class={r['class']} {r['subject']} "
              f"ch{r['chapter_no']} ({r['chapter_title']})")
        print(f"  {r['text'][:160]}\n")