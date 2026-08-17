import os

from dotenv import load_dotenv
from google import genai

from models.schemas import CandidateProfile, Education, Project
from models.jd_schemas import JobProfile
from models.interview_schemas import InterviewQuestion, InterviewSet
from services.interview_answer_service import generate_interview_answers


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing.")

client = genai.Client(api_key=api_key)


candidate = CandidateProfile(
    name="RAJASHREE BALLAV",
    email="rajashreeballav744@gmail.com",
    phone="+91-9547637417",

    education=[
        Education(
            institution="St. Thomas’ College of Engineering & Technology",
            degree="Bachelor of Technology",
            field_of_study="Computer Science and Engineering",
            year="2023 – Present",
            score="CGPA: 8.11"
        ),
        Education(
            institution="Garalgacha High School",
            degree="Higher Secondary (WBCHSE)",
            field_of_study=None,
            year="2023",
            score="78.4%"
        ),
        Education(
            institution="Sree Ramkrishna Sishutirtha High School",
            degree="Secondary (WBBSE)",
            field_of_study=None,
            year="2021",
            score="87%"
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

    projects=[
        Project(
            name="AI Bank Statement Analyzer",
            description=(
                "Developed an AI-powered Bank Statement Analyzer "
                "using React, Spring Boot, FastAPI and PostgreSQL "
                "to automate transaction extraction and financial "
                "analysis. Implemented DistilBERT/MiniLM for "
                "transaction categorization and Isolation Forest "
                "for anomaly detection to identify unusual "
                "financial activities. Built interactive dashboards "
                "with AI-generated summaries, spending insights "
                "and recurring transaction analysis."
            ),
            technologies=[
                "React",
                "Spring Boot",
                "FastAPI",
                "PostgreSQL",
                "DistilBERT/MiniLM",
                "Isolation Forest"
            ]
        )
    ],

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


interview_set = InterviewSet(
    target_role="Software Engineer",

    questions=[
        InterviewQuestion(
            question=(
                "Explain the concept of runtime polymorphism in Java "
                "using method overriding."
            ),
            category="Technical",
            difficulty="Easy",
            expected_topics=[
                "Java",
                "Object-Oriented Programming",
                "Polymorphism",
                "Method Overriding"
            ]
        ),

        InterviewQuestion(
            question=(
                "What is the difference between INNER JOIN, LEFT JOIN, "
                "and FULL OUTER JOIN in SQL?"
            ),
            category="Technical",
            difficulty="Medium",
            expected_topics=[
                "SQL",
                "DBMS",
                "Joins"
            ]
        ),

        InterviewQuestion(
            question=(
                "Describe the TCP three-way handshake mechanism."
            ),
            category="Technical",
            difficulty="Medium",
            expected_topics=[
                "Computer Networks",
                "TCP/IP",
                "Handshake"
            ]
        ),

        InterviewQuestion(
            question=(
                "Why did you use Isolation Forest in your "
                "AI Bank Statement Analyzer?"
            ),
            category="Project",
            difficulty="Medium",
            expected_topics=[
                "Isolation Forest",
                "Anomaly Detection",
                "Machine Learning"
            ]
        ),

        InterviewQuestion(
            question=(
                "Why did you use FastAPI in your "
                "AI Bank Statement Analyzer?"
            ),
            category="Project",
            difficulty="Easy",
            expected_topics=[
                "FastAPI",
                "API Development"
            ]
        ),

        InterviewQuestion(
            question=(
                "Why are you interested in the Software Engineer role?"
            ),
            category="Behavioral",
            difficulty="Easy",
            expected_topics=[
                "Motivation",
                "Career Goals"
            ]
        )
    ]
)


answer_set = generate_interview_answers(
    client=client,
    candidate=candidate,
    job=job,
    interview_set=interview_set
)


print("\n========== INTERVIEW ANSWERS ==========\n")

print(
    answer_set.model_dump_json(
        indent=2
    )
)

print("\n========== END ==========\n")