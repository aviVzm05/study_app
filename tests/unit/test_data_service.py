import pytest
import sqlite3
from unittest.mock import patch, MagicMock
from src.services.data_service import DataService
from src.models.models import Student, QuizSession, PerformanceHistory
from src.services.database import get_db_connection, close_db_connection, execute_query, create_tables # Import create_tables
from pathlib import Path

@pytest.fixture(autouse=True)
def in_memory_db():
    """Sets up an in-memory SQLite database for testing."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    # Patch get_db_connection to return this in-memory connection
    with patch('services.database.get_db_connection', return_value=conn), \
         patch('services.database.close_db_connection', new=MagicMock()): # Patch close to do nothing
        # Patch DATABASE_FILE and DATABASE_DIR to prevent interaction with real files
        with patch('services.database.DATABASE_FILE', new=Path(":memory:")):
            with patch('services.database.DATABASE_DIR', new=Path("/mock/path")):
                # Create tables using the patched connection
                create_tables(conn) # Use the actual create_tables function
                yield
    conn.close()

def test_create_and_get_student_profile():
    """Test creating and retrieving a student profile."""
    student = DataService.create_student_profile("TestStudent")
    assert student.id is not None
    assert student.nickname == "TestStudent"
    assert student.current_difficulty_english == "Beginner"

    retrieved_student = DataService.get_student_profile(student.id)
    assert retrieved_student is not None
    assert retrieved_student.nickname == "TestStudent"

def test_update_student_profile():
    """Test updating a student's difficulty levels."""
    student = DataService.create_student_profile("UpdateMe")
    updated_student = DataService.update_student_profile(student.id, difficulty_english="Intermediate", difficulty_math="Advanced")
    assert updated_student.current_difficulty_english == "Intermediate"
    assert updated_student.current_difficulty_math == "Advanced"

    retrieved_student = DataService.get_student_profile(student.id)
    assert retrieved_student.current_difficulty_english == "Intermediate"
    assert retrieved_student.current_difficulty_math == "Advanced"

def test_start_and_end_quiz_session():
    """Test starting and ending a quiz session."""
    student = DataService.create_student_profile("QuizStudent")
    session = DataService.start_quiz_session(student.id, "Math", "Beginner")
    assert session.id is not None
    assert session.student_id == student.id
    assert session.subject == "Math"
    assert session.end_time is None
    assert session.overall_score is None

    ended_session = DataService.end_quiz_session(session.id, 90.5)
    assert ended_session.overall_score == 90.5
    assert ended_session.end_time is not None

def test_save_and_get_performance_history():
    """Test saving and retrieving performance history."""
    student = DataService.create_student_profile("HistoryStudent")
    session = DataService.start_quiz_session(student.id, "English", "Intermediate")
    
    # Need to add a dummy question to satisfy FK
    # Ensure all NOT NULL columns are provided, including 'subject' and 'prompt'
    execute_query("INSERT INTO questions (id, prompt, subject, correct_answer) VALUES (?, ?, ?, ?)", (1, "Dummy Question", "English", "Dummy Answer"))

    attempt = DataService.save_question_attempt(session.id, 1, "user_ans", True, 20.0)
    assert attempt.id is not None
    assert attempt.quiz_session_id == session.id
    assert attempt.is_correct is True

    history = DataService.get_performance_history(student.id, "English")
    assert len(history) == 1
    assert history[0].student_answer == "user_ans"

def test_delete_performance_history():
    """Test deleting performance history and quiz sessions for a student."""
    student = DataService.create_student_profile("DeleteStudent")
    session = DataService.start_quiz_session(student.id, "Math", "Advanced")
    
    # Need to add a dummy question to satisfy FK
    # Ensure all NOT NULL columns are provided, including 'subject' and 'prompt'
    execute_query("INSERT INTO questions (id, prompt, subject, correct_answer) VALUES (?, ?, ?, ?)", (1, "Dummy Question", "Math", "Dummy Answer"))
    
    DataService.save_question_attempt(session.id, 1, "ans1", True, 15.0)
    
    # Verify records exist
    student_sessions = execute_query("SELECT * FROM quiz_sessions WHERE student_id = ?", (student.id,)).fetchall()
    student_history = execute_query("SELECT ph.* FROM performance_history ph JOIN quiz_sessions qs ON ph.quiz_session_id = qs.id WHERE qs.student_id = ?", (student.id,)).fetchall()
    assert len(student_sessions) == 1
    assert len(student_history) == 1

    deleted = DataService.delete_performance_history(student.id)
    assert deleted is True

    # Verify records are deleted
    student_sessions = execute_query("SELECT * FROM quiz_sessions WHERE student_id = ?", (student.id,)).fetchall()
    student_history = execute_query("SELECT ph.* FROM performance_history ph JOIN quiz_sessions qs ON ph.quiz_session_id = qs.id WHERE qs.student_id = ?", (student.id,)).fetchall()
    assert len(student_sessions) == 0
    assert len(student_history) == 0
