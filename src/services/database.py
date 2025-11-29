import sqlite3
from pathlib import Path
import datetime

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

    # Alter questions table to add new columns if they don't exist
    # Check if 'explanation' column exists
    cursor.execute("PRAGMA table_info(questions)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'explanation' not in columns:
        cursor.execute("ALTER TABLE questions ADD COLUMN explanation TEXT")
    if 'difficulty_band' not in columns:
        cursor.execute("ALTER TABLE questions ADD COLUMN difficulty_band TEXT")

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