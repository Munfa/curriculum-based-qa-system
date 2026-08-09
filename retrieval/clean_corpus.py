"""
clean_corpus.py
Cleaning + quality-filtering pipeline for the NCTB-SchoolText corpus.

What it does:
1. Loads every processed_chapters_*/*.jsonl file under the dataset root.
2. Computes a per-chunk quality score based on the ratio of valid
   Bangla/Latin/Arabic letters to total characters (a proxy for OCR noise).
3. Flags/drops chunks that look like OCR garbage (diagrams, tables, formulas
   that Tesseract mangled) vs. chunks that are just short-but-legitimate.
4. Writes out:
   - a cleaned chunk-level JSONL (noise dropped)
   - a quarantined chunk-level JSONL (noise kept separately for manual review)
   - a chapter-level JSONL (chunks concatenated in order per chapter) for use
     as the unit fed into question generation
   - a quality report (per-subject noise rates) so you can see which subjects
     need the most attention (expect Math/Physics/Chemistry/Higher Math to be
     the worst offenders)

"""

import argparse
import json
import re
import glob
import os
from collections import defaultdict

# ---- character classes we consider "valid" content ----
BANGLA_RANGE = r"\u0980-\u09FF"
ARABIC_RANGE = r"\u0600-\u06FF"
LATIN_RANGE = r"A-Za-z"
DIGIT_RANGE = r"0-9\u09E6-\u09EF"  # ASCII + Bangla digits
# punctuation / whitespace we don't penalize
BENIGN_PUNCT = r"\s.,;:!?'\"()\-–—।॥/%০-৯০-৯"

VALID_CHAR_RE = re.compile(f"[{BANGLA_RANGE}{ARABIC_RANGE}{LATIN_RANGE}{DIGIT_RANGE}]")
ANY_LETTER_RE = re.compile(f"[{BANGLA_RANGE}{ARABIC_RANGE}{LATIN_RANGE}]")


def quality_score(text: str) -> float:
   
    stripped = re.sub(r"\s+", "", text)
    if not stripped:
        return 0.0
    valid = len(VALID_CHAR_RE.findall(stripped))
    return valid / len(stripped)


def looks_fragmented(text: str) -> bool:
    
    words = text.split()
    if len(words) < 4:
        return False
    short_words = [w for w in words if len(re.sub(r"[^\w]", "", w)) <= 2]
    return (len(short_words) / len(words)) > 0.55


def looks_formula_garbled(text: str) -> bool:
    
    words = text.split()
    if len(words) < 3:
        return False
    short_words = [w for w in words if len(re.sub(r"[^\w]", "", w)) <= 2]
    mixed_alnum = [w for w in words if re.search(r"\d", w) and re.search(r"[A-Za-z\u0980-\u09FF]", w)]
    short_ratio = len(short_words) / len(words)
    mixed_ratio = len(mixed_alnum) / len(words)
    return short_ratio > 0.55 or mixed_ratio > 0.15


