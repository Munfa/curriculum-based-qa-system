import uuid
from retrieval.retrieval import retrieve
from .build_QA import build_context
from .get_patterns import get_mcq_examples
from .llm import generate

mcq_ans_store = {}

MCQ_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "question": {
            "type": "STRING"
        },
        "options": {
            "type": "ARRAY",
            "items": {
                "type": "STRING"
            }
        },
        "correct_option": {
            "type": "STRING"
        }
    },
    "required": [
        "question",
        "options",
        "correct_option"
    ]
}

# ============================================================
# MCQ prompt generate
# ============================================================

def build_mcq_prompt(class_number, subject, chapter, difficulty, passages, examples):

    context = build_context(passages)

    example_text = "\n\n".join(
        f"""
            Question:
            {e["question"]}

            Options:
            {chr(10).join(
                f"{i + 1}. {option}"
                for i, option in enumerate(e["options"])
            )}
        """
        for e in examples
    )

    prompt = f"""
        Generate twenty multiple-choice question for:

        Class: {class_number}
        Subject: {subject}
        Chapter: {chapter}
        Difficulty: {difficulty}

        Use ONLY the textbook passages for factual content.

        The examples are only for learning the exam style.
        Do not copy them.

        Requirements:
        - exactly 4 options
        - exactly 1 correct option
        - appropriate for the requested difficulty
        - answer must be supported by the textbook

        TEXTBOOK PASSAGES:

        {context}

        EXAMPLES:

        {example_text}
    """
    return prompt

# ============================================================
# MCQ question generate
# ============================================================

def generate_mcq(class_number, subject, chapter, difficulty):

    retrieval = retrieve(
        class_number,
        subject,
        chapter,
        f"{subject} chapter {chapter} {difficulty} MCQ",
        top_k=5
    )

    passages = retrieval["passages"]

    if not passages:
        raise ValueError("No relevant textbook passages were retrieved.")

    examples = get_mcq_examples(
        subject,
        difficulty,
        n=3
    )

    if not examples:
        raise ValueError( "No MCQ examples available.")

    prompt = build_mcq_prompt(
        class_number,
        subject,
        chapter,
        difficulty,
        passages,
        examples
    )

    result = generate( prompt, MCQ_SCHEMA)

    if len(result["options"]) != 4:
        raise ValueError("Generated MCQ does not contain exactly 4 options.")

    if result["correct_option"] not in result["options"]:
        raise ValueError( "Correct option is not one of the options.")

    question_id = str(uuid.uuid4())

    mcq_ans_store[question_id] = {
        "correct_option": result["correct_option"]
    }

    return {
        "question_id": question_id,
        "question": result["question"],
        "options": result["options"]
    }