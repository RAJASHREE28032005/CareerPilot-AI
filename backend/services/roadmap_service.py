import json

from google import genai

from models.roadmap_schemas import LearningRoadmap


def generate_learning_roadmap(
    client: genai.Client,
    target_role: str,
    current_skills: list[str],
    skill_gaps: list[str],
    total_days: int
) -> LearningRoadmap:

    prompt = f"""
You are CareerPilot AI, an expert Placement and Career Assistant.

Create a practical learning roadmap for a candidate preparing
for a specific target job.

TARGET ROLE:
{target_role}

CURRENT SKILLS:
{current_skills}

SKILL GAPS:
{skill_gaps}

AVAILABLE DAYS:
{total_days}

IMPORTANT RULES:

1. Focus primarily on the identified skill gaps.
2. Do not create unnecessary learning topics unrelated to the gaps.
3. Use the candidate's existing skills as prerequisites when useful.
4. Prioritize required skills over preferred skills.
5. Divide the preparation across exactly {total_days} days.
6. Each day must contain practical topics and actionable tasks.
7. Keep the workload realistic for a college student.
8. Do not claim that the candidate already knows a skill unless it
   appears in CURRENT SKILLS.
9. Do not invent certifications, courses, or achievements.
10. Return ONLY valid JSON.
11. Do not use Markdown.
12. Do not include explanations outside the JSON.

Return exactly this structure:

{{
    "total_days": {total_days},

    "target_role": "{target_role}",

    "skill_gaps": {json.dumps(skill_gaps)},

    "roadmap": [
        {{
            "day": 1,
            "skill": "",
            "topics": [],
            "tasks": []
        }}
    ]
}}

Make sure the roadmap contains exactly {total_days} days.
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


    roadmap_data = json.loads(response_text)


    return LearningRoadmap.model_validate(
        roadmap_data
    )
