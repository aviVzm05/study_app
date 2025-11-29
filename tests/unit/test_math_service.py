import pytest
from unittest.mock import patch, MagicMock
from services.math_service import MathService
from models.models import Lesson, Question, Topic

@pytest.fixture
def mock_models():
    """Fixture to mock model find_all methods."""
    with patch('models.models.Lesson.find_all') as mock_lesson_find_all, \
         patch('models.models.Question.find_all') as mock_question_find_all, \
         patch('models.models.Topic.find_all') as mock_topic_find_all:
        yield mock_lesson_find_all, mock_question_find_all, mock_topic_find_all

def test_get_lesson_and_questions_for_topic(mock_models):
    mock_lesson_find_all, mock_question_find_all, _ = mock_models
    math_service = MathService()

    # Mock data
    mock_lesson = MagicMock(spec=Lesson, topic_id=1, title="Test Lesson", content="Lesson Content")
    mock_lesson_find_all.return_value = [mock_lesson, MagicMock(topic_id=2)]

    mock_question1 = MagicMock(spec=Question, topic_id=1, question_type="multiple_choice", correct_answer="A")
    mock_question2 = MagicMock(spec=Question, topic_id=1, question_type="multiple_choice", correct_answer="B")
    mock_question3 = MagicMock(spec=Question, topic_id=1, question_type="fill_in_the_blank", correct_answer="C")
    mock_question_find_all.return_value = [mock_question1, mock_question2, mock_question3, MagicMock(topic_id=2)]

    # Test with existing topic
    lesson, questions = math_service.get_lesson_and_questions_for_topic(1)
    assert lesson.title == "Test Lesson"
    assert len(questions) == 2  # Only multiple_choice questions should be returned
    assert questions[0].correct_answer == "A"
    assert questions[1].correct_answer == "B"

    # Test with non-existing topic
    lesson, questions = math_service.get_lesson_and_questions_for_topic(99)
    assert lesson is None
    assert len(questions) == 0

def test_get_topics_for_grade_subject(mock_models):
    _, _, mock_topic_find_all = mock_models
    math_service = MathService()

    # Mock data
    mock_topic1 = MagicMock(spec=Topic)
    mock_topic1.grade = 5
    mock_topic1.subject_id = 1
    mock_topic1.name = "Math - Grade 5 Algebra"

    mock_topic2 = MagicMock(spec=Topic)
    mock_topic2.grade = 5
    mock_topic2.subject_id = 1
    mock_topic2.name = "Math - Grade 5 Geometry"

    mock_topic3 = MagicMock(spec=Topic)
    mock_topic3.grade = 6
    mock_topic3.subject_id = 1
    mock_topic3.name = "Math - Grade 6 Decimals"
    
    mock_topic4 = MagicMock(grade=5, subject_id=2, name="English - Grade 5 Nouns") # Non-Math topic
    mock_topic_find_all.return_value = [mock_topic1, mock_topic2, mock_topic3, mock_topic4]

    # Test with existing grade and subject
    topics = math_service.get_topics_for_grade_subject(5, 1)
    assert len(topics) == 2
    assert topics[0].name == "Math - Grade 5 Algebra"
    assert topics[1].name == "Math - Grade 5 Geometry"

    # Test with non-existing grade
    topics = math_service.get_topics_for_grade_subject(7, 1)
    assert len(topics) == 0

    # Test with non-existing subject
    topics = math_service.get_topics_for_grade_subject(5, 99)
    assert len(topics) == 0
