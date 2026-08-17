from typing import List, Optional

from pydantic import BaseModel


class JobProfile(BaseModel):
    job_title: Optional[str] = None

    company: Optional[str] = None

    location: Optional[str] = None

    required_skills: List[str] = []

    preferred_skills: List[str] = []

    experience_required: Optional[str] = None

    education_required: List[str] = []

    responsibilities: List[str] = []

    qualifications: List[str] = []