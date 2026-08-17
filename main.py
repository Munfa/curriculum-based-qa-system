import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from retrieval.retrieval import retrieve_passage, retrieve, list_chapters, list_classes, list_subjects

from generation_grading.build_QA import answer_question
from generation_grading.build_MCQ import generate_mcq
from generation_grading.build_CQ import generate_cq


CLASS = 6
SUBJECT = "Science"
CHAPTER = 5


# -------------------------
# QA
# -------------------------

question = "সালোকসংশ্লেষণ কী"

qa_result = answer_question(
    CLASS,
    SUBJECT,
    CHAPTER,
    question
)

print("\n===== QA =====")
print(qa_result)


# -------------------------
# MCQ
# -------------------------

mcq_result = generate_mcq(
    CLASS,
    SUBJECT,
    CHAPTER,
    "medium"
)

print("\n===== MCQ =====")
print(mcq_result)


# -------------------------
# CQ
# -------------------------

cq_result = generate_cq(
    CLASS,
    SUBJECT,
    CHAPTER,
    "medium"
)

print("\n===== CQ =====")
print(cq_result)


# -------------------------
# classes, subjects, chapters
# -------------------------
classes = list_classes()
print("Classes: ", classes)

subjects = list_subjects(CLASS)
print(f"Subjects of class {CLASS}: ", subjects)

chapters = list_chapters(CLASS, SUBJECT)
print(f"Chapters of {SUBJECT} of class-{CLASS}: ", chapters)

