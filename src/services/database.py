import sqlite3
from pathlib import Path

DATABASE_DIR = Path(__file__).parent.parent.parent / "database"
DATABASE_FILE = DATABASE_DIR / "content.db"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    if not DATABASE_DIR.exists():
        DATABASE_DIR.mkdir()
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def close_db_connection(conn):
    """Closes the database connection."""
    if conn:
        conn.close()

def execute_query(query, params=()):
    """Executes a given SQL query with optional parameters."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        close_db_connection(conn)

def fetch_one(query, params=()):
    """Fetches a single row from the database."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        close_db_connection(conn)

def fetch_all(query, params=()):
    """Fetches all rows from the database."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        close_db_connection(conn)

if __name__ == '__main__':
    # Example usage:
    print("Initializing database connection...")
    conn = get_db_connection()
    if conn:
        print("Connection successful.")
        close_db_connection(conn)
        print("Connection closed.")
