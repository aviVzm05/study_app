import pytest
import os
import json
import sqlite3
from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt, QTimer
from src.ui.english_exercise_view import EnglishExerciseView
from src.models.models import Lesson, Student
from services.llm_service import LLMService
from services.data_service import DataService
from services.adaptive_learning_service import AdaptiveLearningService
from services.database import execute_query # For clearing test data

# Sample LLM responses for different scenarios
MOCK_LLM_QUESTION_BEGINNER = json.dumps([
    {
        "question_text": "What is the past tense of 'go'?",
        "possible_answers": ["goes", "went", "going"],
        "correct_answer": "went",
        "explanation": "'Went' is the simple past tense of the verb 'go'.",
        "subject": "English",
        "difficulty_band": "Beginner"
    }
])
MOCK_LLM_QUESTION_INTERMEDIATE = json.dumps([
    {
        "question_text": "Identify the gerund in the sentence: 'Swimming is my favorite activity.'",
        "possible_answers": ["is", "my", "favorite", "Swimming"],
        "correct_answer": "Swimming",
        "explanation": "A gerund is a verb ending in '-ing' that functions as a noun.",
        "subject": "English",
        "difficulty_band": "Intermediate"
    }
])
MOCK_LLM_QUESTION_ADVANCED = json.dumps([
    {
        "question_text": "Explain the concept of 'subjunctive mood' in English grammar.",
        "possible_answers": [],
        "correct_answer": "The subjunctive mood is used to express wishes, proposals, demands, or statements contrary to fact.",
        "explanation": "The subjunctive mood is a grammatical mood of verbs found in many languages. Subjunctive forms of verbs are typically used to express various states of unreality such as wish, emotion, possibility, judgment, opinion, obligation, or action that has not yet occurred. In English, it's often seen in 'if I were' or 'I wish it were' constructions.",
        "subject": "English",
        "difficulty_band": "Advanced"
    }
])

@pytest.fixture(scope="session", autouse=True)
def qapp_session():
    """Initializes QApplication once for all tests."""
    return QApplication([])

@pytest.fixture(autouse=True)
def setup_integration_test_environment(qapp_session):
    """Sets up and tears down a clean environment for each integration test."""
    # Patch LLMService initialization to avoid actual API calls
    with patch('services.llm_service.genai.configure'), \
         patch('services.llm_service.genai.GenerativeModel') as MockGenerativeModel:
        # Provide a mock for the model instance
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.side_effect = [
            MagicMock(text=MOCK_LLM_QUESTION_BEGINNER), # First question
            MagicMock(text=MOCK_LLM_QUESTION_INTERMEDIATE), # Second question
            MagicMock(text=MOCK_LLM_QUESTION_BEGINNER) # Third question (after downgrade)
        ]
        MockGenerativeModel.return_value = mock_model_instance
        
        # Patch the database connection to use in-memory for testing
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        with patch('services.database.get_db_connection', return_value=conn):
            # Ensure tables are created in the in-memory db
            from services.database import create_tables
            create_tables(conn)
            
            # Clear data before each test
            execute_query("DELETE FROM students", conn=conn)
            execute_query("DELETE FROM quiz_sessions", conn=conn)
            execute_query("DELETE FROM performance_history", conn=conn)
            execute_query("DELETE FROM questions", conn=conn) # Clear dummy questions if any
            execute_query("INSERT INTO questions (id, prompt, question_type, options, correct_answer, explanation, difficulty_band) VALUES (?, ?, ?, ?, ?, ?, ?)", (1, "Dummy Q for FK", "text", "[]", "Ans", "Exp", "Beginner"), conn=conn) # Add a dummy for FK
            
            yield # Run the test
        conn.close()

@pytest.fixture
def english_exercise_view_integration(qapp_session):
    """Provides a clean EnglishExerciseView instance for integration tests."""
    view = EnglishExerciseView()
    view.show()
    yield view
    view.close()

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

    # 2. Start the exercise (should load a Beginner question)
    QTest.mouseClick(view.start_exercise_button, Qt.MouseButton.LeftButton)
    QApplication.processEvents() # Process events to allow LLM call to return
    
    assert view.exercise_widget.isVisible()
    assert view.question_text_label.text() == "What is the past tense of 'go'?"
    assert view.current_difficulty_band == "Beginner" # Still beginner until performance tracked

    # Simulate 3 correct answers to trigger an upgrade
    for i in range(3):
        # Current question is from MOCK_LLM_QUESTION_BEGINNER
        view.user_answer_input.setText("went")
        QTest.mouseClick(view.submit_answer_button, Qt.MouseButton.LeftButton)
        QApplication.processEvents()
        
        assert "Correct!" in view.feedback_label.text()
        
        # Save performance history (mock DataService will handle this)
        # Note: In a real app, this would be handled within submit_answer
        DataService.save_question_attempt(
            DataService.start_quiz_session(view.student_id, "English", view.current_difficulty_band).id,
            100 + i, # Dummy question_id
            "went", True, 5.0
        )
        # Trigger adaptive logic to check for upgrade
        # In actual application, the AdaptiveLearningService would be called after each submission
        # For integration test, we'll simulate the next question load to trigger adaptation
        
        if i < 2: # Don't click next after last correct answer, to test current difficulty before next load
            QTest.mouseClick(view.next_question_button, Qt.MouseButton.LeftButton)
            QApplication.processEvents()
            
            # Check difficulty update (should only update on load of next question)
            # We explicitly call it here for test verification as the view's current_difficulty_band is updated
            # by a function called within _load_llm_question
            next_diff, _ = AdaptiveLearningService.analyze_performance_and_suggest_next(student.id, "English")
            if i == 2: # After 3 correct answers
                assert next_diff == "Intermediate"
            else:
                assert next_diff == "Beginner" # Still beginner for first two correct answers
    
    # After 3 correct answers, load next question. Difficulty should upgrade to Intermediate.
    QTest.mouseClick(view.next_question_button, Qt.MouseButton.LeftButton)
    QApplication.processEvents()
    
    # LLMService is mocked to return INTERMEDIATE question next
    assert view.question_text_label.text() == "Identify the gerund in the sentence: 'Swimming is my favorite activity.'"
    # The view's difficulty band should be updated by the logic called within _load_llm_question
    assert view.current_difficulty_band == "Intermediate" 

    # Simulate 2 incorrect answers to trigger a downgrade
    for i in range(2):
        # Current question is from MOCK_LLM_QUESTION_INTERMEDIATE
        view.user_answer_input.setText("wrong answer")
        QTest.mouseClick(view.submit_answer_button, Qt.MouseButton.LeftButton)
        QApplication.processEvents()
        
        assert "Incorrect." in view.feedback_label.text()
        
        DataService.save_question_attempt(
            DataService.start_quiz_session(view.student_id, "English", view.current_difficulty_band).id,
            200 + i, # Dummy question_id
            "wrong answer", False, 10.0
        )
        
        if i < 1: # Only click next after first incorrect answer
            QTest.mouseClick(view.next_question_button, Qt.MouseButton.LeftButton)
            QApplication.processEvents()

    # After 2 incorrect answers, load next question. Difficulty should downgrade to Beginner.
    QTest.mouseClick(view.next_question_button, Qt.MouseButton.LeftButton)
    QApplication.processEvents()
    
    # LLMService is mocked to return BEGINNER question next (after downgrade)
    assert view.question_text_label.text() == "What is the past tense of 'go'?"
    # The view's difficulty band should be updated by the logic called within _load_llm_question
    assert view.current_difficulty_band == "Beginner"