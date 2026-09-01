from fastapi import APIRouter, HTTPException, Query

from backend.dependencies import normalize_class
from retrieval.retrieval import list_chapters, list_classes, list_subjects

router = APIRouter(prefix="/metadata", tags=["metadata"])


@router.get("/classes")
def get_classes():
    return {"classes": list_classes()}


@router.get("/subjects")
def get_subjects(class_: str = Query(..., alias="class")):
    try:
        return {"subjects": list_subjects(normalize_class(class_))}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/chapters")
def get_chapters(class_: str = Query(..., alias="class"), subject: str = Query(...)):
    try:
        raw_chapters = list_chapters(normalize_class(class_), subject)
        chapters = [
            f"Chapter-{chapter['chapter_no']}: {chapter['chapter_title']}"
            if isinstance(chapter, dict) and "chapter_no" in chapter and "chapter_title" in chapter
            else str(chapter)
            for chapter in raw_chapters
        ]
        return {"chapters": chapters}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
