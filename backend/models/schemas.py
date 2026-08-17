from typing import List, Optional

from pydantic import BaseModel


class Education(BaseModel):
    institution: str
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    year: Optional[str] = None
    score: Optional[str] = None


class Project(BaseModel):
    name: str
    description: Optional[str] = None
    technologies: List[str] = []


class CandidateProfile(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None

    education: List[Education] = []

    skills: List[str] = []

    projects: List[Project] = []

    certifications: List[str] = []

    interests: List[str] = []

    experience: List[str] = []

    target_roles: List[str] = []