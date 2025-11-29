import pytest
from unittest.mock import patch, MagicMock
from src.services.adaptive_learning_service import AdaptiveLearningService
from src.services.data_service import DataService
from src.models.models import Student, PerformanceHistory

@pytest.fixture
def mock_student():
    """Returns a mock Student object."""
    student = Student(id=1, nickname="TestStudent", current_difficulty_english="Beginner", current_difficulty_math="Beginner")
    return student

@pytest.fixture
def mock_data_service(mock_student):
    """Mocks DataService methods."""
    with patch.object(DataService, 'get_student_profile', return_value=mock_student), \
         patch.object(DataService, 'update_student_profile', side_effect=lambda sid, d_eng=None, d_math=None: mock_student.current_difficulty_english if d_eng else d_eng == d_eng), \
         patch.object(Student, 'save', return_value=None): # Mock save method on the student object
        yield

def create_mock_history(is_correct_list):
    """Helper to create a list of mock PerformanceHistory objects."""
    history = []
    for i, is_correct in enumerate(is_correct_list):
        mock_attempt = MagicMock(spec=PerformanceHistory)
        mock_attempt.is_correct = is_correct
        mock_attempt.question_id = i + 1
        mock_attempt.student_answer = "mock_answer"
        history.append(mock_attempt)
    return history

def test_analyze_no_history_maintains_difficulty(mock_data_service, mock_student):
    """Test when there's no history, difficulty remains current."""
    with patch.object(DataService, 'get_performance_history', return_value=[]):
        difficulty, context = AdaptiveLearningService.analyze_performance_and_suggest_next(1, "English")
        assert difficulty == "Beginner"
        assert "No recent performance data" in context

def test_analyze_correct_streak_upgrades_difficulty(mock_data_service, mock_student):
    """Test that a correct streak upgrades difficulty."""
    mock_student.current_difficulty_english = "Beginner"
    history = create_mock_history([True] * AdaptiveLearningService.CORRECT_STREAK_FOR_UPGRADE)
    with patch.object(DataService, 'get_performance_history', return_value=history):
        difficulty, context = AdaptiveLearningService.analyze_performance_and_suggest_next(1, "English")
        assert difficulty == "Intermediate"
        assert "shows strong understanding" in context

def test_analyze_incorrect_streak_downgrades_difficulty(mock_data_service, mock_student):
    """Test that an incorrect streak downgrades difficulty."""
    mock_student.current_difficulty_english = "Intermediate"
    history = create_mock_history([False] * AdaptiveLearningService.INCORRECT_STREAK_FOR_DOWNGRADE)
    with patch.object(DataService, 'get_performance_history', return_value=history):
        difficulty, context = AdaptiveLearningService.analyze_performance_and_suggest_next(1, "English")
        assert difficulty == "Beginner"
        assert "struggling" in context

def test_analyze_mixed_performance_maintains_difficulty(mock_data_service, mock_student):
    """Test mixed performance maintains current difficulty."""
    mock_student.current_difficulty_english = "Intermediate"
    history = create_mock_history([True, False, True, False]) # Mixed performance
    with patch.object(DataService, 'get_performance_history', return_value=history):
        difficulty, context = AdaptiveLearningService.analyze_performance_and_suggest_next(1, "English")
        assert difficulty == "Intermediate"
        assert "maintaining current performance" in context

def test_analyze_cannot_upgrade_from_advanced(mock_data_service, mock_student):
    """Test cannot upgrade past Advanced difficulty."""
    mock_student.current_difficulty_english = "Advanced"
    history = create_mock_history([True] * AdaptiveLearningService.CORRECT_STREAK_FOR_UPGRADE)
    with patch.object(DataService, 'get_performance_history', return_value=history):
        difficulty, context = AdaptiveLearningService.analyze_performance_and_suggest_next(1, "English")
        assert difficulty == "Advanced" # Should remain Advanced

def test_analyze_cannot_downgrade_from_beginner(mock_data_service, mock_student):
    """Test cannot downgrade below Beginner difficulty."""
    mock_student.current_difficulty_english = "Beginner"
    history = create_mock_history([False] * AdaptiveLearningService.INCORRECT_STREAK_FOR_DOWNGRADE)
    with patch.object(DataService, 'get_performance_history', return_value=history):
        difficulty, context = AdaptiveLearningService.analyze_performance_and_suggest_next(1, "English")
        assert difficulty == "Beginner" # Should remain Beginner

def test_analyze_non_existent_student():
    """Test handling of non-existent student."""
    with patch.object(DataService, 'get_student_profile', return_value=None):
        difficulty, context = AdaptiveLearningService.analyze_performance_and_suggest_next(999, "Math")
        assert difficulty == "Beginner"
        assert "Student profile not found" in context