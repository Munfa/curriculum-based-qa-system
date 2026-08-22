import json
import random
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "question_pattern"

MCQ_FILE = DATA_DIR / "mcq_question_pattern.json"
CQ_FILE = DATA_DIR / "cq_question_pattern.json"


def _flatten_examples(raw, example_key):
   
    examples = []
    common = raw.get("common_subjects", {})

    if isinstance(common, dict):
        subject_entries = [common]
    elif isinstance(common, list):
        subject_entries = common
    else:
        subject_entries = []

    for subject_entry in subject_entries:
        if not isinstance(subject_entry, dict):
            continue
        for chapter in subject_entry.get("chapters", []):
            for ex in chapter.get(example_key, []):
                if isinstance(ex, dict):
                    examples.append(ex)
    return examples


with open(MCQ_FILE, "r", encoding="utf-8") as f:
    mcq_examples = _flatten_examples(json.load(f), "mcq_examples")

with open(CQ_FILE, "r", encoding="utf-8") as f:
    cq_examples = _flatten_examples(json.load(f), "cq_examples")


def get_mcq_examples(subject, difficulty=None, n=3):
    matches = [
        example
        for example in mcq_examples
        if example["subject"] == subject
    ]

    #matches = list(mcq_examples)

    if difficulty:
        difficulty_matches = [
            example
            for example in matches
            if example.get("difficulty") == difficulty
        ]
        if difficulty_matches:
            matches = difficulty_matches

    return random.sample(matches, min(n, len(matches)))


def get_cq_examples(subject, difficulty=None, n=3):
    matches = [
        example
        for example in cq_examples
        if example["subject"] == subject
    ]

    #matches = list(cq_examples)

    if difficulty:
        difficulty_matches = [
            example
            for example in matches
            if example.get("difficulty") == difficulty
        ]
        if difficulty_matches:
            matches = difficulty_matches

    return random.sample(matches, min(n, len(matches)))


def get_eng_examples():
    pass

def get_eng_gram_examples():
    pass

def get_bang_examples():
    pass