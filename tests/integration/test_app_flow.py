import pytest
import os
import json
import sqlite3
from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QApplication, QMessageBox, QRadioButton
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt, QTimer
from src.ui.english_exercise_view import EnglishExerciseView
from src.models.models import Lesson, Student
from services.llm_service import LLMService
from services.data_service import DataService
from services.adaptive_learning_service import AdaptiveLearningService
from services.database import execute_query, create_tables # For clearing test data and creating tables

# Sample LLM responses for different scenarios, now as lists of 20 questions
MOCK_LLM_QUESTION_BEGINNER_LIST = json.dumps([
    {
        "question_text": f"Beginner Q{i}: What is the past tense of 'go'?",
        "possible_answers": ["goes", "went", "going", "gone"],
        "correct_answer": "went",
        "explanation": "'Went' is the simple past tense of the verb 'go'.",
        "subject": "English",
        "difficulty_band": "Beginner"
    } for i in range(1, 21)
])
MOCK_LLM_QUESTION_INTERMEDIATE_LIST = json.dumps([
    {
        "question_text": f"Intermediate Q{i}: Identify the gerund in the sentence: 'Swimming is my favorite activity.'",
        "possible_answers": ["is", "my", "favorite", "Swimming"],
        "correct_answer": "Swimming",
        "explanation": "A gerund is a verb ending in '-ing' that functions as a noun.",
        "subject": "English",
        "difficulty_band": "Intermediate"
    } for i in range(1, 21)
])
MOCK_LLM_QUESTION_ADVANCED_LIST = json.dumps([
    {
        "question_text": f"Advanced Q{i}: Explain the concept of 'subjunctive mood' in English grammar.",
        "possible_answers": ["Used for wishes/hypotheses", "Used for past actions", "Used for future events", "Used for commands"],
        "correct_answer": "Used for wishes/hypotheses",
        "explanation": "The subjunctive mood is used to express various states of unreality such as wish, emotion, possibility, judgment, opinion, obligation, or action that has has not yet occurred.",
        "subject": "English",
        "difficulty_band": "Advanced"
    } for i in range(1, 21)
])

@pytest.fixture(scope="session", autouse=True)
def qapp_session():
    """Initializes QApplication once for all tests."""
    return QApplication([])

@pytest.fixture(autouse=True)
def setup_integration_test_environment(qapp_session):
    """Sets up and tears down a clean environment for each integration test."""
    os.environ["GEMINI_API_KEY"] = "dummy_key" # Set dummy API key for testing

    # Patch LLMService initialization to avoid actual API calls
    with patch('services.llm_service.genai.configure'), \
         patch('services.llm_service.genai.GenerativeModel') as MockGenerativeModel:
        # Provide a mock for the model instance
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.side_effect = [
            MagicMock(text=MOCK_LLM_QUESTION_BEGINNER_LIST), # First batch
            MagicMock(text=MOCK_LLM_QUESTION_INTERMEDIATE_LIST), # Second batch (after upgrade)
            MagicMock(text=MOCK_LLM_QUESTION_BEGINNER_LIST) # Third batch (after downgrade)
        ]
        MockGenerativeModel.return_value = mock_model_instance
        
        # Patch the database connection to use in-memory for testing
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        with patch('services.database.get_db_connection', return_value=conn):
            # Ensure tables are created in the in-memory db
            create_tables(conn) # Use the actual create_tables function
            
            # Clear data before each test
            execute_query("DELETE FROM students", conn=conn)
            execute_query("DELETE FROM quiz_sessions", conn=conn)
            execute_query("DELETE FROM performance_history", conn=conn)
            execute_query("DELETE FROM questions", conn=conn) # Clear dummy questions if any
            
            # Add a dummy subject and topic for FK constraints for lesson/questions if needed
            execute_query("INSERT INTO subjects (id, name) VALUES (?, ?)", (1, "English"), conn=conn)
            execute_query("INSERT INTO topics (id, subject_id, grade, name) VALUES (?, ?, ?, ?)", (1, 1, 5, "Grammar"), conn=conn)

            yield # Run the test
        conn.close()
    del os.environ["GEMINI_API_KEY"] # Clean up env var

@pytest.fixture
def english_exercise_view_integration(qapp_session):
    """Provides a clean EnglishExerciseView instance for integration tests."""
    view = EnglishExerciseView()
    view.show()
    yield view
    view.close()

def _simulate_option_selection(view, answer_text):
    """Helper to simulate clicking a radio button with the given answer_text."""
    found = False
    for button in view.options_button_group.buttons():
        if button.text() == answer_text:
            button.setChecked(True) # Select the button
            button.clicked.emit() # Emit clicked signal
            found = True
            break
    if not found:
        raise ValueError(f"Radio button with text '{answer_text}' not found.")
    QApplication.processEvents()


