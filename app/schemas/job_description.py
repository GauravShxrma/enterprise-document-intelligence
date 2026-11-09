from pydantic import BaseModel, Field

class JobDescriptionSchema(BaseModel):
    role_title: str = Field(..., description = "The title of the job position.")
    required_skills: list[str] = Field(..., description = "List of mandatory technical and soft skills.")
    preferred_skills: list[str] = Field(default_factory = list, description = "List of optional/preferred skills.")
    min_experience_years: int = Field(default = 0, ge = 0, description = "Minimum required years of experience")
