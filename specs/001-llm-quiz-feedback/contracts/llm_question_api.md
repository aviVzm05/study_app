# LLM Question Generation API Contract

**Endpoint**: Gemini API (external)

## Request (Input to LLM)

**Action**: Generate Questions

**Parameters**:
- `subject` (string, required): e.g., "English", "Math"
- `difficulty_band` (string, required): e.g., "Beginner", "Intermediate", "Advanced"
- `num_questions` (integer, optional, default: 1): Number of questions to generate.
- `context_history` (string, optional): A summary or specific examples from the student's performance history to guide question generation.
- `output_format` (string, required): Expected format for the LLM response, e.g., JSON with question text, options, correct answer, explanation.

## Response (Output from LLM)

**Status**: Success (200 OK) or Error (4xx/5xx)

**Body (JSON)**:
- `questions` (array of objects):
    - `question_text` (string): The generated question.
    - `possible_answers` (array of strings, optional): List of choices for multiple-choice questions.
    - `correct_answer` (string): The correct answer.
    - `explanation` (string): Detailed explanation of the answer.
    - `subject` (string): Subject of the question.
    - `difficulty_band` (string): Difficulty of the question.

**Error Response**:
- `error` (string): Error message.
- `code` (integer): Error code.