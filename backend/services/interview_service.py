import json

from google import genai

from models.schemas import CandidateProfile
from models.jd_schemas import JobProfile
from models.interview_schemas import InterviewSet


def generate_interview_questions(
    client: genai.Client,
    candidate: CandidateProfile,
    job: JobProfile,
    skill_gaps: list[str] | None = None
) -> InterviewSet:

    candidate_data = candidate.model_dump()
    job_data = job.model_dump()

    if skill_gaps is None:
        skill_gaps = []

    prompt = f"""
You are CareerPilot AI, an expert technical interviewer and
placement preparation assistant.

Generate a personalized interview question set for the candidate
based on the candidate profile and target job.

CANDIDATE PROFILE:

{json.dumps(candidate_data, indent=2)}


TARGET JOB:

{json.dumps(job_data, indent=2)}


SKILL GAPS:

{json.dumps(skill_gaps, indent=2)}


Generate questions in these categories:

1. Technical
2. Project
3. Behavioral


IMPORTANT RULES:

1. Use ONLY information present in the candidate profile and job profile.
2. NEVER invent candidate experience.
3. NEVER invent projects.
4. NEVER claim the candidate has a skill that is not in the profile.
5. Project questions must be based only on projects actually present
   in the candidate profile.
6. Include questions relevant to the required skills of the job.
7. Include questions related to the candidate's skill gaps when useful,
   but do NOT assume the candidate already knows those skills.
8. Include a mixture of Easy, Medium, and Hard questions.
9. Make questions realistic for a college-level Software Engineer
   interview.
10. Do not provide answers yet.
11. Return ONLY valid JSON.
12. Do not use Markdown.
13. Do not include explanations outside the JSON.

Generate approximately 12 questions.

Return exactly this structure:

{{
    "target_role": "",
    "questions": [
        {{
            "question": "",
            "category": "Technical",
            "difficulty": "Easy",
            "expected_topics": []
        }}
    ]
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

    interview_data = json.loads(response_text)

    return InterviewSet.model_validate(interview_data)
