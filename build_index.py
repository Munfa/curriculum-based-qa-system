"""
build_index.py
Embedding + indexing pipeline for the cleaned NCTB-SchoolText corpus.
Builds a Chroma collection from the same source.

Retrieval granularity:
  - Indexes chunk-level text (chunks_clean.jsonl) for precise QA grounding.
  - Also supports indexing chapter-level text (chapters_clean.jsonl) if you
    want coarser, chapter-scoped retrieval for question generation -- just
    point --input at that file instead.

Embedding model:
  Defaults to 'intfloat/multilingual-e5-large' . Swap
  via --model. Requires internet access to Hugging Face to download weights
  the first time -- run this on your own machine / Colab, not in a sandboxed
  environment with restricted network egress.

"""

import argparse
import json
import os

import numpy as np


# ---------------------------------------------------------------------------
# Embedding backend -- pluggable so this script can be dry-run tested without
# internet access, and swapped to a real model when you run it for real.
# ---------------------------------------------------------------------------
class Embedder:
    def __init__(self, model_name: str, dim: int = None, use_mock: bool = False):
        self.model_name = model_name
        self.use_mock = use_mock
        if use_mock:
            self.dim = dim or 384
        else:
            from sentence_transformers import SentenceTransformer
            import torch
            device = "mps" if torch.backends.mps.is_available() else "cpu"
            self.model = SentenceTransformer(model_name, device=device)
            print(f"Using device: {device}")
            self.dim = self.model.get_sentence_embedding_dimension()

    def encode(self, texts, batch_size=64, is_query=False):
        if self.use_mock:
            return self._mock_encode(texts)
        # e5 models expect a "query: " / "passage: " prefix for best results
        if "e5" in self.model_name.lower():
            prefix = "query: " if is_query else "passage: "
            texts = [prefix + t for t in texts]
        vecs = self.model.encode(
            texts, batch_size=batch_size, show_progress_bar=True,
            normalize_embeddings=True,
        )
        return np.asarray(vecs, dtype="float32")

    def _mock_encode(self, texts):
        vecs = np.zeros((len(texts), self.dim), dtype="float32")
        for i, t in enumerate(texts):
            for j in range(len(t) - 2):
                ng = t[j:j + 3]
                h = hash(ng) % self.dim
                vecs[i, h] += 1.0
            norm = np.linalg.norm(vecs[i])
            if norm > 0:
                vecs[i] /= norm
        return vecs


def load_records(path):
    recs = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                recs.append(json.loads(line))
    return recs


def build(args):
    records = load_records(args.input)
    texts = [r["text"] for r in records]
    print(f"Loaded {len(records)} records from {args.input}")

    embedder = Embedder(args.model, use_mock=args.mock_embeddings)
    print(f"Embedding with {'MOCK embedder (testing only)' if args.mock_embeddings else args.model} "
          f"(dim={embedder.dim}) ...")

    embeddings = embedder.encode(texts, is_query=False)

    os.makedirs(args.out_dir, exist_ok=True)

    # ---- Chroma ----
    import chromadb
    client = chromadb.PersistentClient(path=os.path.join(args.out_dir, "chroma_db"))
    coll = client.get_or_create_collection("nctb_schooltext")
    B = 500
    for i in range(0, len(records), B):
        batch_recs = records[i:i + B]
        batch_emb = embeddings[i:i + B].tolist()
        coll.add(
            ids=[r.get("chunk_id") or r.get("chapter_id") or str(i + k) for k, r in enumerate(batch_recs)],
            embeddings=batch_emb,
            documents=[r["text"] for r in batch_recs],
            metadatas=[{
                "class": str(r.get("class")),
                "subject": r.get("subject", ""),
                "chapter_no": r.get("chapter_no", 0),
                "chapter_title": r.get("chapter_title", ""),
            } for r in batch_recs],
        )
    print(f"Chroma collection written: {coll.count()} vectors")

    
    with open(os.path.join(args.out_dir, "config.json"), "w") as f:
        json.dump({"model": args.model, "dim": embedder.dim, "mock": args.mock_embeddings}, f)

    print(f"\nDone. Index artifacts in: {args.out_dir}")


def query(args):
    with open(os.path.join(args.out_dir, "config.json")) as f:
        cfg = json.load(f)

    embedder = Embedder(cfg["model"], dim=cfg["dim"], use_mock=cfg["mock"])
    q_vec = embedder.encode([args.query], is_query=True)[0].tolist()

    import chromadb
    client = chromadb.PersistentClient(path=os.path.join(args.out_dir, "chroma_db"))
    coll = client.get_collection("nctb_schooltext")

    where = {}
    if args.filter_class:
        where["class"] = str(args.filter_class)
    if args.filter_subject:
        where["subject"] = args.filter_subject

    res = coll.query(
        query_embeddings=[q_vec],
        n_results=args.top_k,
        where=where if where else None,
    )

    docs = res["documents"][0]
    metas = res["metadatas"][0]
    dists = res["distances"][0]

    print(f"\nTop {len(docs)} results for: {args.query!r}")
    for doc, meta, dist in zip(docs, metas, dists):
        score = 1 - dist  # cosine distance -> similarity
        print(f"\n[{score:.3f}] class={meta.get('class')} subject={meta.get('subject')} "
              f"ch{meta.get('chapter_no')} ({meta.get('chapter_title')})")
        print(f"  {doc[:200]}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", help="chunks_clean.jsonl or chapters_clean.jsonl")
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--model", default="intfloat/multilingual-e5-large")
    ap.add_argument("--mock_embeddings", action="store_true",
                     help="Use a deterministic hash-based embedder for pipeline "
                          "testing without internet/model-download access. "
                          "Do NOT use this for real retrieval quality.")
    ap.add_argument("--query", help="If set, run a query against an existing index instead of building")
    ap.add_argument("--top_k", type=int, default=5)
    ap.add_argument("--filter_class", default=None)
    ap.add_argument("--filter_subject", default=None)
    args = ap.parse_args()

    if args.query:
        query(args)
    else:
        if not args.input:
            raise SystemExit("--input is required when building an index")
        build(args)