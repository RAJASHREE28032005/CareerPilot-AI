import json
import time

from google import genai
from google.genai import errors

from models.schemas import CandidateProfile
from models.jd_schemas import JobProfile
from models.interview_schemas import InterviewSet
from models.interview_answer_schemas import InterviewAnswerSet


def generate_interview_answers(
    client: genai.Client,
    candidate: CandidateProfile,
    job: JobProfile,
    interview_set: InterviewSet
) -> InterviewAnswerSet:

    candidate_data = candidate.model_dump()
    job_data = job.model_dump()
    questions_data = interview_set.model_dump()

    prompt = f"""
You are CareerPilot AI, an expert interview preparation assistant.

Your task is to generate personalized interview answers for the
candidate based on the candidate profile, target job, and interview
questions.

CANDIDATE PROFILE:

{json.dumps(candidate_data, indent=2)}


TARGET JOB:

{json.dumps(job_data, indent=2)}


INTERVIEW QUESTIONS:

{json.dumps(questions_data, indent=2)}


IMPORTANT RULES:

1. Use ONLY information explicitly present in the candidate profile
   when answering questions about the candidate.

2. NEVER invent work experience.

3. NEVER invent project implementation details.

4. NEVER invent achievements, responsibilities, technologies,
   certifications, or results.

5. For technical questions that test general knowledge, provide a
   correct educational answer.

6. For project questions, clearly distinguish between:
   - facts explicitly present in the candidate profile
   - general technical explanations.

7. If a project question asks for a detail that is NOT explicitly
   present in the candidate profile, do NOT present a guessed reason,
   implementation detail, performance result, architecture decision,
   configuration, metric, or challenge as something the candidate
   actually did.

8. For missing project details, use wording such as:
   "The profile confirms that X was used, but it does not specify
   the exact reason or implementation detail. In an interview,
   explain your actual reason."

9. Clearly distinguish between:
   - "The project profile states..." = confirmed fact.
   - "Generally, this technology is used for..." = general knowledge.
   - "You can explain that..." = interview guidance.

10. Never convert general technical knowledge into a personal
    claim about the candidate's project.

11. Answers should sound natural when spoken in an interview.

12. Keep answers concise but sufficiently detailed.

13. Avoid unnecessarily complicated vocabulary.

14. Provide useful key points for each answer.

15. Provide one practical interview tip for each answer.

16. Do not claim that AWS or Docker experience exists unless it is
    explicitly present in the candidate profile.

17. Return ONLY valid JSON.

18. Do not use Markdown.

19. Do not include explanations outside the JSON.

Return exactly this structure:

{{
    "target_role": "{job.job_title}",
    "answers": [
        {{
            "question": "",
            "answer": "",
            "key_points": [],
            "interview_tip": ""
        }}
    ]
}}
"""

    # Try the Gemini request up to 3 times if the server temporarily
    # returns a 503 error.
    response = None

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )
            break

        except errors.ClientError as e:

            # 429 means the API quota has been exceeded.
            # Retrying immediately will not solve the problem.
            if getattr(e, "status_code", None) == 429:
                raise RuntimeError(
                    "Gemini API quota exceeded. "
                    "Please wait for the quota to reset or check "
                    "your Gemini API usage and billing limits."
                ) from e

            # Any other client error should be raised normally.
            raise

        except errors.ServerError as e:

            # We only retry temporary 503 server errors.
            if getattr(e, "status_code", None) != 503:
                raise

            # Last attempt failed.
            if attempt == 2:
                raise

            # Wait 1 second, then 2 seconds.
            wait_time = 2 ** attempt

            print(
                f"Gemini server temporarily unavailable. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)

    # Make sure a response was actually received.
    if response is None:
        raise RuntimeError(
            "Failed to receive a response from Gemini."
        )

    response_text = response.text.strip()

    # Remove accidental Markdown code fences.
    if response_text.startswith("```json"):
        response_text = response_text[7:]

    if response_text.endswith("```"):
        response_text = response_text[:-3]

    response_text = response_text.strip()

    answer_data = json.loads(response_text)

    return InterviewAnswerSet.model_validate(answer_data)
