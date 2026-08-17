import os
import tempfile

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from pydantic import BaseModel

from utils.resume_parser import extract_resume_text

from services.profile_service import create_candidate_profile
from services.jd_service import analyze_job_description
from services.match_service import calculate_match
from services.roadmap_service import generate_learning_roadmap
from services.resume_service import tailor_resume
from services.cover_letter_service import generate_cover_letter
from services.interview_service import generate_interview_questions
from services.interview_answer_service import generate_interview_answers

from models.schemas import CandidateProfile
from models.jd_schemas import JobProfile
from models.interview_schemas import InterviewSet


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Check your .env file."
    )


# =========================================================
# CREATE GEMINI CLIENT
# =========================================================

client = genai.Client(api_key=api_key)


# =========================================================
# CREATE FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="CareerPilot AI",
    description="AI-powered Career and Placement Assistant",
    version="1.0.0"
)


# =========================================================
# CORS CONFIGURATION
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# ROADMAP REQUEST MODEL
# =========================================================

class RoadmapRequest(BaseModel):
    target_role: str
    current_skills: list[str]
    skill_gaps: list[str]
    total_days: int


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "message": "CareerPilot AI API is running!"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =========================================================
# PROFILE ANALYSIS
# =========================================================

@app.post("/profile/analyze")
async def analyze_profile(
    file: UploadFile = File(...)
):

    # -----------------------------------------------------
    # CHECK FILE NAME
    # -----------------------------------------------------

    filename = file.filename or ""

    if not filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX resumes are supported."
        )

    # -----------------------------------------------------
    # READ UPLOADED FILE
    # -----------------------------------------------------

    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded resume is empty."
        )

    # -----------------------------------------------------
    # CREATE TEMPORARY FILE
    # -----------------------------------------------------

    suffix = os.path.splitext(filename)[1]

    temp_file_path = None

    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(file_bytes)
            temp_file_path = temp_file.name

        # -------------------------------------------------
        # EXTRACT RESUME TEXT
        # -------------------------------------------------

        resume_text = extract_resume_text(
            temp_file_path
        )

        if not resume_text or not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the resume."
            )

        # -------------------------------------------------
        # GENERATE CANDIDATE PROFILE
        # -------------------------------------------------

        profile = create_candidate_profile(
            client=client,
            resume_text=resume_text
        )

        # -------------------------------------------------
        # RETURN RESULT
        # -------------------------------------------------

        return {
            "filename": filename,
            "profile": profile.model_dump()
        }

    except HTTPException:
        raise

    except Exception as e:

        print(
            "ERROR while analyzing resume:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        # -------------------------------------------------
        # DELETE TEMPORARY FILE
        # -------------------------------------------------

        if (
            temp_file_path
            and os.path.exists(temp_file_path)
        ):
            os.remove(temp_file_path)


# =========================================================
# JOB DESCRIPTION ANALYSIS
# =========================================================

@app.post("/jobs/analyze")
async def analyze_job(
    job_description: str | dict
):

    try:

        # -------------------------------------------------
        # SUPPORT BOTH STRING AND OBJECT INPUT
        # -------------------------------------------------

        if isinstance(job_description, dict):

            text = job_description.get(
                "job_description",
                ""
            )

        else:

            text = job_description

        if not text or not text.strip():

            raise HTTPException(
                status_code=400,
                detail="Job description cannot be empty."
            )

        # -------------------------------------------------
        # ANALYZE JOB DESCRIPTION
        # -------------------------------------------------

        job = analyze_job_description(
            client=client,
            job_description=text
        )

        return job.model_dump()

    except HTTPException:
        raise

    except Exception as e:

        print(
            "ERROR while analyzing job description:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# JOB MATCHING
# =========================================================

@app.post("/jobs/match")
async def match_candidate_to_job(
    candidate: CandidateProfile,
    job: JobProfile
):

    try:

        result = calculate_match(
            candidate=candidate,
            job=job
        )

        return result.model_dump()

    except Exception as e:

        print(
            "ERROR while calculating job match:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# LEARNING ROADMAP
# =========================================================

@app.post("/roadmap/generate")
async def generate_roadmap(
    request: RoadmapRequest
):

    if request.total_days < 1:

        raise HTTPException(
            status_code=400,
            detail="total_days must be at least 1."
        )

    if request.total_days > 365:

        raise HTTPException(
            status_code=400,
            detail="total_days cannot exceed 365."
        )

    try:

        roadmap = generate_learning_roadmap(
            client=client,
            target_role=request.target_role,
            current_skills=request.current_skills,
            skill_gaps=request.skill_gaps,
            total_days=request.total_days
        )

        return roadmap.model_dump()

    except Exception as e:

        print(
            "ERROR while generating roadmap:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# TAILOR RESUME
# =========================================================

@app.post("/resume/tailor")
async def tailor_candidate_resume(
    candidate: CandidateProfile,
    job: JobProfile
):

    try:

        tailored_resume = tailor_resume(
            client=client,
            candidate=candidate,
            job=job
        )

        return tailored_resume.model_dump()

    except Exception as e:

        print(
            "ERROR while tailoring resume:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# COVER LETTER
# =========================================================

@app.post("/cover-letter/generate")
async def generate_candidate_cover_letter(
    candidate: CandidateProfile,
    job: JobProfile
):

    try:

        cover_letter = generate_cover_letter(
            client=client,
            candidate=candidate,
            job=job
        )

        return cover_letter.model_dump()

    except Exception as e:

        print(
            "ERROR while generating cover letter:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# INTERVIEW QUESTIONS
# =========================================================

@app.post("/interview/generate")
async def generate_interview(
    candidate: CandidateProfile,
    job: JobProfile,
    skill_gaps: list[str] = []
):

    try:

        interview_set = generate_interview_questions(
            client=client,
            candidate=candidate,
            job=job,
            skill_gaps=skill_gaps
        )

        return interview_set.model_dump()

    except Exception as e:

        print(
            "ERROR while generating interview questions:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# INTERVIEW ANSWERS
# =========================================================

@app.post("/interview/answers")
async def generate_interview_answers_endpoint(
    candidate: CandidateProfile,
    job: JobProfile,
    interview_set: InterviewSet
):

    try:

        answer_set = generate_interview_answers(
            client=client,
            candidate=candidate,
            job=job,
            interview_set=interview_set
        )

        return answer_set.model_dump()

    except Exception as e:

        print(
            "ERROR while generating interview answers:",
            repr(e)
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )