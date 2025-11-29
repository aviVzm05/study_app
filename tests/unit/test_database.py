import pytest
from unittest.mock import patch, MagicMock
from services.database import get_db_connection, close_db_connection, execute_query, fetch_one, fetch_all, DATABASE_FILE, DATABASE_DIR, create_tables
import sqlite3
from pathlib import Path

# Mock the database file path for testing
@pytest.fixture(autouse=True)
def mock_db_paths(tmp_path):
    # Ensure DATABASE_DIR exists for mock
    Path(tmp_path / "database").mkdir(exist_ok=True)
    with patch('services.database.DATABASE_DIR', new=Path(tmp_path / "database")):
        with patch('services.database.DATABASE_FILE', new=Path(tmp_path / "database" / "test.db")):
            yield

# Fixture for mocking get_db_connection for tests that use execute_query, fetch_one, fetch_all
@pytest.fixture
def mock_connection_for_queries():
    with patch('services.database.get_db_connection') as mock_get_db_conn:
        mock_conn_instance = MagicMock()
        mock_cursor_instance = MagicMock()
        mock_conn_instance.cursor.return_value = mock_cursor_instance
        mock_get_db_conn.return_value = mock_conn_instance
        yield mock_conn_instance, mock_cursor_instance

def test_get_db_connection_creates_dir_and_connects(tmp_path):
    # Ensure DATABASE_DIR doesn't exist initially for this test
    # This specific test will use the real sqlite3.connect, but we mock create_tables
    (Path(tmp_path / "database")).rmdir() 
    
    with patch('sqlite3.connect') as mock_connect, \
         patch('services.database.create_tables') as mock_create_tables:
        mock_db_connection = MagicMock()
        mock_connect.return_value = mock_db_connection
        
        conn = get_db_connection()
        expected_db_file = Path(tmp_path / "database" / "test.db")
        mock_connect.assert_called_once_with(expected_db_file)
        mock_create_tables.assert_called_once_with(mock_db_connection)
        assert Path(tmp_path / "database").exists()
        assert conn.row_factory is sqlite3.Row

def test_close_db_connection_closes_if_exists():
    mock_db_connection = MagicMock()
    close_db_connection(mock_db_connection)
    mock_db_connection.close.assert_called_once()

def test_close_db_connection_does_nothing_if_none():
    mock_db_connection = None
    close_db_connection(mock_db_connection) # Should not raise error

def test_execute_query_success(mock_connection_for_queries):
    mock_conn, mock_cursor = mock_connection_for_queries

    query = "INSERT INTO test_table (name) VALUES (?)"
    params = ("test_name",)
    
    result_cursor = execute_query(query, params)
    
    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(query, params)
    mock_conn.commit.assert_called_once()
    assert result_cursor == mock_cursor

def test_execute_query_error(mock_connection_for_queries):
    mock_conn, mock_cursor = mock_connection_for_queries
    mock_cursor.execute.side_effect = sqlite3.Error("Test Error") # Error during execute

    with patch('builtins.print') as mock_print:
        result = execute_query("SELECT * FROM non_existent_table")
        mock_print.assert_called_with("Database error: Test Error")
        assert result is None
    # Ensure connection is closed if it was opened locally within execute_query
    mock_conn.close.assert_called_once() # Should be closed due to local_conn logic

def test_fetch_one_success(mock_connection_for_queries):
    mock_conn, mock_cursor = mock_connection_for_queries
    mock_cursor.fetchone.return_value = {"id": 1, "name": "Test"}

    query = "SELECT * FROM test_table WHERE id = ?"
    params = (1,)
    
    result = fetch_one(query, params)
    
    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(query, params)
    mock_cursor.fetchone.assert_called_once()
    assert result == {"id": 1, "name": "Test"}
    mock_conn.close.assert_called_once()

def test_fetch_one_no_result(mock_connection_for_queries):
    mock_conn, mock_cursor = mock_connection_for_queries
    mock_cursor.fetchone.return_value = None

    result = fetch_one("SELECT * FROM test_table WHERE id = 99")
    assert result is None
    mock_conn.close.assert_called_once()

def test_fetch_all_success(mock_connection_for_queries):
    mock_conn, mock_cursor = mock_connection_for_queries
    mock_cursor.fetchall.return_value = [{"id": 1, "name": "Test1"}, {"id": 2, "name": "Test2"}]

    query = "SELECT * FROM test_table"
    result = fetch_all(query)
    
    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once_with(query, ()) # default params
    mock_cursor.fetchall.assert_called_once()
    assert len(result) == 2
    assert result[0]["name"] == "Test1"
    mock_conn.close.assert_called_once()

def test_fetch_all_error(mock_connection_for_queries):
    mock_conn, mock_cursor = mock_connection_for_queries
    mock_cursor.execute.side_effect = sqlite3.Error("Test Error Fetch All")

    with patch('builtins.print') as mock_print:
        result = fetch_all("SELECT * FROM non_existent_table_all")
        mock_print.assert_called_with("Database error: Test Error Fetch All")
        assert result is None
    mock_conn.close.assert_called_once()

@pytest.fixture
def mock_create_tables():
    with patch('services.database.create_tables') as mock_ct:
        yield mock_ct

def test_create_tables(mock_create_tables):
    # This test ensures create_tables is called by get_db_connection
    # We will test the actual SQL in an integration test or a more specific unit test
    conn = MagicMock()
    create_tables(conn)
    # Just ensure it doesn't raise errors and calls commit (implicitly from execute)
    conn.commit.assert_called_once()
