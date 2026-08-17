from .build_MCQ import mcq_ans_store
from .build_CQ import cq_ans_store
from .llm import generate


CQ_GRADING_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "score": {
            "type": "INTEGER"
        },
        "feedback": {
            "type": "STRING"
        }
    },
    "required": [
        "score",
        "feedback"
    ]
}

# ============================================================
# MCQ grading
# ============================================================

def grade_mcq(question_id, selected_option):

    if question_id not in mcq_ans_store:
        raise ValueError("Unknown question_id.")

    correct_option = mcq_ans_store[question_id]["correct_option"]

    correct = (selected_option == correct_option)

    return {
        "score": 1 if correct else 0,
        "correct": correct,
        "feedback":
            "Correct answer."
            if correct
            else "Incorrect answer."
    }

# ============================================================
# CQ grading
# ============================================================

def grade_cq(question_id, student_answers):

    if question_id not in cq_ans_store:
        raise ValueError("Unknown question_id.")

    reference_answers = cq_ans_store[question_id]["reference_answers"]

    results = {}
    total = 0

    for part in ["ka", "kha", "ga", "gha"]:

        student = student_answers.get(part, "")
        reference = reference_answers[part]

        prompt = f"""
            Grade this student's answer to a Bangladeshi
            school textbook question.

            Part: {part}

            Reference answer:
            {reference}

            Student answer:
            {student}

            Evaluate whether the student's answer contains the
            important information required by the reference answer.

            Return a score and concise feedback.

            Use a score from 1 to 4.
        """

        result = generate(prompt, CQ_GRADING_SCHEMA)

        results[part] = {
            "score": result["score"],
            "feedback": result["feedback"]
        }

        total += result["score"]

    results["total"] = total

    return results