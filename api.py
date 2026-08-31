from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from retrieval.retrieval import list_classes, list_subjects, list_chapters
from generation_grading.build_QA import answer_question
from generation_grading.build_MCQ import generate_mcq
from generation_grading.build_CQ import generate_cq
from generation_grading.grading import grade_mcq, grade_cq

app = FastAPI(
    title="Curriculum-Based Bangla QA System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Metadata
# ============================================================

@app.get("/metadata/classes")
def get_classes():

    return {
        "classes": list_classes()
    }

# @app.get("/metadata/groups")
# def get_groups(class_: str = Query(..., alias="class")):

#     return {
#         "groups": []
#     }


@app.get("/metadata/subjects")
def get_subjects(
    class_: str = Query(..., alias="class"),
    # group: str | None = None
):

    try:
        class_value = (
            int(class_)
            if str(class_).isdigit()
            else class_
        )

        return {
            "subjects":
                list_subjects(class_value)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/metadata/chapters")
def get_chapters(
    class_: str = Query(..., alias="class"),
    subject: str = Query(...),
    # group: str | None = None
):

    try:
        class_value = (
            int(class_)
            if str(class_).isdigit()
            else class_
        )

        raw_chapters =list_chapters(
                        class_value,
                        subject
                    )
        chapters = []
        for ch in raw_chapters:
            if isinstance(ch, dict) and "chapter_no" in ch and "chapter_title" in ch:
                chapters.append(
                    f"Chapter-{ch['chapter_no']}: {ch['chapter_title']}"
                )
            else:
                chapters.append(str(ch))

        return {
            "chapters": chapters
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
def _parse_chapter(chapter_val):
    if isinstance(chapter_val, str) and chapter_val.startswith("Chapter-"):
        try:
            return int(chapter_val.split(":")[0].replace("Chapter-", ""))
        except ValueError:
            pass
    return chapter_val

# ============================================================
# QA
# ============================================================

class QARequest(BaseModel):
    class_: int | str = Field(..., alias="class")
    # group: str | None = None
    subject: str
    chapter: int | str | None = None
    question: str

@app.post("/qa")
def qa(request: QARequest):

    try:
        return answer_question(
            class_number=request.class_,
            subject=request.subject,
            chapter=_parse_chapter(request.chapter),
            question=request.question
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# ============================================================
# MCQ
# ============================================================

class MCQGenerateRequest(BaseModel):
    class_: int | str = Field(..., alias="class")
    # group: str | None = None
    subject: str
    chapter: int | str
    difficulty: str


@app.post("/mcq/generate")
def mcq_generate(request: MCQGenerateRequest):

    try:
        return generate_mcq(
            class_number=request.class_,
            subject=request.subject,
            chapter=_parse_chapter(request.chapter),
            difficulty=request.difficulty
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


class MCQGradeRequest(BaseModel):
    question_id: str
    selected_option: str

@app.post("/mcq/grade")
def mcq_grade(request: MCQGradeRequest):

    try:
        return grade_mcq(
            question_id=request.question_id,
            selected_option=request.selected_option
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# ============================================================
# CQ
# ============================================================

class CQGenerateRequest(BaseModel):
    class_: int | str = Field(..., alias="class")
    # group: str | None = None
    subject: str
    chapter: int | str
    difficulty: str

@app.post("/cq/generate")
def cq_generate(
    request: CQGenerateRequest
):

    try:

        return generate_cq(
            class_number=request.class_,
            subject=request.subject,
            chapter=_parse_chapter(request.chapter),
            difficulty=request.difficulty
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


class CQGradeRequest(BaseModel):

    question_id: str
    student_answers: dict[str, str]


@app.post("/cq/grade")
def cq_grade(
    request: CQGradeRequest
):

    try:

        return grade_cq(
            question_id=request.question_id,
            student_answers=request.student_answers
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )