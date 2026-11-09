import pytest 
from unittest.mock import MagicMock, patch
from app.services.llm_service import extract_candidate_info
from app.schemas.resume import CandidateResumeSchema

def test_extract_candidate_info_missing_api_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising = False)

    with pytest.raises(ValueError) as exc_info:
        extract_candidate_info(["Sample chunk context"])

    assert "GROQ_API_KEY environment variable is missing" in str(exc_info.value)

@patch("app.services.llm_service.Groq")
def test_extract_candidate_info_success(mock_groq_Class, monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY","mock_key_12345")

    mock_json_payload = (
        '{"candidate_name": "Jane Doe", '
        '"extracted_skills": ["Python", "FastAPI", "Docker"], '
        '"years_of_experience": 4, '
        '"summary": "Backend software engineer."}'
    )

    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = mock_json_payload

    mock_client_instance = MagicMock()
    mock_client_instance.chat.completions.create.return_value = mock_response
    mock_groq_Class.return_value = mock_client_instance

    context = ["Jane Doe is a software engineer with 4 years in Python, FastAPI, Docker."]
    result = extract_candidate_info(context)

    assert isinstance(result, CandidateResumeSchema)
    assert result.candidate_name == "Jane Doe"
    assert result.extracted_skills == ["Python", "FastAPI", "Docker"]
    assert result.years_of_experience == 4