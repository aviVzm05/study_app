from services.database import execute_query

def create_schema():
    """Creates the database schema based on the data model."""
    queries = [
        """
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            grade INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (subject_id) REFERENCES subjects (id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (topic_id) REFERENCES topics (id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL,
            question_type TEXT NOT NULL,
            prompt TEXT NOT NULL,
            options TEXT,
            correct_answer TEXT NOT NULL,
            FOREIGN KEY (topic_id) REFERENCES topics (id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL UNIQUE,
            score INTEGER NOT NULL DEFAULT 0,
            last_attempted DATETIME NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY (topic_id) REFERENCES topics (id)
        );
        """
    ]
    for query in queries:
        execute_query(query)
    print("Database schema created or updated.")

if __name__ == '__main__':
    create_schema()
