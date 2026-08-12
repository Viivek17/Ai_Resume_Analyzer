import json
import re


def load_skills():
    """Load skills from skills.json."""
    with open("skills.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["skills"]


def extract_skills(text):
    """Find known skills inside text."""

    skills = load_skills()
    found_skills = []

    for skill in skills:

        # Normal word matching
        if re.search(r"\b" + re.escape(skill) + r"\b", text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills


def compare_skills(resume_skills, job_skills):
    """Compare resume skills with job description skills."""

    resume_set = {skill.lower() for skill in resume_skills}
    job_set = {skill.lower() for skill in job_skills}

    matched = [
        skill for skill in job_skills
        if skill.lower() in resume_set
    ]

    missing = [
        skill for skill in job_skills
        if skill.lower() not in resume_set
    ]

    return matched, missing


def calculate_match_score(matched, job_skills):
    """Calculate ATS match score."""

    if not job_skills:
        return 0

    score = (len(matched) / len(job_skills)) * 100

    return round(score)


def analyze_resume(resume_text, job_description=""):
    """Analyze resume against job description."""

    resume_skills = extract_skills(resume_text)

    # If no job description is provided
    if not job_description.strip():

        return {
            "resume_skills": resume_skills,
            "job_skills": [],
            "matched_skills": [],
            "missing_skills": [],
            "score": 0
        }

    job_skills = extract_skills(job_description)

    matched, missing = compare_skills(
        resume_skills,
        job_skills
    )

    score = calculate_match_score(
        matched,
        job_skills
    )

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "score": score
    }