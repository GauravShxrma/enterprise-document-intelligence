from pydantic import BaseModel, Field

class CandidateResumeSchema(BaseModel):
    candidate_name: str = Field(..., description = "Full Name of the candidate.")
    extracted_skills: list[str] = Field(..., description = "List of techinical/soft skills explicitly stated in the resume")
    years_of_experience: int = Field(default=0, description="Estimated years of experience extracted from work history")
    summary: str = Field(default = "", description="Brief executive summary of candidate background.")