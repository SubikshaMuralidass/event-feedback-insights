from unittest.mock import MagicMock, patch
from app.services.llm import summarize_feedback

@patch("app.services.llm.client")
def test_summarize_feedback_success(mock_client):
    # Fake Gemini response
    fake_response = MagicMock()
    fake_response.text = "Great event overall"

    mock_client.models.generate_content.return_value = fake_response

    comments = ["Nice", "Well organized"]

    result = summarize_feedback(comments)

    assert "Great event" in result
