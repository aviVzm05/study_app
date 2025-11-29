import logging
from services.data_service import DataService

logger = logging.getLogger(__name__)

class AdaptiveLearningService:
    # FR-011: Explicit mappings for difficulty bands to grade ranges
    DIFFICULTY_GRADE_MAP = {
        "Beginner": {"min_grade": 5, "max_grade": 7},
        "Intermediate": {"min_grade": 8, "max_grade": 9},
        "Advanced": {"min_grade": 10, "max_grade": 10},
        # Assuming grade 10 is the max target based on constitution
    }

    # Parameters for adaptation logic
    CORRECT_STREAK_FOR_UPGRADE = 3
    INCORRECT_STREAK_FOR_DOWNGRADE = 2
    RECENT_HISTORY_LIMIT = 10 # Look at last 10 questions for streak

    @staticmethod
    def _get_difficulty_levels():
        """Returns ordered difficulty levels."""
        return ["Beginner", "Intermediate", "Advanced"]

    @staticmethod
    def analyze_performance_and_suggest_next(student_id: int, subject: str) -> tuple[str, str]:
        """
        Analyzes student performance history for a given subject and suggests
        the next difficulty band and context for the LLM prompt.
        Incorporates FR-011 (difficulty to grade mapping) implicitly for educational context.
        """
        student = DataService.get_student_profile(student_id)
        if not student:
            logger.warning(f"Student {student_id} not found. Suggesting Beginner difficulty.")
            return "Beginner", "Student profile not found. Start with foundational questions."

        current_difficulty = getattr(student, f"current_difficulty_{subject.lower()}", "Beginner")
        history = DataService.get_performance_history(student_id, subject, AdaptiveLearningService.RECENT_HISTORY_LIMIT)
        
        correct_streak = 0
        incorrect_streak = 0
        performance_summary = []

        if not history:
            logger.info(f"No recent history for student {student_id} in {subject}. Recommending current difficulty: {current_difficulty}.")
            return current_difficulty, f"No recent performance data for {subject}. Generate questions suitable for {current_difficulty} level."

        for attempt in history:
            performance_summary.append(f"{'Correct' if attempt.is_correct else 'Incorrect'} (Q: {attempt.question_id}, Ans: {attempt.student_answer})")
            if attempt.is_correct:
                correct_streak += 1
                incorrect_streak = 0
            else:
                incorrect_streak += 1
                correct_streak = 0
            
            # Break streaks if opposite answer is encountered
            if correct_streak > 0 and not attempt.is_correct:
                correct_streak = 0
            if incorrect_streak > 0 and attempt.is_correct:
                incorrect_streak = 0

        next_difficulty = current_difficulty
        difficulty_levels = AdaptiveLearningService._get_difficulty_levels()
        current_difficulty_index = difficulty_levels.index(current_difficulty)

        # Logic for upgrading difficulty
        if correct_streak >= AdaptiveLearningService.CORRECT_STREAK_FOR_UPGRADE and current_difficulty_index < len(difficulty_levels) - 1:
            next_difficulty = difficulty_levels[current_difficulty_index + 1]
            logger.info(f"Student {student_id} has a correct streak. Upgrading {subject} difficulty to {next_difficulty}.")
            # Update student profile
            setattr(student, f"current_difficulty_{subject.lower()}", next_difficulty)
            student.save()
            context = f"Student shows strong understanding. Generate {subject} questions at {next_difficulty} level. Recent attempts: {', '.join(performance_summary)}."
            return next_difficulty, context
        
        # Logic for downgrading difficulty
        if incorrect_streak >= AdaptiveLearningService.INCORRECT_STREAK_FOR_DOWNGRADE and current_difficulty_index > 0:
            next_difficulty = difficulty_levels[current_difficulty_index - 1]
            logger.info(f"Student {student_id} has an incorrect streak. Downgrading {subject} difficulty to {next_difficulty}.")
            # Update student profile
            setattr(student, f"current_difficulty_{subject.lower()}", next_difficulty)
            student.save()
            context = f"Student is struggling. Generate {subject} questions at {next_difficulty} level. Focus on fundamental concepts. Recent attempts: {', '.join(performance_summary)}."
            return next_difficulty, context

        # If no significant streak, maintain current difficulty
        logger.info(f"Student {student_id} maintaining {subject} difficulty at {current_difficulty}. Recent performance: {', '.join(performance_summary)}.")
        context = f"Student maintaining current performance. Generate {subject} questions at {current_difficulty} level. Recent attempts: {', '.join(performance_summary)}."
        return current_difficulty, context

if __name__ == '__main__':
    from services.logging_service import setup_logging
    from services.database import get_db_connection, close_db_connection, execute_query

    setup_logging()
    conn = get_db_connection() # Ensure tables are created

    # Clear old data for consistent testing
    execute_query("DELETE FROM students")
    execute_query("DELETE FROM quiz_sessions")
    execute_query("DELETE FROM performance_history")
    
    # Create a dummy student
    student = DataService.create_student_profile(nickname="TestKid")
    print(f"Created student: {student.nickname} (ID: {student.id})")

    # Simulate some performance history
    session1 = DataService.start_quiz_session(student.id, "English", "Beginner")
    DataService.save_question_attempt(session1.id, 1, "ans1", True, 10.0)
    DataService.save_question_attempt(session1.id, 2, "ans2", True, 12.0)
    DataService.save_question_attempt(session1.id, 3, "ans3", True, 8.0) # Correct streak of 3
    DataService.end_quiz_session(session1.id, 100.0)

    # Analyze and suggest next difficulty
    print("\n--- After a correct streak ---")
    next_diff, context = AdaptiveLearningService.analyze_performance_and_suggest_next(student.id, "English")
    print(f"Suggested next difficulty: {next_diff}")
    print(f"Context for LLM: {context}")
    updated_student = DataService.get_student_profile(student.id)
    print(f"Student's current English difficulty: {updated_student.current_difficulty_english}")


    session2 = DataService.start_quiz_session(student.id, "English", "Intermediate")
    DataService.save_question_attempt(session2.id, 4, "ans4", False, 15.0)
    DataService.save_question_attempt(session2.id, 5, "ans5", False, 11.0) # Incorrect streak of 2
    DataService.end_quiz_session(session2.id, 0.0)

    print("\n--- After an incorrect streak ---")
    next_diff, context = AdaptiveLearningService.analyze_performance_and_suggest_next(student.id, "English")
    print(f"Suggested next difficulty: {next_diff}")
    print(f"Context for LLM: {context}")
    updated_student = DataService.get_student_profile(student.id)
    print(f"Student's current English difficulty: {updated_student.current_difficulty_english}")
    
    close_db_connection(conn)
