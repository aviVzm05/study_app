import pytest
from unittest.mock import patch, MagicMock
from src.services.english_service import EnglishService
from src.models.models import Lesson, Question, Topic

@pytest.fixture
def mock_models():
    """Fixture to mock model find_all methods."""
    with patch('models.models.Lesson.find_all') as mock_lesson_find_all, \
         patch('models.models.Question.find_all') as mock_question_find_all, \
         patch('models.models.Topic.find_all') as mock_topic_find_all:
        yield mock_lesson_find_all, mock_question_find_all, mock_topic_find_all

def test_get_lesson_and_questions_for_topic_english(mock_models):
    mock_lesson_find_all, mock_question_find_all, _ = mock_models
    english_service = EnglishService()

    # Mock data
    mock_lesson = MagicMock(spec=Lesson, topic_id=101, title="English Lesson", content="Lesson Content")
    mock_lesson_find_all.return_value = [mock_lesson, MagicMock(topic_id=102)]

    mock_question1 = MagicMock(spec=Question, topic_id=101, question_type="sentence_construction", correct_answer="A")
    mock_question2 = MagicMock(spec=Question, topic_id=101, question_type="sentence_construction", correct_answer="B")
    mock_question3 = MagicMock(spec=Question, topic_id=101, question_type="multiple_choice", correct_answer="C") # Should be filtered out
    mock_question_find_all.return_value = [mock_question1, mock_question2, mock_question3, MagicMock(topic_id=102)]

    # Test with existing topic
    lesson, questions = english_service.get_lesson_and_questions_for_topic(101)
    assert lesson.title == "English Lesson"
    assert len(questions) == 2  # Only sentence_construction questions should be returned
    assert questions[0].correct_answer == "A"
    assert questions[1].correct_answer == "B"

    # Test with non-existing topic
    lesson, questions = english_service.get_lesson_and_questions_for_topic(999)
    assert lesson is None
    assert len(questions) == 0

def test_get_topics_for_grade_subject_english(mock_models):
    _, _, mock_topic_find_all = mock_models
    english_service = EnglishService()

    # Mock data
    mock_topic1 = MagicMock(spec=Topic)
    mock_topic1.grade = 5
    mock_topic1.subject_id = 2
    mock_topic1.name = "English - Grade 5 Nouns"

    mock_topic2 = MagicMock(spec=Topic)
    mock_topic2.grade = 5
    mock_topic2.subject_id = 2
    mock_topic2.name = "English - Grade 5 Verbs"

    mock_topic3 = MagicMock(spec=Topic)
    mock_topic3.grade = 6
    mock_topic3.subject_id = 2
    mock_topic3.name = "English - Grade 6 Adjectives"

    mock_topic4 = MagicMock(grade=5, subject_id=1, name="Math - Grade 5 Decimals") # Non-English topic
    mock_topic_find_all.return_value = [mock_topic1, mock_topic2, mock_topic3, mock_topic4]

    # Test with existing grade and subject
    topics = english_service.get_topics_for_grade_subject(5, 2)
    assert len(topics) == 2
    assert topics[0].name == "English - Grade 5 Nouns"
    assert topics[1].name == "English - Grade 5 Verbs"

    # Test with non-existing grade
    topics = english_service.get_topics_for_grade_subject(7, 2)
    assert len(topics) == 0

    # Test with non-existing subject
    topics = english_service.get_topics_for_grade_subject(5, 99)
    assert len(topics) == 0
