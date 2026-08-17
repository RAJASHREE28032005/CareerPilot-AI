from models.schemas import CandidateProfile
from models.jd_schemas import JobProfile
from models.match_schemas import MatchResult


# =========================================================
# NORMALIZE SKILLS
# =========================================================

def normalize_skill(skill: str) -> str:

    skill = skill.strip().lower()

    # Replace common symbols
    skill = skill.replace("&", "and")

    # Normalize spaces
    skill = " ".join(skill.split())

    # Common skill variations / aliases
    replacements = {

        # -------------------------------------------------
        # DATA STRUCTURES / ALGORITHMS
        # -------------------------------------------------

        "dsa":
            "data structures and algorithms",

        "data structures algorithm":
            "data structures and algorithms",

        "data structures & algorithms":
            "data structures and algorithms",

        "data structures and algorithm":
            "data structures and algorithms",

        "data structures and algorithms":
            "data structures and algorithms",

        # -------------------------------------------------
        # OOP
        # -------------------------------------------------

        "oop":
            "object-oriented programming",

        "object oriented programming":
            "object-oriented programming",

        "object-oriented programming":
            "object-oriented programming",

        "object oriented":
            "object-oriented programming",

        # -------------------------------------------------
        # DATABASE
        # -------------------------------------------------

        "dbms":
            "database management systems",

        "database management system":
            "database management systems",

        "database management systems":
            "database management systems",

        "sql database":
            "sql",

        # -------------------------------------------------
        # COMPUTER NETWORKS
        # -------------------------------------------------

        "computer network":
            "computer networks",

        "computer networks":
            "computer networks",

        "cn":
            "computer networks",

        # -------------------------------------------------
        # OPERATING SYSTEM
        # -------------------------------------------------

        "os":
            "operating systems",

        "operating system":
            "operating systems",

        "operating systems":
            "operating systems",

        # -------------------------------------------------
        # JAVASCRIPT
        # -------------------------------------------------

        "js":
            "javascript",

        "javascript":
            "javascript",

        # -------------------------------------------------
        # TYPESCRIPT
        # -------------------------------------------------

        "ts":
            "typescript",

        # -------------------------------------------------
        # PYTHON
        # -------------------------------------------------

        "python programming":
            "python",

        # -------------------------------------------------
        # JAVA
        # -------------------------------------------------

        "java programming":
            "java",

        "core java":
            "java",

        # -------------------------------------------------
        # C++
        # -------------------------------------------------

        "c plus plus":
            "c++",

        "cpp":
            "c++",

        # -------------------------------------------------
        # C#
        # -------------------------------------------------

        "c sharp":
            "c#",

        # -------------------------------------------------
        # SPRING
        # -------------------------------------------------

        "spring boot framework":
            "spring boot",

        # -------------------------------------------------
        # GIT
        # -------------------------------------------------

        "git version control":
            "git",

        "version control":
            "git",

        # -------------------------------------------------
        # MACHINE LEARNING
        # -------------------------------------------------

        "ml":
            "machine learning",

        "machine-learning":
            "machine learning",

        # -------------------------------------------------
        # ARTIFICIAL INTELLIGENCE
        # -------------------------------------------------

        "ai":
            "artificial intelligence",

        "artificial-intelligence":
            "artificial intelligence",

    }

    return replacements.get(skill, skill)


# =========================================================
# CHECK WHETHER TWO SKILLS MATCH
# =========================================================

def skills_match(
    candidate_skill: str,
    job_skill: str
) -> bool:

    candidate = normalize_skill(candidate_skill)
    job = normalize_skill(job_skill)

    # Exact normalized match
    if candidate == job:
        return True

    # -----------------------------------------------------
    # HANDLE SIMPLE CONTAINMENT
    # -----------------------------------------------------

    # Example:
    # "java programming" -> "java"
    # "python programming" -> "python"

    if (
        candidate in job
        and len(candidate) >= 3
    ):
        return True

    if (
        job in candidate
        and len(job) >= 3
    ):
        return True

    return False


# =========================================================
# CALCULATE JOB MATCH
# =========================================================

def calculate_match(
    candidate: CandidateProfile,
    job: JobProfile
) -> MatchResult:

    # -----------------------------------------------------
    # GET SKILLS
    # -----------------------------------------------------

    candidate_skills = [
        normalize_skill(skill)
        for skill in candidate.skills
        if skill and skill.strip()
    ]

    required_skills = [
        normalize_skill(skill)
        for skill in job.required_skills
        if skill and skill.strip()
    ]

    preferred_skills = [
        normalize_skill(skill)
        for skill in job.preferred_skills
        if skill and skill.strip()
    ]

    # Remove duplicates while preserving order
    candidate_skills = list(
        dict.fromkeys(candidate_skills)
    )

    required_skills = list(
        dict.fromkeys(required_skills)
    )

    preferred_skills = list(
        dict.fromkeys(preferred_skills)
    )

    # -----------------------------------------------------
    # MATCH REQUIRED SKILLS
    # -----------------------------------------------------

    matched_required = []

    missing_required = []

    for job_skill in required_skills:

        found = any(
            skills_match(
                candidate_skill,
                job_skill
            )
            for candidate_skill in candidate_skills
        )

        if found:
            matched_required.append(job_skill)
        else:
            missing_required.append(job_skill)

    # -----------------------------------------------------
    # MATCH PREFERRED SKILLS
    # -----------------------------------------------------

    matched_preferred = []

    missing_preferred = []

    for job_skill in preferred_skills:

        found = any(
            skills_match(
                candidate_skill,
                job_skill
            )
            for candidate_skill in candidate_skills
        )

        if found:
            matched_preferred.append(job_skill)
        else:
            missing_preferred.append(job_skill)

    # -----------------------------------------------------
    # CALCULATE REQUIRED SCORE
    # -----------------------------------------------------

    if required_skills:

        required_score = (
            len(matched_required)
            / len(required_skills)
        ) * 80

    else:

        required_score = 80

    # -----------------------------------------------------
    # CALCULATE PREFERRED SCORE
    # -----------------------------------------------------

    if preferred_skills:

        preferred_score = (
            len(matched_preferred)
            / len(preferred_skills)
        ) * 20

    else:

        preferred_score = 20

    # -----------------------------------------------------
    # FINAL SCORE
    # -----------------------------------------------------

    match_percentage = (
        required_score
        + preferred_score
    )

    # -----------------------------------------------------
    # SKILL GAPS
    # -----------------------------------------------------

    skill_gaps = sorted(
        set(missing_required)
        | set(missing_preferred)
    )

    # -----------------------------------------------------
    # RECOMMENDATION
    # -----------------------------------------------------

    if missing_required:

        recommendation = (
            "Focus on the missing required skills "
            "before applying."
        )

    elif missing_preferred:

        recommendation = (
            "You meet the required skills. "
            "Consider learning the preferred skills "
            "to strengthen your profile."
        )

    else:

        recommendation = (
            "Your listed skills match the job "
            "requirements well."
        )

    # -----------------------------------------------------
    # RETURN RESULT
    # -----------------------------------------------------

    return MatchResult(

        match_percentage=round(
            match_percentage,
            2
        ),

        matched_required_skills=sorted(
            matched_required
        ),

        missing_required_skills=sorted(
            missing_required
        ),

        matched_preferred_skills=sorted(
            matched_preferred
        ),

        missing_preferred_skills=sorted(
            missing_preferred
        ),

        skill_gaps=skill_gaps,

        recommendation=recommendation
    )