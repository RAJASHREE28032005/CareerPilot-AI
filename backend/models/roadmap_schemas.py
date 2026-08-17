from typing import List

from pydantic import BaseModel


class RoadmapDay(BaseModel):
    day: int

    skill: str

    topics: List[str] = []

    tasks: List[str] = []


class LearningRoadmap(BaseModel):
    total_days: int

    target_role: str

    skill_gaps: List[str] = []

    roadmap: List[RoadmapDay] = []