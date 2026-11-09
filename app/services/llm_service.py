import json
import os
from pydantic import BaseModel, Field
from groq import Groq


class CandidateLLMInfo(BaseModel):
    candidate_name: str = Field(description="Candidate's full name extracted from resume")
    extracted_skills: list[str] = Field(default_factory=list, description="All technical/hard skills mentioned in text")
    years_of_experience: float = Field(default=0.0, description="Total years of professional experience calculated from dates")
    hiring_verdict: str = Field(description="Verdict: 'Strong Hire', 'Consider', or 'Pass'")
    summary: str = Field(description="Detailed HR Recruiter verdict on candidate fit and skill authenticity")


def extract_candidate_info(
    full_resume_text: str, 
    role_title: str = "General Role", 
    required_skills: list[str] = None
) -> CandidateLLMInfo:
    """
    Evaluates the FULL resume text against job requirements to verify genuine skill usage 
    and output a recruiter hiring recommendation.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is missing")

    client = Groq(api_key=api_key)
    skills_str = ", ".join(required_skills) if required_skills else "Not specified"

    system_prompt = """You are an Enterprise Lead Technical Recruiter evaluating a job applicant.
You have access to the ENTIRE resume text.

Analyze the resume rigorously:
1. Verify if required skills are actively demonstrated in work achievements/projects, or merely listed as keywords.
2. Determine total relevant work experience.
3. Assign a hiring_verdict strictly matching one of these strings: "Strong Hire", "Consider", or "Pass".
4. Write a 3-4 sentence recruiter summary covering:
   - Overall role fit & practical skill verification.
   - Core strengths demonstrated in past roles.
   - Gaps, risks, or concerns (if any).

Respond STRICTLY in valid JSON matching this structure:
{
  "candidate_name": "John Doe",
  "extracted_skills": ["Python", "FastAPI", "Docker"],
  "years_of_experience": 3.5,
  "hiring_verdict": "Strong Hire",
  "summary": "John demonstrates hands-on implementation of FastAPI and Docker across two production environments. His 3.5 years of experience directly align with the target role."
}
"""

    user_prompt = f"""
TARGET ROLE: {role_title}
REQUIRED SKILLS: {skills_str}

FULL RESUME TEXT:
{full_resume_text}
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",  # Updated to active Groq model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )

        content = response.choices[0].message.content
        data = json.loads(content)

        verdict = data.get("hiring_verdict", "Consider").strip()
        if verdict not in ["Strong Hire", "Consider", "Pass"]:
            verdict = "Consider"

        return CandidateLLMInfo(
            candidate_name=data.get("candidate_name", "Unknown Candidate"),
            extracted_skills=data.get("extracted_skills", []),
            years_of_experience=float(data.get("years_of_experience", 0.0)),
            hiring_verdict=verdict,
            summary=data.get("summary", "No evaluation generated.")
        )
    except Exception as e:
        return CandidateLLMInfo(
            candidate_name="Parse Error Candidate",
            extracted_skills=[],
            years_of_experience=0.0,
            hiring_verdict="Pass",
            summary=f"Failed to evaluate resume: {str(e)}"
        )