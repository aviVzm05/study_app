import pytest
from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QApplication
from src.main import KidsLearningApp
from models.models import Subject, Topic, Lesson, Question # Import actual models for setup
from services.database import get_db_connection, close_db_connection, DATABASE_FILE
from models.schema import create_schema
from services.data_seeder import seed_initial_data
import os
from pathlib import Path

# Fixture to ensure a clean database for each test
@pytest.fixture(scope="function", autouse=True)
def clean_db():
    if DATABASE_FILE.exists():
        os.remove(DATABASE_FILE)
    create_schema()
    seed_initial_data()
    yield
    if DATABASE_FILE.exists():
        os.remove(DATABASE_FILE)

@pytest.fixture(scope="session")
def app(request):
    """Fixture for QApplication instance."""
    app = QApplication(sys.argv)
    yield app
    app.quit()

def test_full_math_lesson_flow(app, monkeypatch):
    """
    Integration test for a full math lesson flow.
    Mocks user interaction with UI elements.
    """
    main_app = KidsLearningApp()
    main_app.show() # In a real test, this would be a headless display

    # 1. Grade Selection
    main_app.grade_selection_view.grade_combo.setCurrentText("5")
    main_app.grade_selection_view.select_button.click()
    assert main_app.stacked_widget.currentWidget() == main_app.topic_selection_view

    # 2. Topic Selection - Math
    # Assuming "Mathematics" is the first subject and "Math - Grade 5 Decimals" is the first topic
    main_app.topic_selection_view.subject_combo.setCurrentIndex(0) # Select Math
    
    # Manually trigger load_topics as it depends on subject_combo currentData
    main_app.topic_selection_view.load_topics() 
    
    # Assert that "Math - Grade 5 Decimals" is available and select it
    assert main_app.topic_selection_view.topic_combo.count() > 0
    main_app.topic_selection_view.topic_combo.setCurrentIndex(0) # Select the first topic

    main_app.topic_selection_view.start_button.click()
    assert main_app.stacked_widget.currentWidget() == main_app.math_lesson_view

    # 3. Math Lesson View
    assert "Understanding Decimals" in main_app.math_lesson_view.lesson_title_label.text()
    main_app.math_lesson_view.start_quiz_button.click()
    assert main_app.math_lesson_view.question_widget.isVisible()

    # 4. Answer first question correctly
    main_app.math_lesson_view.answer_input.setText("1/2") # Correct answer from data_seeder
    main_app.math_lesson_view.submit_answer_button.click()
    assert "Correct!" in main_app.math_lesson_view.feedback_label.text()
    main_app.math_lesson_view.next_question_button.click()

    # Assuming only one math question seeded for the MVP for simplicity
    assert "You have completed all practice questions!" in main_app.math_lesson_view.feedback_label.text()
    assert not main_app.math_lesson_view.question_widget.isVisible()
    assert main_app.math_lesson_view.start_quiz_button.isVisible()

    main_app.close()

def test_full_english_lesson_flow(app, monkeypatch):
    """
    Integration test for a full English lesson flow.
    Mocks user interaction with UI elements.
    """
    main_app = KidsLearningApp()
    main_app.show()

    # 1. Grade Selection
    main_app.grade_selection_view.grade_combo.setCurrentText("5")
    main_app.grade_selection_view.select_button.click()
    assert main_app.stacked_widget.currentWidget() == main_app.topic_selection_view

    # 2. Topic Selection - English
    main_app.topic_selection_view.subject_combo.setCurrentIndex(1) # Select English
    
    # Manually trigger load_topics
    main_app.topic_selection_view.load_topics() 
    
    assert main_app.topic_selection_view.topic_combo.count() > 0
    main_app.topic_selection_view.topic_combo.setCurrentIndex(0) # Select the first English topic

    main_app.topic_selection_view.start_button.click()
    assert main_app.stacked_widget.currentWidget() == main_app.english_exercise_view

    # 3. English Exercise View
    assert "Exploring Nouns" in main_app.english_exercise_view.lesson_title_label.text()
    main_app.english_exercise_view.start_exercise_button.click()
    assert main_app.english_exercise_view.exercise_widget.isVisible()

    # 4. Answer first question (sentence construction)
    main_app.english_exercise_view.user_input_text.setText("The big dog barks.")
    main_app.english_exercise_view.submit_sentence_button.click()
    assert "Correct!" in main_app.english_exercise_view.feedback_label.text() # Based on current validation service
    main_app.english_exercise_view.next_exercise_button.click()
    
    assert "You have completed all writing exercises!" in main_app.english_exercise_view.feedback_label.text()
    assert not main_app.english_exercise_view.exercise_widget.isVisible()
    assert main_app.english_exercise_view.start_exercise_button.isVisible()
    
    main_app.close()
