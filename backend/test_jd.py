import os

from dotenv import load_dotenv
from google import genai

from services.jd_service import analyze_job_description


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing.")


client = genai.Client(api_key=api_key)


job_description = """
Software Engineer

We are looking for a graduate Software Engineer to join our team.

Required Skills:
- Java
- Python
- SQL
- Data Structures and Algorithms
- Computer Networks

Preferred Skills:
- FastAPI
- Docker
- AWS

Education:
- Bachelor's degree in Computer Science or a related field.

Responsibilities:
- Develop and maintain software applications.
- Write clean and efficient code.
- Work with other developers to build software solutions.
- Debug and test applications.
"""


job_profile = analyze_job_description(
    client=client,
    job_description=job_description
)


print("\n========== JOB PROFILE ==========\n")

print(job_profile.model_dump_json(indent=2))

print("\n========== END ==========\n")