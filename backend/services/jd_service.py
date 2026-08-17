import json

from google import genai

from models.jd_schemas import JobProfile


def analyze_job_description(
    client: genai.Client,
    job_description: str
) -> JobProfile:

    prompt = f"""
You are CareerPilot AI, an expert Placement and Career Assistant.

Your task is to analyze the provided job description and convert it
into a structured job profile.

IMPORTANT RULES:

1. Use ONLY information explicitly present in the job description.
2. Do NOT invent requirements.
3. Do NOT assume skills that are not mentioned.
4. Separate required skills from preferred skills whenever possible.
5. If information is missing, use null or an empty list.
6. Return ONLY valid JSON.
7. Do not use Markdown.
8. Do not include explanations outside the JSON.

Return JSON using exactly this structure:

{{
    "job_title": null,
    "company": null,
    "location": null,

    "required_skills": [],

    "preferred_skills": [],

    "experience_required": null,

    "education_required": [],

    "responsibilities": [],

    "qualifications": []
}}

JOB DESCRIPTION:

{job_description}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    response_text = response.text.strip()

    # Remove Markdown code fences if Gemini adds them.
    if response_text.startswith("```json"):
        response_text = response_text[7:]

    if response_text.endswith("```"):
        response_text = response_text[:-3]

    response_text = response_text.strip()

    job_data = json.loads(response_text)

    return JobProfile.model_validate(job_data)
