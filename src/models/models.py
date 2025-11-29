from services.database import execute_query, fetch_one, fetch_all
import json

class BaseModel:
    _table_name = None
    _columns = []

    def __init__(self, **kwargs):
        for col in self._columns:
            setattr(self, col, kwargs.get(col))

    @classmethod
    def find_by_id(cls, id):
        query = f"SELECT * FROM {cls._table_name} WHERE id = ?"
        row = fetch_one(query, (id,))
        return cls(**row) if row else None

    @classmethod
    def find_all(cls):
        query = f"SELECT * FROM {cls._table_name}"
        rows = fetch_all(query)
        return [cls(**row) for row in rows] if rows else []

    def save(self):
        # This is a very basic save; for full ORM features, a library would be better.
        # It assumes `id` is auto-incrementing and handles new records vs updates.
        # Dynamically handle columns based on _columns attribute
        cols_for_insert = [col for col in self._columns if col != 'id']
        values_for_insert = [getattr(self, col) for col in cols_for_insert]

        if hasattr(self, 'id') and self.id is not None:
            # Update existing record
            set_clauses = [f"{col} = ?" for col in cols_for_insert]
            query = f"UPDATE {self._table_name} SET {', '.join(set_clauses)} WHERE id = ?"
            execute_query(query, values_for_insert + [self.id])
        else:
            # Insert new record
            placeholders = ', '.join(['?' for _ in cols_for_insert])
            query = f"INSERT INTO {self._table_name} ({', '.join(cols_for_insert)}) VALUES ({placeholders})"
            cursor = execute_query(query, values_for_insert)
            if cursor:
                self.id = cursor.lastrowid
        return self

    def delete(self):
        if hasattr(self, 'id') and self.id is not None:
            query = f"DELETE FROM {self._table_name} WHERE id = ?"
            execute_query(query, (self.id,))
            self.id = None


class Subject(BaseModel):
    _table_name = "subjects"
    _columns = ["id", "name"]

    def __init__(self, id=None, name=None):
        super().__init__(id=id, name=name)


class Topic(BaseModel):
    _table_name = "topics"
    _columns = ["id", "subject_id", "grade", "name"]

    def __init__(self, id=None, subject_id=None, grade=None, name=None):
        super().__init__(id=id, subject_id=subject_id, grade=grade, name=name)


class Lesson(BaseModel):
    _table_name = "lessons"
    _columns = ["id", "topic_id", "title", "content"]

    def __init__(self, id=None, topic_id=None, title=None, content=None):
        super().__init__(id=id, topic_id=topic_id, title=title, content=content)


class Question(BaseModel):
    _table_name = "questions"
    _columns = ["id", "topic_id", "question_type", "prompt", "options", "correct_answer", "explanation", "difficulty_band"]

    def __init__(self, id=None, topic_id=None, question_type=None, prompt=None, options=None, correct_answer=None, explanation=None, difficulty_band=None):
        super().__init__(id=id, topic_id=topic_id, question_type=question_type, prompt=prompt, options=options, correct_answer=correct_answer, explanation=explanation, difficulty_band=difficulty_band)
        # Ensure options is stored as a JSON string if it's a list/dict
        if isinstance(self.options, (list, dict)):
            self.options = json.dumps(self.options)

    @property
    def options_list(self):
        # Convert options back to a list when accessed
        if isinstance(self.options, str):
            return json.loads(self.options)
        return self.options


class Progress(BaseModel):
    _table_name = "progress"
    _columns = ["id", "topic_id", "score", "last_attempted", "completed"]

    def __init__(self, id=None, topic_id=None, score=0, last_attempted=None, completed=False):
        super().__init__(id=id, topic_id=topic_id, score=score, last_attempted=last_attempted, completed=completed)

class Student(BaseModel):
    _table_name = "students"
    _columns = ["id", "nickname", "current_difficulty_english", "current_difficulty_math"]

    def __init__(self, id=None, nickname=None, current_difficulty_english="Beginner", current_difficulty_math="Beginner"):
        super().__init__(id=id, nickname=nickname, current_difficulty_english=current_difficulty_english, current_difficulty_math=current_difficulty_math)

class QuizSession(BaseModel):
    _table_name = "quiz_sessions"
    _columns = ["id", "student_id", "start_time", "end_time", "subject", "difficulty_band", "overall_score"]

    def __init__(self, id=None, student_id=None, start_time=None, end_time=None, subject=None, difficulty_band=None, overall_score=None):
        super().__init__(id=id, student_id=student_id, start_time=start_time, end_time=end_time, subject=subject, difficulty_band=difficulty_band, overall_score=overall_score)

class PerformanceHistory(BaseModel):
    _table_name = "performance_history"
    _columns = ["id", "quiz_session_id", "question_id", "student_answer", "is_correct", "time_taken_seconds", "timestamp"]

    def __init__(self, id=None, quiz_session_id=None, question_id=None, student_answer=None, is_correct=None, time_taken_seconds=None, timestamp=None):
        super().__init__(id=id, quiz_session_id=quiz_session_id, question_id=question_id, student_answer=student_answer, is_correct=is_correct, time_taken_seconds=time_taken_seconds, timestamp=timestamp)
