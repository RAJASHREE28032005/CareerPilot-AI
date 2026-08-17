import os

from dotenv import load_dotenv
from google import genai

from utils.resume_parser import extract_resume_text
from services.profile_service import create_candidate_profile


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing.")


client = genai.Client(api_key=api_key)


resume_path = "test_files/sample_resume.pdf"

resume_text = extract_resume_text(resume_path)

profile = create_candidate_profile(
    client=client,
    resume_text=resume_text
)

print("\n========== CANDIDATE PROFILE ==========\n")

print(profile.model_dump_json(indent=2))

print("\n========== END ==========\n")