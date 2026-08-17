import os

from dotenv import load_dotenv
from google import genai

from models.schemas import CandidateProfile, Education
from models.jd_schemas import JobProfile
from services.resume_service import tailor_resume


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing.")

client = genai.Client(api_key=api_key)


candidate = CandidateProfile(
    name="RAJASHREE BALLA V",
    email="Brajashreeballav744@gmail.com",
    phone="+91-9547637417",

    education=[
        Education(
            institution="St. Thomas’ College of Engineering & Technology",
            degree="Bachelor of Technology",
            field_of_study="Computer Science and Engineering",
            year="2023 – Present",
            score="CGPA: 8.11"
        )
    ],

    skills=[
        "C",
        "Java",
        "Python",
        "SQL",
        "Git",
        "GitHub",
        "VS Code",
        "Google Colab",
        "Jupyter Notebook",
        "FastAPI",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "Isolation Forest",
        "Data Structures & Algorithms",
        "Object-Oriented Programming",
        "Operating Systems",
        "Database Management Systems",
        "Computer Networks"
    ],

    projects=[],
    certifications=[
        "Google Cloud Study Jam (2025)",
        "International Conference Paper Presentation (SMDV 2025)",
        "College Hackathon – CODEFLOW (2026)"
    ],
    interests=[
        "Problem Solving",
        "Machine Learning",
        "Learning New Technologies"
    ],
    experience=[],
    target_roles=[]
)


job = JobProfile(
    job_title="Software Engineer",

    company=None,

    location=None,

    required_skills=[
        "Java",
        "Python",
        "SQL",
        "Data Structures and Algorithms",
        "Computer Networks"
    ],

    preferred_skills=[
        "FastAPI",
        "Docker",
        "AWS"
    ],

    experience_required=None,

    education_required=[
        "Bachelor's degree in Computer Science or a related field."
    ],

    responsibilities=[
        "Develop and maintain software applications.",
        "Write clean and efficient code.",
        "Work with other developers to build software solutions.",
        "Debug and test applications."
    ],

    qualifications=[]
)


tailored_resume = tailor_resume(
    client=client,
    candidate=candidate,
    job=job
)


print("\n========== TAILORED RESUME ==========\n")

print(
    tailored_resume.model_dump_json(
        indent=2
    )
)

print("\n========== END ==========\n")