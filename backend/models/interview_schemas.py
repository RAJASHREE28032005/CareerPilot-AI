from typing import List


from pydantic import BaseModel


class InterviewQuestion(BaseModel):
    question: str
    category: str
    difficulty: str
    expected_topics: List[str] = []


class InterviewSet(BaseModel):
    target_role: str
    questions: List[InterviewQuestion] = []