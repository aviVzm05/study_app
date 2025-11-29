import pytest
import os
import json
from unittest.mock import patch, MagicMock
from services.llm_service import LLMService

# Sample valid response from LLM
MOCK_LLM_RESPONSE_TEXT = json.dumps([
    {
        "question_text": "What is the capital of France?",
        "possible_answers": ["Berlin", "Madrid", "Paris", "Rome"],
        "correct_answer": "Paris",
        "explanation": "Paris is the capital and most populous city of France.",
        "subject": "Geography",
        "difficulty_band": "Beginner"
    }
])

@pytest.fixture(autouse=True)
def mock_genai_configure():
    """Mocks genai.configure to prevent actual API calls."""
    with patch('google.generativeai.configure') as mock_configure:
        yield mock_configure

@pytest.fixture
def mock_generative_model():
    """Mocks the genai.GenerativeModel instance."""
    with patch('google.generativeai.GenerativeModel') as MockModel:
        mock_instance = MockModel.return_value
        mock_response = MagicMock()
        mock_response.text = MOCK_LLM_RESPONSE_TEXT
        mock_instance.generate_content.return_value = mock_response
        yield mock_instance

def test_llm_service_initialization_success(mock_genai_configure):
    """Tests if LLMService initializes successfully with a valid API key."""
    os.environ["GEMINI_API_KEY"] = "fake_api_key"
    LLMService._model = None # Reset model for fresh initialization
    LLMService.initialize()
    mock_genai_configure.assert_called_once_with(api_key="fake_api_key")
    assert LLMService._model is not None
    del os.environ["GEMINI_API_KEY"]

def test_llm_service_initialization_no_api_key():
    """Tests if LLMService raises ValueError when API key is not set."""
    if "GEMINI_API_KEY" in os.environ:
        del os.environ["GEMINI_API_KEY"]
    LLMService._model = None
    with pytest.raises(ValueError, match="GEMINI_API_KEY environment variable not set."):
        LLMService.initialize()

def test_generate_question_success(mock_generative_model):
    """Tests if generate_question returns correctly parsed questions."""
    os.environ["GEMINI_API_KEY"] = "fake_api_key" # Needed for get_model to not raise ValueError
    LLMService._model = mock_generative_model # Ensure the mock is used
    
    questions = LLMService.generate_question(
        subject="Math", 
        difficulty_band="Beginner", 
        num_questions=1
    )

    assert isinstance(questions, list)
    assert len(questions) == 1
    assert questions[0]["question_text"] == "What is the capital of France?"
    assert questions[0]["correct_answer"] == "Paris"
    mock_generative_model.generate_content.assert_called_once()
    del os.environ["GEMINI_API_KEY"]

def test_generate_question_malformed_json(mock_generative_model):
    """Tests if generate_question handles malformed JSON responses."""
    os.environ["GEMINI_API_KEY"] = "fake_api_key"
    LLMService._model = mock_generative_model
    mock_generative_model.generate_content.return_value.text = "This is not JSON"

    with pytest.raises(json.JSONDecodeError):
        LLMService.generate_question(subject="Math", difficulty_band="Beginner")
    del os.environ["GEMINI_API_KEY"]

def test_generate_question_llm_error(mock_generative_model):
    """Tests if generate_question re-raises LLM related exceptions."""
    os.environ["GEMINI_API_KEY"] = "fake_api_key"
    LLMService._model = mock_generative_model
    mock_generative_model.generate_content.side_effect = Exception("LLM connection error")

    with pytest.raises(Exception, match="LLM connection error"):
        LLMService.generate_question(subject="Math", difficulty_band="Beginner")
    del os.environ["GEMINI_API_KEY"]

def test_generate_question_retry_logic():
    """Tests if generate_question attempts retries on failure."""
    os.environ["GEMINI_API_KEY"] = "fake_api_key"
    LLMService._model = None # Force re-init to ensure mock is fresh
    with patch('google.generativeai.GenerativeModel') as MockModel:
        mock_instance = MockModel.return_value
        mock_instance.generate_content.side_effect = [Exception("Transient error"), Exception("Another transient error"), MagicMock(text=MOCK_LLM_RESPONSE_TEXT)]
        LLMService._model = mock_instance # Assign the mock
        
        with patch('time.sleep') as mock_sleep:
            questions = LLMService.generate_question(subject="Math", difficulty_band="Beginner")
            assert len(questions) == 1
            assert mock_instance.generate_content.call_count == 3
            assert mock_sleep.call_count == 2
    del os.environ["GEMINI_API_KEY"]

def test_generate_question_retry_exhausted():
    """Tests if generate_question raises exception after exhausting retries."""
    os.environ["GEMINI_API_KEY"] = "fake_api_key"
    LLMService._model = None # Force re-init to ensure mock is fresh
    with patch('google.generativeai.GenerativeModel') as MockModel:
        mock_instance = MockModel.return_value
        mock_instance.generate_content.side_effect = [Exception("Error 1")] * LLMService._MAX_RETRIES
        LLMService._model = mock_instance # Assign the mock
        
        with patch('time.sleep') as mock_sleep:
            with pytest.raises(Exception, match="Error 1"):
                LLMService.generate_question(subject="Math", difficulty_band="Beginner")
            assert mock_instance.generate_content.call_count == LLMService._MAX_RETRIES
            assert mock_sleep.call_count == LLMService._MAX_RETRIES -1
    del os.environ["GEMINI_API_KEY"]
