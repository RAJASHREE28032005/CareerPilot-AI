from typing import List, Optional

from pydantic import BaseModel


class TailoredEducation(BaseModel):
    institution: str
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    year: Optional[str] = None
    score: Optional[str] = None


class TailoredProject(BaseModel):
    name: str
    description: str
    technologies: List[str] = []


class TailoredResume(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None

    professional_summary: str

    skills: List[str] = []

    education: List[TailoredEducation] = []

    projects: List[TailoredProject] = []

    certifications: List[str] = []

    experience: List[str] = []