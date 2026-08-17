from retrieval.retrieval import retrieve
from .llm import generate

QA_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "answer": {
            "type": "STRING"
        }
    },
    "required": ["answer"]
}

# ============================================================
# Build context for prompt
# ============================================================

def build_context(passages):

    return "\n\n".join(
        f"[Chunk: {p['chunk_id']} | {p['chapter_title']}]\n{p['text']}"
        for p in passages
    )

# ============================================================
# QA prompt
# ============================================================

def build_qa_prompt(question, retrieval):

    context = build_context(retrieval)

    prompt = f"""
You are answering a student's question using a Bangladeshi
school textbook.

Use ONLY the textbook passages below.

Do not use outside knowledge.

If the answer cannot be determined from the passages,
say that the answer is not available in the provided
textbook content.

TEXTBOOK:

{context}

QUESTION:

{question}

Give a concise, student-friendly answer.
"""

    return prompt

# ============================================================
# Answer query
# ============================================================

def answer_question(class_number, subject, chapter, question):

    retrieval = retrieve(
        class_number,
        subject,
        chapter,
        question,
        top_k=5
    )

    passages = retrieval["passages"]

    if not passages:
        raise ValueError(
            "No relevant textbook passages were retrieved."
        )

    prompt = build_qa_prompt(question, passages)

    result = generate(prompt, QA_SCHEMA)

    return {
        "answer": result["answer"],
        "sources": [
            {
                "chapter": p.get("chapter_no"),
                "chunk_id": p["chunk_id"]
            }
            for p in passages
        ]
    }