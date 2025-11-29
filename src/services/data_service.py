import logging
from models.models import Student, QuizSession, PerformanceHistory
from services.database import execute_query, fetch_one, fetch_all

logger = logging.getLogger(__name__)

class DataService:

    @staticmethod
    def get_student_profile(student_id: int) -> Student | None:
        """Retrieves a student profile by ID."""
        logger.info(f"Fetching student profile for ID: {student_id}")
        return Student.find_by_id(student_id)

    @staticmethod
    def create_student_profile(nickname: str) -> Student:
        """Creates a new student profile."""
        logger.info(f"Creating student profile for nickname: {nickname}")
        student = Student(nickname=nickname)
        student.save()
        return student

    @staticmethod
    def update_student_profile(student_id: int, difficulty_english: str = None, difficulty_math: str = None) -> Student | None:
        """Updates an existing student profile's difficulty settings."""
        student = DataService.get_student_profile(student_id)
        if student:
            logger.info(f"Updating student profile for ID: {student_id}")
            if difficulty_english:
                student.current_difficulty_english = difficulty_english
            if difficulty_math:
                student.current_difficulty_math = difficulty_math
            student.save()
        else:
            logger.warning(f"Student with ID {student_id} not found for update.")
        return student

    # Other CRUD operations will be added in subsequent tasks

    @staticmethod
    def start_quiz_session(student_id: int, subject: str, difficulty_band: str) -> QuizSession:
        """Starts a new quiz session."""
        from datetime import datetime
        logger.info(f"Starting quiz session for student {student_id}, subject {subject}, difficulty {difficulty_band}")
        session = QuizSession(
            student_id=student_id,
            start_time=datetime.now().isoformat(),
            subject=subject,
            difficulty_band=difficulty_band
        )
        session.save()
        return session

    @staticmethod
    def end_quiz_session(session_id: int, overall_score: float) -> QuizSession | None:
        """Ends an existing quiz session, updating the end time and score."""
        from datetime import datetime
        session = QuizSession.find_by_id(session_id)
        if session:
            logger.info(f"Ending quiz session {session_id} with score {overall_score}")
            session.end_time = datetime.now().isoformat()
            session.overall_score = overall_score
            session.save()
        else:
            logger.warning(f"Quiz session with ID {session_id} not found for ending.")
        return session

    @staticmethod
    def save_question_attempt(quiz_session_id: int, question_id: int | None, student_answer: str, is_correct: bool, time_taken_seconds: float) -> PerformanceHistory:
        """Saves a student's attempt at a question."""
        from datetime import datetime
        logger.info(f"Saving attempt for session {quiz_session_id}, question {question_id}, correct: {is_correct}")
        attempt = PerformanceHistory(
            quiz_session_id=quiz_session_id,
            question_id=question_id,
            student_answer=student_answer,
            is_correct=is_correct,
            time_taken_seconds=time_taken_seconds,
            timestamp=datetime.now().isoformat()
        )
        attempt.save()
        return attempt

    @staticmethod
    def get_performance_history(student_id: int, subject: str = None, limit: int = None) -> list[PerformanceHistory]:
        """Retrieves performance history for a student, optionally filtered by subject and limited."""
        logger.info(f"Fetching performance history for student {student_id}, subject: {subject}, limit: {limit}")
        
        # This requires joining with QuizSession to filter by student_id and subject
        query = """
            SELECT ph.* FROM performance_history ph
            JOIN quiz_sessions qs ON ph.quiz_session_id = qs.id
            WHERE qs.student_id = ?
        """
        params = [student_id]
        
        if subject:
            query += " AND qs.subject = ?"
            params.append(subject)
        
        query += " ORDER BY ph.timestamp DESC"
        
        if limit:
            query += f" LIMIT {limit}"
        
        rows = execute_query(query, params, conn=True) # Pass conn=True to prevent auto-closing
        return [PerformanceHistory(**row) for row in rows] if rows else []

    @staticmethod
    def delete_performance_history(student_id: int) -> bool:
        """Deletes all performance history and quiz sessions for a given student."""
        logger.warning(f"Deleting all performance history and quiz sessions for student ID: {student_id}")
        try:
            # Delete performance history records linked to the student's quiz sessions
            execute_query("""
                DELETE FROM performance_history
                WHERE quiz_session_id IN (SELECT id FROM quiz_sessions WHERE student_id = ?)
            """, (student_id,))
            
            # Delete the quiz sessions themselves
            execute_query("DELETE FROM quiz_sessions WHERE student_id = ?", (student_id,))
            
            logger.info(f"Successfully deleted performance history and quiz sessions for student ID: {student_id}.")
            return True
        except Exception as e:
            logger.error(f"Error deleting performance history for student {student_id}: {e}")
            return False


