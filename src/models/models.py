from services.database import execute_query, fetch_one, fetch_all

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
        cols = [col for col in self._columns if col != 'id']
        values = [getattr(self, col) for col in cols]

        if hasattr(self, 'id') and self.id is not None:
            # Update existing record
            set_clauses = [f"{col} = ?" for col in cols]
            query = f"UPDATE {self._table_name} SET {', '.join(set_clauses)} WHERE id = ?"
            execute_query(query, values + [self.id])
        else:
            # Insert new record
            placeholders = ', '.join(['?' for _ in cols])
            query = f"INSERT INTO {self._table_name} ({', '.join(cols)}) VALUES ({placeholders})"
            cursor = execute_query(query, values)
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
    _columns = ["id", "topic_id", "question_type", "prompt", "options", "correct_answer"]

    def __init__(self, id=None, topic_id=None, question_type=None, prompt=None, options=None, correct_answer=None):
        super().__init__(id=id, topic_id=topic_id, question_type=question_type, prompt=prompt, options=options, correct_answer=correct_answer)


class Progress(BaseModel):
    _table_name = "progress"
    _columns = ["id", "topic_id", "score", "last_attempted", "completed"]

    def __init__(self, id=None, topic_id=None, score=0, last_attempted=None, completed=False):
        super().__init__(id=id, topic_id=topic_id, score=score, last_attempted=last_attempted, completed=completed)
