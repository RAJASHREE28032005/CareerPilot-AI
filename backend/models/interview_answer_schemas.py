from typing import List

from pydantic import BaseModel


class InterviewAnswer(BaseModel):
    question: str
    answer: str
    key_points: List[str] = []
    interview_tip: str


class InterviewAnswerSet(BaseModel):
    target_role: str
    answers: List[InterviewAnswer] = []