import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
from unittest.mock import MagicMock, patch
from src.ui.english_exercise_view import EnglishExerciseView
from services.llm_service import LLMService

# Initialize QApplication once for all tests
@pytest.fixture(scope="session", autouse=True)
def qapp():
    return QApplication([])

@pytest.fixture
def english_exercise_view(qapp):
    """Provides a clean EnglishExerciseView instance for each test."""
    view = EnglishExerciseView()
    view.show()
    yield view
    view.close()

@pytest.fixture
def mock_llm_generate_question():
    """Mocks LLMService.generate_question to return a controlled response."""
    with patch.object(LLMService, 'generate_question') as mock_method:
        mock_method.return_value = [
            {
                "question_text": "What is 2 + 2?",
                "possible_answers": ["3", "4", "5"],
                "correct_answer": "4",
                "explanation": "2 + 2 equals 4. It is a basic arithmetic operation.",
                "subject": "Math",
                "difficulty_band": "Beginner"
            }
        ]
        yield mock_method

def test_initial_ui_state(english_exercise_view):
    """Test initial visibility and text of UI elements."""
    assert english_exercise_view.lesson_title_label.text() == "English Lesson"
    assert english_exercise_view.start_exercise_button.isVisible()
    assert not english_exercise_view.exercise_widget.isVisible()
    assert english_exercise_view.feedback_label.text() == ""
    assert not english_exercise_view.next_question_button.isVisible()

def test_start_exercise_loads_llm_question(english_exercise_view, mock_llm_generate_question):
    """Test that clicking start exercise button triggers LLM question load and display."""
    english_exercise_view.set_lesson_data(MagicMock(title="Test Lesson", content="Lesson Content"))
    QTest.mouseClick(english_exercise_view.start_exercise_button, Qt.MouseButton.LeftButton)
    
    mock_llm_generate_question.assert_called_once_with(
        subject="English", difficulty_band="Beginner", num_questions=1, context_history=None
    )
    assert english_exercise_view.exercise_widget.isVisible()
    assert english_exercise_view.question_text_label.text() == "What is 2 + 2?"
    assert english_exercise_view.user_answer_input.text() == ""
    assert english_exercise_view.submit_answer_button.isVisible()
    assert not english_exercise_view.next_question_button.isVisible()

def test_submit_correct_answer_displays_correct_feedback(english_exercise_view, mock_llm_generate_question):
    """Test feedback display for a correct answer."""
    english_exercise_view.set_lesson_data(MagicMock(title="Test Lesson", content="Lesson Content"))
    QTest.mouseClick(english_exercise_view.start_exercise_button, Qt.MouseButton.LeftButton)
    
    english_exercise_view.user_answer_input.setText("4")
    QTest.mouseClick(english_exercise_view.submit_answer_button, Qt.MouseButton.LeftButton)
    
    assert "Correct!" in english_exercise_view.feedback_label.text()
    assert "Explanation: 2 + 2 equals 4." in english_exercise_view.feedback_label.text()
    assert not english_exercise_view.submit_answer_button.isVisible()
    assert english_exercise_view.next_question_button.isVisible()

def test_submit_incorrect_answer_displays_incorrect_feedback(english_exercise_view, mock_llm_generate_question):
    """Test feedback display for an incorrect answer."""
    english_exercise_view.set_lesson_data(MagicMock(title="Test Lesson", content="Lesson Content"))
    QTest.mouseClick(english_exercise_view.start_exercise_button, Qt.MouseButton.LeftButton)
    
    english_exercise_view.user_answer_input.setText("5")
    QTest.mouseClick(english_exercise_view.submit_answer_button, Qt.MouseButton.LeftButton)
    
    assert "Incorrect." in english_exercise_view.feedback_label.text()
    assert "The correct answer was: 4." in english_exercise_view.feedback_label.text()
    assert "Explanation: 2 + 2 equals 4." in english_exercise_view.feedback_label.text()
    assert not english_exercise_view.submit_answer_button.isVisible()
    assert english_exercise_view.next_question_button.isVisible()

def test_next_question_button_loads_new_question(english_exercise_view, mock_llm_generate_question):
    """Test that clicking next question button loads a new question."""
    english_exercise_view.set_lesson_data(MagicMock(title="Test Lesson", content="Lesson Content"))
    QTest.mouseClick(english_exercise_view.start_exercise_button, Qt.MouseButton.LeftButton)
    
    english_exercise_view.user_answer_input.setText("4")
    QTest.mouseClick(english_exercise_view.submit_answer_button, Qt.MouseButton.LeftButton)
    
    # Mock LLM to return a different question for the next call
    mock_llm_generate_question.return_value = [
        {
            "question_text": "What is 3 + 3?",
            "possible_answers": ["5", "6", "7"],
            "correct_answer": "6",
            "explanation": "3 + 3 equals 6.",
            "subject": "Math",
            "difficulty_band": "Beginner"
        }
    ]
    
    QTest.mouseClick(english_exercise_view.next_question_button, Qt.MouseButton.LeftButton)
    
    # Assert that LLMService.generate_question was called again
    assert mock_llm_generate_question.call_count == 2
    assert english_exercise_view.question_text_label.text() == "What is 3 + 3?"
    assert english_exercise_view.user_answer_input.text() == ""
    assert english_exercise_view.submit_answer_button.isVisible()
    assert not english_exercise_view.next_question_button.isVisible()

def test_llm_error_handling_in_ui(english_exercise_view):
    """Test that UI handles LLM errors gracefully."""
    english_exercise_view.set_lesson_data(MagicMock(title="Test Lesson", content="Lesson Content"))
    
    with patch.object(LLMService, 'generate_question', side_effect=Exception("API call failed")):
        with patch('PyQt6.QtWidgets.QMessageBox.critical') as mock_critical_message_box:
            QTest.mouseClick(english_exercise_view.start_exercise_button, Qt.MouseButton.LeftButton)
            mock_critical_message_box.assert_called_once()
            assert not english_exercise_view.exercise_widget.isVisible()
            assert english_exercise_view.start_exercise_button.isVisible()
