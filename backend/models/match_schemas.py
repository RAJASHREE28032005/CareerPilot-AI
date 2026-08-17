from typing import List

from pydantic import BaseModel


class MatchResult(BaseModel):
    match_percentage: float

    matched_required_skills: List[str] = []

    missing_required_skills: List[str] = []

    matched_preferred_skills: List[str] = []

    missing_preferred_skills: List[str] = []

    skill_gaps: List[str] = []

    recommendation: str