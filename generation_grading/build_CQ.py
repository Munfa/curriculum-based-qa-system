import uuid
from retrieval.retrieval import retrieve
from .build_QA import build_context
from .get_patterns import get_cq_examples
from .llm import generate

cq_ans_store = {}


CQ_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "stimulus": {
            "type": "STRING"
        },
        "ka": {
            "type": "STRING"
        },
        "kha": {
            "type": "STRING"
        },
        "ga": {
            "type": "STRING"
        },
        "gha": {
            "type": "STRING"
        },
        "reference_answers": {
            "type": "OBJECT",
            "properties": {
                "ka": {"type": "STRING"},
                "kha": {"type": "STRING"},
                "ga": {"type": "STRING"},
                "gha": {"type": "STRING"}
            },
            "required": [
                "ka",
                "kha",
                "ga",
                "gha"
            ]
        }
    },
    "required": [
        "stimulus",
        "ka",
        "kha",
        "ga",
        "gha",
        "reference_answers"
    ]
}

# ============================================================
# CQ prompt generate
# ============================================================

def build_cq_prompt(class_number, subject, chapter, difficulty, passages, examples):

    context = build_context(passages)

    example_text = "\n\n".join(
        f"""
            Stimulus:
            {e["stimulus"]}

            ক:
            {e["questions"]["ka"]}

            খ:
            {e["questions"]["kha"]}

            গ:
            {e["questions"]["ga"]}

            ঘ:
            {e["questions"]["gha"]}
            """
        for e in examples
    )

    prompt = f"""
        Generate ONE Bangladeshi curriculum-style Creative Question (CQ).

        Class: {class_number}
        Subject: {subject}
        Chapter: {chapter}
        Difficulty: {difficulty}

        Use ONLY the textbook passages for factual information.

        The examples are only for learning question structure
        and exam style. Do not copy them.

        Requirements:
        - one stimulus
        - four connected parts: ka, kha, ga, gha
        - increasing cognitive difficulty
        - appropriate for the requested difficulty
        - all content must be supported by the textbook
        - provide a reference answer for every part

        TEXTBOOK PASSAGES:

        {context}

        EXAMPLES:

        {example_text}
        """
    
    return prompt

# ============================================================
# CQ question generate
# ============================================================

def generate_cq(class_number, subject, chapter, difficulty):

    retrieval = retrieve(
        class_number,
        subject,
        chapter,
        f"{subject} chapter {chapter} {difficulty} creative question",
        top_k=5
    )

    passages = retrieval["passages"]

    if not passages:
        raise ValueError(
            "No relevant textbook passages were retrieved."
        )

    examples = get_cq_examples(
        difficulty,
        n=2
    )

    if not examples:
        raise ValueError("No CQ examples available.")

    prompt = build_cq_prompt(
        class_number,
        subject,
        chapter,
        difficulty,
        passages,
        examples
    )

    result = generate(prompt, CQ_SCHEMA)

    question_id = str(uuid.uuid4())

    cq_ans_store[question_id] = {
        "reference_answers": result["reference_answers"]
    }

    return {
        "question_id": question_id,
        "stimulus": result["stimulus"],
        "ka": result["ka"],
        "kha": result["kha"],
        "ga": result["ga"],
        "gha": result["gha"]
    }