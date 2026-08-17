import json
import random
from pathlib import Path

mock_passages = {
    ("Science", 8, "Photosynthesis"): [
        {
            "chunk_id": "science8_ch03_001",
            "text": "Photosynthesis is the process by which green plants prepare food using sunlight, carbon dioxide and water.",
            "page": 42,
            "score": 0.91
        },
        {
            "chunk_id": "science8_ch03_002",
            "text": "Chlorophyll in green leaves absorbs sunlight needed for photosynthesis.",
            "page": 43,
            "score": 0.87
        }
    ],

    ("Mathematics", 8, "Geometry"): [
        {
            "chunk_id": "math8_ch05_001",
            "text": "The area of a rectangle is calculated by multiplying its length by its width.",
            "page": 65,
            "score": 0.92
        }
    ]
}

DATA_DIR = Path("person C/examples")

MCQ_FILE = DATA_DIR / "mcq_examples.json"
CQ_FILE = DATA_DIR / "cq_examples.json"

with open(MCQ_FILE, "r", encoding="utf-8") as f:
    mcq_examples = json.load(f)

with open(CQ_FILE, "r", encoding="utf-8") as f:
    cq_examples = json.load(f)

# print("MCQ examples:", len(mcq_examples))
# print("CQ examples:", len(cq_examples))

# print(mcq_examples[0])
# print(cq_examples[0])

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

# examples = get_cq_examples("Science", 8)

# for example in examples:
#     print(example)

# examples = get_mcq_examples("Science", 8)

# for example in examples:
#     print(example)

def mock_retrieve(class_number, subject, chapter, query):
    key = (subject, class_number, chapter)

    passages = mock_passages.get(key, [])

    return {
        "query": query,
        "class": class_number,
        "subject": subject,
        "chapter": chapter,
        "passages": passages
    }

retrieval = mock_retrieve(
    class_number=8,
    subject="Science",
    chapter="Photosynthesis",
    query="What is photosynthesis?"
)

# print(retrieval)
# print(json.dumps(retrieval, ensure_ascii=False, indent=2))

def mock_llm(prompt, task):
    """
    Temporary stand-in for the real LLM.

    Later, replace only this function with the actual
    free LLM/API call.
    """

    if task == "mcq":

        return {
            "question": "Which process allows green plants to prepare their own food?",
            "options": [
                "Respiration",
                "Photosynthesis",
                "Digestion",
                "Excretion"
            ],
            "correct_option": "Photosynthesis"
        }

    elif task == "cq":

        return {
            "stimulus": (
                "Rafi placed a green plant near a sunny window "
                "and watered it regularly. After several days, "
                "he observed that the plant remained healthy "
                "and continued to grow."
            ),
            "ka": "What is photosynthesis?",
            "kha": "Why is sunlight important for photosynthesis?",
            "ga": "Explain how green plants prepare food through photosynthesis.",
            "gha": (
                "Analyze why photosynthesis is important for "
                "maintaining life in an ecosystem."
            ),

            # These will be hidden from Person D
            "reference_answers": {
                "ka": (
                    "Photosynthesis is the process by which "
                    "green plants prepare food using sunlight, "
                    "carbon dioxide and water."
                ),
                "kha": (
                    "Sunlight provides the energy needed for "
                    "photosynthesis."
                ),
                "ga": (
                    "Green plants use sunlight, carbon dioxide "
                    "and water to prepare food through photosynthesis."
                ),
                "gha": (
                    "Photosynthesis provides food and releases oxygen, "
                    "supporting organisms and energy flow in ecosystems."
                )
            }
        }

    else:
        raise ValueError(f"Unknown task: {task}")