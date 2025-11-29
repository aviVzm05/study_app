# Data Model: LLM Dynamic Quiz and Feedback

**Feature Branch**: `001-llm-quiz-feedback`  
**Date**: 2025-11-29  

## Entities

### Student

*   **Description**: A user of the learning application, identified by a unique ID.
*   **Attributes**:
    *   `id`: Unique identifier (e.g., UUID or integer, primary key)
    *   `nickname`: Display name for the student (string)
    *   `current_difficulty_english`: Current difficulty band for English (string, e.g., "Beginner", "Intermediate", "Advanced")
    *   `current_difficulty_math`: Current difficulty band for Math (string, e.g., "Beginner", "Intermediate", "Advanced")

### Question

*   **Description**: A dynamically generated quiz item.
*   **Attributes**:
    *   `id`: Unique identifier (e.g., UUID or integer, primary key)
    *   `question_text`: The text of the question (string)
    *   `possible_answers`: List of possible answers (list of strings, if multiple choice)
    *   `correct_answer`: The correct answer (string)
    *   `explanation`: Explanation of the correct answer (string)
    *   `subject`: The subject of the question (string, e.g., "English", "Math")
    *   `difficulty_band`: The difficulty band of the question (string, e.g., "Beginner", "Intermediate", "Advanced")

### Quiz Session

*   **Description**: A record of a student's interaction with a set of questions.
*   **Attributes**:
    *   `id`: Unique identifier (e.g., UUID or integer, primary key)
    *   `student_id`: Foreign key referencing Student.id
    *   `start_time`: Timestamp when the session began
    *   `end_time`: Timestamp when the session ended
    *   `subject`: Subject of the quiz (string)
    *   `difficulty_band`: Overall difficulty band for the session (string)
    *   `overall_score`: Score for the session (e.g., percentage, integer)

### Performance History (Question Attempt)

*   **Description**: A collection of individual question attempts.
*   **Attributes**:
    *   `id`: Unique identifier (e.g., UUID or integer, primary key)
    *   `quiz_session_id`: Foreign key referencing QuizSession.id
    *   `question_id`: Foreign key referencing Question.id (optional, if questions are cached or stored)
    *   `student_answer`: The answer provided by the student (string)
    *   `is_correct`: Boolean indicating if the student's answer was correct
    *   `time_taken_seconds`: Time taken to answer the question (integer or float)
    *   `timestamp`: Timestamp of the attempt

### LLM Prompt

*   **Description**: The input provided to the LLM to generate questions.
*   **Attributes**:
    *   `id`: Unique identifier (e.g., UUID or integer, primary key)
    *   `subject`: Subject for which to generate questions (string)
    *   `difficulty_band`: Difficulty band for question generation (string)
    *   `context`: Additional context for LLM (e.g., "based on previous performance, focus on fractions") (string)
    *   `generated_at`: Timestamp when the prompt was used for generation
