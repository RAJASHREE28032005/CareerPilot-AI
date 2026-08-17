import json

from google import genai

from models.schemas import CandidateProfile
from models.jd_schemas import JobProfile
from models.resume_schemas import TailoredResume


def tailor_resume(
    client: genai.Client,
    candidate: CandidateProfile,
    job: JobProfile
) -> TailoredResume:

    candidate_data = candidate.model_dump()
    job_data = job.model_dump()

    prompt = f"""
You are CareerPilot AI, an expert resume tailoring assistant.

Your task is to create a job-targeted resume version using ONLY
information that already exists in the candidate profile.

CANDIDATE PROFILE:

{json.dumps(candidate_data, indent=2)}


TARGET JOB:

{json.dumps(job_data, indent=2)}


IMPORTANT RULES:

1. NEVER invent experience.
2. NEVER invent skills.
3. NEVER invent projects.
4. NEVER invent certifications.
5. NEVER invent job titles.
6. NEVER claim the candidate knows a technology that is not present
   in the candidate profile.
7. Prioritize skills and projects that are relevant to the target job.
8. Rewrite descriptions for relevance and clarity, but preserve
   factual meaning.
9. Do not add Docker or AWS unless they already exist in the
   candidate profile.
10. Keep education and certifications factual.
11. Create a concise professional summary based only on the
    candidate profile.
12. Return ONLY valid JSON.
13. Do not use Markdown.
14. Do not include explanations outside the JSON.

Return exactly this structure:

{{
    "name": "",
    "email": null,
    "phone": null,

    "professional_summary": "",

    "skills": [],

    "education": [],

    "projects": [
        {{
            "name": "",
            "description": "",
            "technologies": []
        }}
    ],

    "certifications": [],

    "experience": []
}}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    response_text = response.text.strip()

    if response_text.startswith("```json"):
        response_text = response_text[7:]

    if response_text.endswith("```"):
        response_text = response_text[:-3]

    response_text = response_text.strip()

    resume_data = json.loads(response_text)

    return TailoredResume.model_validate(resume_data)
