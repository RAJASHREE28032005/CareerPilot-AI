import json

from google import genai

from models.schemas import CandidateProfile
from models.jd_schemas import JobProfile
from models.cover_letter_schemas import CoverLetter


def generate_cover_letter(
    client: genai.Client,
    candidate: CandidateProfile,
    job: JobProfile
) -> CoverLetter:

    candidate_data = candidate.model_dump()
    job_data = job.model_dump()

    prompt = f"""
You are CareerPilot AI, an expert career and placement assistant.

Create a professional, concise, personalized cover letter for the
candidate based on the target job.

CANDIDATE PROFILE:

{json.dumps(candidate_data, indent=2)}


TARGET JOB:

{json.dumps(job_data, indent=2)}


IMPORTANT RULES:

1. Use ONLY information present in the candidate profile.
2. NEVER invent work experience.
3. NEVER invent skills.
4. NEVER invent projects.
5. NEVER invent certifications.
6. NEVER claim that the candidate has AWS, Docker, or any other
   technology unless it exists in the candidate profile.
7. Highlight the candidate's skills that are relevant to the job.
8. Mention relevant academic projects when useful.
9. Keep the tone professional and suitable for a job application.
10. Do not exaggerate the candidate's experience.
11. Do not mention the candidate's weaknesses or missing skills.
12. If the company name is unavailable, do not invent one.
13. If the recipient is unknown, use "Hiring Manager".
14. Return ONLY valid JSON.
15. Do not use Markdown.
16. Do not include explanations outside the JSON.

Return exactly this structure:

{{
    "recipient": "",
    "subject": "",
    "greeting": "",
    "body": "",
    "closing": ""
}}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    response_text = response.text.strip()

    # Remove accidental Markdown code fences.
    if response_text.startswith("```json"):
        response_text = response_text[7:]

    if response_text.endswith("```"):
        response_text = response_text[:-3]

    response_text = response_text.strip()

    letter_data = json.loads(response_text)

    return CoverLetter.model_validate(letter_data)
