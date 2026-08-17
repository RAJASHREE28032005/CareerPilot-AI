from models.schemas import (
    CandidateProfile,
    Education,
    Project
)

from models.jd_schemas import JobProfile

from services.match_service import calculate_match


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
    certifications=[],
    interests=[],
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

    responsibilities=[],

    qualifications=[]
)


result = calculate_match(
    candidate=candidate,
    job=job
)


print("\n========== MATCH RESULT ==========\n")

print(result.model_dump_json(indent=2))

print("\n========== END ==========\n")