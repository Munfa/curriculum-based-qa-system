"""Direct end-to-end smoke test for retrieval and generation."""

from generation_grading.build_CQ import generate_cq
from generation_grading.build_MCQ import generate_mcq
from generation_grading.build_QA import answer_question
from retrieval.retrieval import list_chapters, list_classes, list_subjects


def main() -> None:
    class_number = 6
    subject = "Science"
    chapter = 5

    print("Classes:", list_classes())
    print(f"Subjects of class {class_number}:", list_subjects(class_number))
    print(f"Chapters of {subject}:", list_chapters(class_number, subject))
    print("QA:", answer_question(class_number, subject, chapter, "সালোকসংশ্লেষণ কী"))
    print("MCQ:", generate_mcq(class_number, subject, chapter, "medium"))
    print("CQ:", generate_cq(class_number, subject, chapter, "medium"))


if __name__ == "__main__":
    main()
