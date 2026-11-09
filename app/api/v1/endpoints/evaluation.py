import os
import shutil
import tempfile
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.engines.ingestion import extract_text
from app.engines.chunker import chunk_text
from app.engines.vector_store import VectorStoreManager
from app.engines.scoring import evaluate_candidate_skills
from app.services.llm_service import extract_candidate_info
from app.schemas.evaluation import CandidateEvaluationSchema, BatchEvaluationResponseSchema

router = APIRouter()
vector_store = VectorStoreManager()


@router.post("/evaluate", response_model=CandidateEvaluationSchema)
async def evaluate_candidate(
    role_title: str = Form(...),
    required_skills: str = Form(..., description="Comma-separated list of required skills"),
    file: UploadFile = File(...)
):
    """
    Upload a single resume file (PDF/DOCX) alongside job requirements to receive
    a deterministic match score and structured skill analysis.
    """
    req_skills_list = [s.strip() for s in required_skills.split(",") if s.strip()]
    if not req_skills_list:
        raise HTTPException(status_code=400, detail="At least one required skill must be provided.")

    temp_dir = tempfile.mkdtemp()
    temp_file_path = Path(temp_dir) / file.filename

    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        raw_text = extract_text(temp_file_path)
        if not raw_text or not raw_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract readable text from file.")

        # Full Document LLM HR Evaluation
        candidate_data = extract_candidate_info(
            full_resume_text=raw_text,
            role_title=role_title,
            required_skills=req_skills_list
        )

        candidate_name = candidate_data.candidate_name.strip() or Path(file.filename).stem.replace("_", " ").title()

        matched_skills, missing_skills, score = evaluate_candidate_skills(
            required_skills=req_skills_list,
            extracted_skills=candidate_data.extracted_skills
        )

        reasoning = (
            f"Extracted {candidate_data.years_of_experience} years of experience. "
            f"Matched {len(matched_skills)} of {len(req_skills_list)} required skills."
        )

        return CandidateEvaluationSchema(
            candidate_name=candidate_name,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            deterministic_match_score=score,
            years_of_experience=candidate_data.years_of_experience,
            hiring_verdict=candidate_data.hiring_verdict,
            summary=candidate_data.summary,
            reasoning=reasoning
        )

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal engine evaluation error: {str(e)}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@router.post("/evaluate-batch", response_model=BatchEvaluationResponseSchema)
async def evaluate_candidate_batch(
    role_title: str = Form(...),
    required_skills: str = Form(..., description="Comma-separated list of required skills"),
    files: list[UploadFile] = File(..., description="Multiple PDF or DOCX resume files")
):
    """
    Evaluates multiple candidate resumes against job requirements and returns
    a ranked list sorted by match score.
    """
    req_skills_list = [s.strip() for s in required_skills.split(",") if s.strip()]
    if not req_skills_list:
        raise HTTPException(status_code=400, detail="At least one required skill must be provided.")

    if not files:
        raise HTTPException(status_code=400, detail="At least one file must be uploaded.")

    evaluations: list[CandidateEvaluationSchema] = []

    for file in files:
        temp_dir = tempfile.mkdtemp()
        temp_file_path = Path(temp_dir) / file.filename

        try:
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            raw_text = extract_text(temp_file_path)
            if not raw_text or not raw_text.strip():
                print(f"⚠️ Empty text extracted from file '{file.filename}'")
                continue

            # Full Document LLM HR Evaluation
            candidate_data = extract_candidate_info(
                full_resume_text=raw_text,
                role_title=role_title,
                required_skills=req_skills_list
            )

            candidate_name = candidate_data.candidate_name.strip() or Path(file.filename).stem.replace("_", " ").title()

            matched_skills, missing_skills, score = evaluate_candidate_skills(
                required_skills=req_skills_list,
                extracted_skills=candidate_data.extracted_skills
            )

            reasoning = (
                f"Extracted {candidate_data.years_of_experience} years of experience. "
                f"Matched {len(matched_skills)} of {len(req_skills_list)} required skills."
            )

            evaluations.append(
                CandidateEvaluationSchema(
                    candidate_name=candidate_name,
                    matched_skills=matched_skills,
                    missing_skills=missing_skills,
                    deterministic_match_score=score,
                    years_of_experience=candidate_data.years_of_experience,
                    hiring_verdict=candidate_data.hiring_verdict,
                    summary=candidate_data.summary,
                    reasoning=reasoning
                )
            )

        except Exception as e:
            print(f"❌ Error processing file '{file.filename}': {str(e)}")
            continue
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    # Sort candidates in descending order by deterministic_match_score
    ranked = sorted(evaluations, key=lambda c: c.deterministic_match_score, reverse=True)

    return BatchEvaluationResponseSchema(
        total_candidates=len(ranked),
        role_title=role_title,
        ranked_candidates=ranked
    )