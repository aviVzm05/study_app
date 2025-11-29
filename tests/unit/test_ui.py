import pytest
from PyQt6.QtWidgets import QApplication, QRadioButton
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
from unittest.mock import MagicMock, patch
from src.ui.english_exercise_view import EnglishExerciseView
from src.services.llm_service import LLMService

# Sample valid response from LLM, now with 20 questions
MOCK_LLM_RESPONSE_DATA = [
    {
        "question_text": f"What is {i} + {i}?",
        "possible_answers": [f"{i+i-1}", f"{i+i}", f"{i+i+1}"],
        "correct_answer": f"{i+i}",
        "explanation": f"{i} + {i} equals {i+i}.",
        "subject": "Math",
        "difficulty_band": "Beginner"
    } for i in range(1, 21) # Generate 20 questions
]


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
        mock_method.return_value = MOCK_LLM_RESPONSE_DATA
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
    QApplication.processEvents() # Allow UI to update and LLM call to process

    mock_llm_generate_question.assert_called_once_with(
        subject="English", difficulty_band="Beginner", num_questions=20, context_history=None
    )
    assert english_exercise_view.exercise_widget.isVisible()
    assert "Question 1/20: What is 1 + 1?" in english_exercise_view.question_text_label.text()
    assert english_exercise_view.options_layout.count() > 0 # Check that options are displayed
    assert english_exercise_view.submit_answer_button.isVisible()
    assert not english_exercise_view.next_question_button.isVisible()

def test_submit_correct_answer_displays_correct_feedback(english_exercise_view, mock_llm_generate_question):
    """Test feedback display for a correct answer."""
    english_exercise_view.set_lesson_data(MagicMock(title="Test Lesson", content="Lesson Content"))
    QTest.mouseClick(english_exercise_view.start_exercise_button, Qt.MouseButton.LeftButton)
    QApplication.processEvents() # Allow UI to update and LLM call to process

    # Simulate selecting the correct answer (e.g., "2" for "1+1")
    correct_answer_text = MOCK_LLM_RESPONSE_DATA[0]["correct_answer"]
    for button in english_exercise_view.options_button_group.buttons():
        if button.text() == correct_answer_text:
            QTest.mouseClick(button, Qt.MouseButton.LeftButton)
            break
    QApplication.processEvents()
    
    QTest.mouseClick(english_exercise_view.submit_answer_button, Qt.MouseButton.LeftButton)
    QApplication.processEvents()
    
    assert "Correct!" in english_exercise_view.feedback_label.text()
    assert "Explanation: 1 + 1 equals 2." in english_exercise_view.feedback_label.text()
    assert not english_exercise_view.submit_answer_button.isEnabled() # Button should be disabled
    assert english_exercise_view.next_question_button.isVisible()
    assert english_exercise_view.score == 1
    assert english_exercise_view.total_questions == 1


def test_submit_incorrect_answer_displays_incorrect_feedback(english_exercise_view, mock_llm_generate_question):
    """Test feedback display for an incorrect answer."""
    english_exercise_view.set_lesson_data(MagicMock(title="Test Lesson", content="Lesson Content"))
    QTest.mouseClick(english_exercise_view.start_exercise_button, Qt.MouseButton.LeftButton)
    QApplication.processEvents() # Allow UI to update and LLM call to process
    
    # Simulate selecting an incorrect answer (e.g., "3" for "1+1")
    incorrect_answer_text = "3" # assuming "3" is an incorrect option
    for button in english_exercise_view.options_button_group.buttons():
        if button.text() == incorrect_answer_text:
            QTest.mouseClick(button, Qt.MouseButton.LeftButton)
            break
    QApplication.processEvents()

    QTest.mouseClick(english_exercise_view.submit_answer_button, Qt.MouseButton.LeftButton)
    QApplication.processEvents()
    
    assert "Incorrect." in english_exercise_view.feedback_label.text()
    assert "The correct answer was: 2." in english_exercise_view.feedback_label.text()
    assert "Explanation: 1 + 1 equals 2." in english_exercise_view.feedback_label.text()
    assert not english_exercise_view.submit_answer_button.isEnabled()
    assert english_exercise_view.next_question_button.isVisible()
    assert english_exercise_view.score == 0
    assert english_exercise_view.total_questions == 1

def test_next_question_button_loads_next_question_from_batch(english_exercise_view, mock_llm_generate_question):
    """Test that clicking next question button loads the next question from the batch."""
    english_exercise_view.set_lesson_data(MagicMock(title="Test Lesson", content="Lesson Content"))
    QTest.mouseClick(english_exercise_view.start_exercise_button, Qt.MouseButton.LeftButton)
    QApplication.processEvents() # Initial question load

    # Answer first question correctly
    correct_answer_text = MOCK_LLM_RESPONSE_DATA[0]["correct_answer"]
    for button in english_exercise_view.options_button_group.buttons():
        if button.text() == correct_answer_text:
            QTest.mouseClick(button, Qt.MouseButton.LeftButton)
            break
    QApplication.processEvents()
    QTest.mouseClick(english_exercise_view.submit_answer_button, Qt.MouseButton.LeftButton)
    QApplication.processEvents()
    
    # Click next question button
    QTest.mouseClick(english_exercise_view.next_question_button, Qt.MouseButton.LeftButton)
    QApplication.processEvents()
    
    # Assert that LLMService.generate_question was NOT called again (questions are from batch)
    mock_llm_generate_question.assert_called_once() # Still only called once for the initial batch of 20
    assert "Question 2/20: What is 2 + 2?" in english_exercise_view.question_text_label.text()
    assert english_exercise_view.options_layout.count() > 0
    assert english_exercise_view.submit_answer_button.isEnabled()
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
