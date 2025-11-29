import pytest
from unittest.mock import patch, MagicMock
from services.database import get_db_connection, close_db_connection, execute_query, fetch_one, fetch_all, DATABASE_FILE, DATABASE_DIR
import sqlite3
from pathlib import Path

# Mock the database file path for testing
@pytest.fixture(autouse=True)
def mock_db_paths(tmp_path):
    # Ensure DATABASE_DIR exists for mock
    Path(tmp_path / "database").mkdir(exist_ok=True)
    with patch('services.database.DATABASE_DIR', new=Path(tmp_path / "database")),
         patch('services.database.DATABASE_FILE', new=Path(tmp_path / "database" / "test.db")):
        yield

# Fixture for a mock database connection
@pytest.fixture
def mock_conn():
    with patch('sqlite3.connect') as mock_connect:
        mock_db_connection = MagicMock()
        mock_connect.return_value = mock_db_connection
        yield mock_db_connection

def test_get_db_connection_creates_dir_and_connects(mock_conn, tmp_path):
    # Ensure DATABASE_DIR doesn't exist initially for this test
    (Path(tmp_path / "database")).rmdir() 
    
    conn = get_db_connection()
    mock_conn.assert_called_once_with(DATABASE_FILE)
    assert Path(tmp_path / "database").exists()
    assert conn.row_factory is sqlite3.Row

def test_close_db_connection_closes_if_exists():
    mock_db_connection = MagicMock()
    close_db_connection(mock_db_connection)
    mock_db_connection.close.assert_called_once()

def test_close_db_connection_does_nothing_if_none():
    mock_db_connection = None
    close_db_connection(mock_db_connection) # Should not raise error

def test_execute_query_success(mock_conn):
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    query = "INSERT INTO test_table (name) VALUES (?)"
    params = ("test_name",)
    
    result_cursor = execute_query(query, params)
    
    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(query, params)
    mock_conn.commit.assert_called_once()
    assert result_cursor == mock_cursor

def test_execute_query_error(mock_conn):
    mock_conn.cursor.side_effect = sqlite3.Error("Test Error")
    
    with patch('builtins.print') as mock_print:
        result = execute_query("SELECT * FROM non_existent_table")
        mock_print.assert_called_with("Database error: Test Error")
        assert result is None

def test_fetch_one_success(mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {"id": 1, "name": "Test"}
    mock_conn.cursor.return_value = mock_cursor

    query = "SELECT * FROM test_table WHERE id = ?"
    params = (1,)
    
    result = fetch_one(query, params)
    
    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(query, params)
    mock_cursor.fetchone.assert_called_once()
    assert result == {"id": 1, "name": "Test"}

def test_fetch_one_no_result(mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    mock_conn.cursor.return_value = mock_cursor

    result = fetch_one("SELECT * FROM test_table WHERE id = 99")
    assert result is None

def test_fetch_all_success(mock_conn):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [{"id": 1, "name": "Test1"}, {"id": 2, "name": "Test2"}]
    mock_conn.cursor.return_value = mock_cursor

    query = "SELECT * FROM test_table"
    result = fetch_all(query)
    
    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(query, ()) # default params
    mock_cursor.fetchall.assert_called_once()
    assert len(result) == 2
    assert result[0]["name"] == "Test1"
