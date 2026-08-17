import json
import random
from pathlib import Path

DATA_DIR = Path("question_pattern")

MCQ_FILE = DATA_DIR / "mcq_question_pattern.json"
CQ_FILE = DATA_DIR / "cq_question_pattern.json"

with open(MCQ_FILE, "r", encoding="utf-8") as f:
    mcq_examples = json.load(f)

with open(CQ_FILE, "r", encoding="utf-8") as f:
    cq_examples = json.load(f)

def get_mcq_examples(subject, difficulty=None, n=3):

    matches = [
        example
        for example in mcq_examples
        if example["subject"] == subject
    ]

    if difficulty:
        difficulty_matches = [
            example
            for example in matches
            if example.get("difficulty") == difficulty
        ]

        if difficulty_matches:
            matches = difficulty_matches

    return random.sample(
        matches,
        min(n, len(matches))
    )

def get_cq_examples(subject, difficulty=None, n=3):

    matches = [
        example
        for example in cq_examples
        if example["subject"] == subject
    ]

    if difficulty:
        difficulty_matches = [
            example
            for example in matches
            if example.get("difficulty") == difficulty
        ]

        if difficulty_matches:
            matches = difficulty_matches

    return random.sample(
        matches,
        min(n, len(matches))
    )

def get_eng_examples():
    pass

def get_eng_gram_examples():
    pass

def get_bang_examples():
    pass