from pydantic import BaseModel, Field

class CandidateEvaluationSchema(BaseModel):
    candidate_name: str = Field(..., description="Full name extracted from candidate resume")
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    deterministic_match_score: float = Field(..., description="Match percentage score (0-100)")
    years_of_experience: float = Field(default=0.0)
    summary: str = Field(..., description="Clean LLM narrative summary of candidate background")
    reasoning: str = Field(..., description="Evaluation summary explanation")
    
class BatchEvaluationResponseSchema(BaseModel):
    total_candidates: int = Field(..., description="Total Number of evaluated resumes")
    role_title: str = Field(..., description="Target role title")
    ranked_candidates: list[CandidateEvaluationSchema] = Field(
        ..., description= "List of candidates sorted in descending order by match score"
    )

class CandidateEvaluationSchema(BaseModel):
    candidate_name: str = Field(..., description="Full name extracted from candidate resume")
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    deterministic_match_score: float = Field(..., description="Match percentage score (0-100)")
    years_of_experience: float = Field(default=0.0)
    hiring_verdict: str = Field(..., description="'Strong Hire', 'Consider', or 'Pass'")
    summary: str = Field(..., description="HR Recruiter summary of candidate background")
    reasoning: str = Field(..., description="Evaluation summary explanation")


class BatchEvaluationResponseSchema(BaseModel):
    total_candidates: int
    role_title: str
    ranked_candidates: list[CandidateEvaluationSchema]