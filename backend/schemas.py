"""Pydantic request models shared by the API routers."""

from pydantic import BaseModel, Field


class QARequest(BaseModel):
    class_: int | str = Field(..., alias="class")
    subject: str
    chapter: int | str | None = None
    question: str


class MCQGenerateRequest(BaseModel):
    class_: int | str = Field(..., alias="class")
    subject: str
    chapter: int | str
    difficulty: str


class MCQGradeRequest(BaseModel):
    question_id: str
    selected_option: str


class CQGenerateRequest(BaseModel):
    class_: int | str = Field(..., alias="class")
    subject: str
    chapter: int | str
    difficulty: str


class CQGradeRequest(BaseModel):
    question_id: str
    student_answers: dict[str, str]
