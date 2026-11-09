import pytest 
from app.engines.scoring import evaluate_candidate_skills

def test_evaluate_candidate_skills_matching():
    required = ["Python", "FastAPI", "SQL", "Docker"]
    extracted = ["python", "FastAPI", "SQL", "Git"]

    matched, missing, score = evaluate_candidate_skills(required, extracted)

    assert matched == ["Python","FastAPI","SQL"]
    assert missing == ["Docker"]
    assert score == 75.0

def test_evaluate_candidate_skills_empty_required():
    matched, missing, score = evaluate_candidate_skills([],["Python", "FastAPI"])

    assert matched == []
    assert missing == []
    assert score == 0.0