def load_chunks(root: str):
    pattern = os.path.join(root, "**", "processed_chapters_*", "*.jsonl")
    files = glob.glob(pattern, recursive=True)
    for fp in files:
        with open(fp, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                rec["_source_file"] = fp
                yield rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="Path to the extracted nctb/ folder")
    ap.add_argument("--out", required=True, help="Output directory")
    ap.add_argument("--min-quality", type=float, default=0.55,
                     help="Minimum valid-character ratio to keep a chunk (default 0.55)")
    ap.add_argument("--min-len", type=int, default=15,
                     help="Minimum character length to keep a chunk (default 15)")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)

    clean_path = os.path.join(args.out, "chunks_clean.jsonl")
    quarantine_path = os.path.join(args.out, "chunks_quarantined.jsonl")
    chapter_path = os.path.join(args.out, "chapters_clean.jsonl")
    report_path = os.path.join(args.out, "quality_report.json")

    subject_stats = defaultdict(lambda: {"total": 0, "kept": 0, "quarantined": 0, "review_recommended": 0})
    chapter_buffer = defaultdict(list)  # (class, subject, chapter_no) -> [ (chunk_index, text) ]
    chapter_meta = {}

    n_total = 0
    n_kept = 0
    n_quarantined = 0

    with open(clean_path, "w", encoding="utf-8") as f_clean, \
         open(quarantine_path, "w", encoding="utf-8") as f_quar:

        for rec in load_chunks(args.root):
            n_total += 1
            text = rec.get("text", "") or ""
            subj = rec.get("subject", "unknown")
            subject_stats[subj]["total"] += 1

            q = quality_score(text)
            too_short = len(text.strip()) < args.min_len
            fragmented = looks_fragmented(text)
            review_recommended = looks_formula_garbled(text)
            
            rec_out = dict(rec)
            rec_out["quality_score"] = round(q, 3)
            rec_out["flag_too_short"] = too_short
            rec_out["flag_fragmented"] = fragmented
            rec_out["flag_review_recommended"] = review_recommended

            if review_recommended:
                subject_stats[subj]["review_recommended"] += 1

            if is_noisy:
                n_quarantined += 1
                subject_stats[subj]["quarantined"] += 1
                f_quar.write(json.dumps(rec_out, ensure_ascii=False) + "\n")
            else:
                n_kept += 1
                subject_stats[subj]["kept"] += 1
                f_clean.write(json.dumps(rec_out, ensure_ascii=False) + "\n")

                # accumulate for chapter-level rollup (clean chunks only)
                key = (rec.get("class"), subj, rec.get("chapter_no"))
                chunk_id = rec.get("chunk_id", "")
                idx = chunk_id.split("-")[-1] if chunk_id else "0"
                try:
                    idx = int(idx)
                except ValueError:
                    idx = 0
                chapter_buffer[key].append((idx, text))
                chapter_meta[key] = {
                    "class": rec.get("class"),
                    "subject": subj,
                    "chapter_no": rec.get("chapter_no"),
                    "chapter_title": rec.get("chapter_title"),
                }

    # write chapter-level rollups, ordered by chunk index
    with open(chapter_path, "w", encoding="utf-8") as f_chap:
        for key, chunks in chapter_buffer.items():
            chunks.sort(key=lambda x: x[0])
            full_text = "\n".join(t for _, t in chunks)
            meta = chapter_meta[key]
            out = {
                **meta,
                "chapter_id": f"{meta['class']}-{meta['subject']}-{meta['chapter_no']}",
                "n_chunks": len(chunks),
                "text": full_text,
            }
            f_chap.write(json.dumps(out, ensure_ascii=False) + "\n")

    # quality report
    report = {
        "total_chunks": n_total,
        "kept": n_kept,
        "quarantined": n_quarantined,
        "kept_pct": round(100 * n_kept / n_total, 2) if n_total else 0,
        "by_subject": {
            s: {
                **v,
                "quarantined_pct": round(100 * v["quarantined"] / v["total"], 2) if v["total"] else 0,
            }
            for s, v in sorted(subject_stats.items(), key=lambda kv: -kv[1]["quarantined"])
        },
    }
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"Total chunks:      {n_total}")
    print(f"Kept (clean):      {n_kept} ({report['kept_pct']}%)")
    print(f"Quarantined:       {n_quarantined}")
    print(f"Chapters rolled up:{len(chapter_buffer)}")
    print(f"\nWorst subjects by quarantine rate:")
    worst = sorted(subject_stats.items(), key=lambda kv: -(kv[1]["quarantined"] / kv[1]["total"]))[:8]
    for s, v in worst:
        pct = round(100 * v["quarantined"] / v["total"], 1) if v["total"] else 0
        print(f"  {s:25s} {v['quarantined']:5d}/{v['total']:5d} quarantined ({pct}%)")

    print(f"\nWorst subjects by REVIEW-RECOMMENDED rate (soft flag, not dropped -- "
          f"these are the ones the hard filter misses):")
    worst_review = sorted(subject_stats.items(), key=lambda kv: -(kv[1]["review_recommended"] / kv[1]["total"]))[:10]
    for s, v in worst_review:
        pct = round(100 * v["review_recommended"] / v["total"], 1) if v["total"] else 0
        print(f"  {s:25s} {v['review_recommended']:5d}/{v['total']:5d} flagged ({pct}%)")
    print(f"\nOutputs written to: {args.out}")


if __name__ == "__main__":
    main()