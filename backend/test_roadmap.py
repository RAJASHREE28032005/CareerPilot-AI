import os

from dotenv import load_dotenv
from google import genai

from services.roadmap_service import generate_learning_roadmap


load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is missing."
    )


client = genai.Client(
    api_key=api_key
)


target_role = "Software Engineer"


current_skills = [
    "C",
    "Java",
    "Python",
    "SQL",
    "Git",
    "GitHub",
    "FastAPI",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "Data Structures & Algorithms",
    "Object-Oriented Programming",
    "Operating Systems",
    "Database Management Systems",
    "Computer Networks"
]


skill_gaps = [
    "AWS",
    "Docker"
]


total_days = 7


roadmap = generate_learning_roadmap(
    client=client,
    target_role=target_role,
    current_skills=current_skills,
    skill_gaps=skill_gaps,
    total_days=total_days
)


print("\n========== LEARNING ROADMAP ==========\n")

print(
    roadmap.model_dump_json(
        indent=2
    )
)

print("\n========== END ==========\n")