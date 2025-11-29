import sqlite3
from pathlib import Path

DATABASE_DIR = Path(__file__).parent.parent.parent / "database"
DATABASE_FILE = DATABASE_DIR / "content.db"

def get_db_connection():
    """Establishes a connection to the SQLite database and ensures tables are created."""
    if not DATABASE_DIR.exists():
        DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    
    # Ensure tables are created on connection
    create_tables(conn)
    
    return conn

def close_db_connection(conn):
    """Closes the database connection."""
    if conn:
        conn.close()

def execute_query(query, params=(), conn=None):
    """Executes a given SQL query with optional parameters."""
    local_conn = False
    if conn is None:
        conn = get_db_connection()
        local_conn = True
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if local_conn and conn:
            close_db_connection(conn)

def fetch_one(query, params=(), conn=None):
    """Fetches a single row from the database."""
    local_conn = False
    if conn is None:
        conn = get_db_connection()
        local_conn = True
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if local_conn and conn:
            close_db_connection(conn)

def fetch_all(query, params=(), conn=None):
    """Fetches all rows from the database."""
    local_conn = False
    if conn is None:
        conn = get_db_connection()
        local_conn = True
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if local_conn and conn:
            close_db_connection(conn)

def create_tables(conn):
    """Creates all necessary database tables."""
    cursor = conn.cursor()

    # Create students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT NOT NULL,
            current_difficulty_english TEXT DEFAULT 'Beginner',
            current_difficulty_math TEXT DEFAULT 'Beginner'
        )
    """)

    # Create subjects table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    # Create topics table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            grade INTEGER NOT NULL,
            name TEXT NOT NULL,
            FOREIGN KEY (subject_id) REFERENCES subjects (id)
        )
    """)

    # Create lessons table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (topic_id) REFERENCES topics (id)
        )
    """)

    # Create questions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id INTEGER,
            question_type TEXT,
            prompt TEXT NOT NULL,
            options TEXT,
            correct_answer TEXT,
            explanation TEXT,
            difficulty_band TEXT,
            subject TEXT NOT NULL, -- Added subject column
            FOREIGN KEY (topic_id) REFERENCES topics (id)
        )
    """)

    # Create quiz_sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT,
            subject TEXT NOT NULL,
            difficulty_band TEXT NOT NULL,
            overall_score REAL,
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    """)

    # Create performance_history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_session_id INTEGER NOT NULL,
            question_id INTEGER,
            student_answer TEXT,
            is_correct INTEGER,
            time_taken_seconds REAL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (quiz_session_id) REFERENCES quiz_sessions (id),
            FOREIGN KEY (question_id) REFERENCES questions (id)
        )
    """)
    conn.commit()


if __name__ == '__main__':
    print("Initializing database connection and tables...")
    conn = get_db_connection()
    if conn:
        print("Connection successful and tables ensured.")
        
        # Example usage:
        # from models.models import Student, Subject, Topic, Lesson, Question as StaticQuestion, Progress
        # # Assuming you have an existing setup for subjects, topics, lessons
        
        close_db_connection(conn)
        print("Connection closed.")