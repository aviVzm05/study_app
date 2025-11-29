# Local Data Interface Contract

## Entity: Student

### `get_student_profile(student_id)`
- **Input**: `student_id` (string)
- **Output**: `Student` object or `None`

### `create_student_profile(nickname)`
- **Input**: `nickname` (string)
- **Output**: `Student` object

### `update_student_profile(student_id, difficulty_english, difficulty_math)`
- **Input**: `student_id` (string), `difficulty_english` (string), `difficulty_math` (string)
- **Output**: `Student` object or `None` if not found

## Entity: Performance History

### `save_question_attempt(quiz_session_id, question_id, student_answer, is_correct, time_taken_seconds)`
- **Input**: `quiz_session_id` (string), `question_id` (string), `student_answer` (string), `is_correct` (boolean), `time_taken_seconds` (float)
- **Output**: `PerformanceHistory` object

### `get_performance_history(student_id, subject, limit)`
- **Input**: `student_id` (string), `subject` (string, optional), `limit` (integer, optional)
- **Output**: List of `PerformanceHistory` objects

### `delete_performance_history(student_id)`
- **Input**: `student_id` (string)
- **Output**: Boolean indicating success

## Entity: Quiz Session

### `start_quiz_session(student_id, subject, difficulty_band)`
- **Input**: `student_id` (string), `subject` (string), `difficulty_band` (string)
- **Output**: `QuizSession` object

### `end_quiz_session(session_id, overall_score)`
- **Input**: `session_id` (string), `overall_score` (integer or float)
- **Output**: `QuizSession` object or `None` if not found