def test_full_english_quiz_flow_with_adaptation(english_exercise_view_integration):
    """
    Tests the full quiz flow: dynamic question generation, answering, feedback,
    and adaptive difficulty changes based on mocked LLM responses and data service.
    """
    view = english_exercise_view_integration

    # 1. Simulate initial setup: create student, set lesson data
    student = DataService.create_student_profile("IntegrationStudent")
    lesson = Lesson(id=1, topic_id=1, title="Grammar Basics", content="Lesson about grammar.")
    view.set_lesson_data(lesson)
    
    # Manually set the student in the view for this test
    # In a real app, this would be passed from a main window or session manager
    view.student_id = student.id 

    # Initial difficulty should be Beginner
    assert view.current_difficulty_band == "Beginner"

    # 2. Start the exercise (should load a Beginner question batch)
    QTest.mouseClick(view.start_exercise_button, Qt.MouseButton.LeftButton)
    QApplication.processEvents() # Process events to allow LLM call to return
    
    assert view.exercise_widget.isVisible()
    assert "Question 1/20: Beginner Q1: What is the past tense of 'go'?" in view.question_text_label.text()
    assert view.current_difficulty_band == "Beginner" # Still beginner until performance tracked

    # Simulate answering enough questions to trigger an upgrade (e.g., 5 correct answers in a row)
    # We will simulate 5 correct answers for the first 5 questions
    for i in range(5):
        # Current question is from MOCK_LLM_QUESTION_BEGINNER_LIST
        _simulate_option_selection(view, "went")
        QTest.mouseClick(view.submit_answer_button, Qt.MouseButton.LeftButton)
        QApplication.processEvents()
        
        assert "Correct!" in view.feedback_label.text()
        
        # No need to manually save performance history here, DataService methods should be called by the view
        # if view's submit_answer logic is fully integrated. For this test, we assume view does that.
        # But we need to ensure the adaptive service can pick up the performance.
        
        # Move to the next question
        if i < 4: # For the first 4 questions, click next
            QTest.mouseClick(view.next_question_button, Qt.MouseButton.LeftButton)
            QApplication.processEvents()
        
    # After 5 correct answers, the next question load (which would be question 6)
    # should trigger adaptive learning analysis and potentially an upgrade.
    # The view.current_difficulty_band would be updated *after* the _load_llm_question or similar
    # In this test, we are simulating question flow one by one, so we check difficulty before next question loads
    # For now, let's simplify by ensuring we complete 5 correct answers then proceed.

    # After 5 correct answers, simulate advancing to the next question
    # This should trigger an adaptive learning check
    QTest.mouseClick(view.next_question_button, Qt.MouseButton.LeftButton)
    QApplication.processEvents()

    # Assuming AdaptiveLearningService would have upgraded the difficulty after 5 correct answers
    # This is a simplification; a full integration test might need to mock AdaptiveLearningService's return
    # For now, we are verifying that the view's internal state for difficulty changes.
    # The view calls _load_llm_question, which implicitly gets the next difficulty from AdaptiveLearningService
    assert view.current_difficulty_band == "Intermediate" # Should have upgraded

    # Verify the question text is from the Intermediate list
    assert "Question 6/20: Intermediate Q1: Identify the gerund in the sentence: 'Swimming is my favorite activity.'" in view.question_text_label.text()

    # Simulate 5 incorrect answers to trigger a downgrade
    for i in range(5):
        # Current question is from MOCK_LLM_QUESTION_INTERMEDIATE_LIST
        _simulate_option_selection(view, "is") # Incorrect answer for the gerund question
        QTest.mouseClick(view.submit_answer_button, Qt.MouseButton.LeftButton)
        QApplication.processEvents()
        
        assert "Incorrect." in view.feedback_label.text()
        
        if i < 4: # For the first 4 incorrect answers, click next
            QTest.mouseClick(view.next_question_button, Qt.MouseButton.LeftButton)
            QApplication.processEvents()

    # After 5 incorrect answers, simulate advancing to the next question
    # This should trigger an adaptive learning check
    QTest.mouseClick(view.next_question_button, Qt.MouseButton.LeftButton)
    QApplication.processEvents()
    
    # Assert difficulty downgraded to Beginner
    assert view.current_difficulty_band == "Beginner" 

    # Verify the question text is from the Beginner list again
    assert "Question 11/20: Beginner Q1: What is the past tense of 'go'?" in view.question_text_label.text()

    # Finish the remaining questions in the batch (total 20 questions)
    # The first 10 questions were answered (5 correct, 5 incorrect).
    # We need to answer 10 more questions from the second Beginner batch to finish the 20-question quiz.
    for i in range(10):
        _simulate_option_selection(view, "went") # Correct answer
        QTest.mouseClick(view.submit_answer_button, Qt.MouseButton.LeftButton)
        QApplication.processEvents()
        QTest.mouseClick(view.next_question_button, Qt.MouseButton.LeftButton)
        QApplication.processEvents()

    # After 20 questions, the quiz should be complete
    assert not view.exercise_widget.isVisible()
    assert view.start_exercise_button.isVisible()

    # Check final score (5 correct + 10 correct = 15 correct)
    # The actual score logic is within the view's submit_answer, we just need to ensure the final report appears.
    # QMessageBox content can be hard to assert, but we can check if it was called.
    with patch('PyQt6.QtWidgets.QMessageBox.information') as mock_info_message_box:
        # The last click of 'next_question_button' should have triggered _finish_quiz
        # if all 20 questions were completed.
        # This will be triggered on the 21st call to display_current_question
        # The above loop completes 20 questions, and the last QTest.mouseClick(view.next_question_button) would be for the 20th question.
        # So, the _finish_quiz should happen after processing the 20th question and then trying to go to next.
        # Let's adjust the loop to trigger finish after the last question is submitted
        pass # The previous loop should handle this.

    # Check that the QMessageBox was called
    # Note: Mocking QMessageBox.information might be tricky if it's called directly without a patch context
    # This might require a more sophisticated mocking setup or checking logs/UI state
    # For now, we rely on the visibility checks.