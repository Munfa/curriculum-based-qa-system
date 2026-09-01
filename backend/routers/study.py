from fastapi import APIRouter, HTTPException

from backend.dependencies import normalize_chapter, normalize_class
from backend.schemas import CQGenerateRequest, CQGradeRequest, MCQGenerateRequest, MCQGradeRequest, QARequest
from generation_grading.build_CQ import generate_cq
from generation_grading.build_MCQ import generate_mcq
from generation_grading.build_QA import answer_question
from generation_grading.grading import grade_cq, grade_mcq

router = APIRouter(tags=["study"])


@router.post("/qa")
def qa(request: QARequest):
    try:
        return answer_question(normalize_class(request.class_), request.subject, normalize_chapter(request.chapter), request.question)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/mcq/generate")
def mcq_generate(request: MCQGenerateRequest):
    try:
        return generate_mcq(normalize_class(request.class_), request.subject, normalize_chapter(request.chapter), request.difficulty.lower())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/mcq/grade")
def mcq_grade(request: MCQGradeRequest):
    try:
        return grade_mcq(request.question_id, request.selected_option)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/cq/generate")
def cq_generate(request: CQGenerateRequest):
    try:
        return generate_cq(normalize_class(request.class_), request.subject, normalize_chapter(request.chapter), request.difficulty.lower())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/cq/grade")
def cq_grade(request: CQGradeRequest):
    try:
        return grade_cq(request.question_id, request.student_answers)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
