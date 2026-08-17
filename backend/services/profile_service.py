import json
import re

from google import genai

from models.schemas import CandidateProfile


def create_candidate_profile(
    client: genai.Client,
    resume_text: str
) -> CandidateProfile:

    prompt = f"""
You are CareerPilot AI, an expert Placement and Career Assistant.

Your task is to extract a structured candidate profile from the
provided resume.

IMPORTANT RULES:

1. Use ONLY information explicitly present in the resume.
2. Do NOT invent skills, experience, education, projects,
   certifications, or achievements.
3. If information is missing, use an empty list or null.
4. Preserve the candidate's actual information.
5. Return ONLY valid JSON.
6. Do not include Markdown.
7. Do not include explanations outside the JSON.

Return JSON using exactly this structure:

{{
    "name": "",
    "email": null,
    "phone": null,

    "education": [
        {{
            "institution": "",
            "degree": null,
            "field_of_study": null,
            "year": null,
            "score": null
        }}
    ],

    "skills": [],

    "projects": [
        {{
            "name": "",
            "description": null,
            "technologies": []
        }}
    ],

    "certifications": [],

    "interests": [],

    "experience": [],

    "target_roles": []
}}

RESUME:

{resume_text}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    response_text = response.text.strip()

    # Remove accidental Markdown code fences if Gemini adds them.
    if response_text.startswith("```json"):
        response_text = response_text[7:]

    if response_text.endswith("```"):
        response_text = response_text[:-3]

    response_text = response_text.strip()

    profile_data = json.loads(response_text)

    return CandidateProfile.model_validate(profile_data)
