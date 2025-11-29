# Quickstart Guide: LLM Dynamic Quiz and Feedback

**Feature Branch**: `001-llm-quiz-feedback`
**Date**: 2025-11-29

This guide provides instructions to quickly set up and run the LLM Dynamic Quiz and Feedback feature.

## Prerequisites

*   Python 3.11 installed.
*   Access to the Gemini API (ensure you have an API key).
*   The project's virtual environment is set up and activated.

## Setup

1.  **Environment Variable**: Set your Gemini API key as an environment variable named `GEMINI_API_KEY`.
    *   **Windows (Command Prompt)**: `set GEMINI_API_KEY=YOUR_API_KEY_HERE`
    *   **Windows (PowerShell)**: `$env:GEMINI_API_KEY="YOUR_API_KEY_HERE"`
    *   **Linux/macOS**: `export GEMINI_API_KEY=YOUR_API_KEY_HERE`

2.  **Install Dependencies**: Ensure all project dependencies are installed.
    ```bash
    pip install -r requirements.txt
    ```

## Running the Feature

1.  **Start the application**: Run the main Python script.
    ```bash
    python src/main.py
    ```
2.  Navigate to the English section.
3.  Select a lesson.
4.  Click "Start Dynamic English Quiz" to begin generating questions from the LLM.

## Testing

1.  **Run unit tests**:
    ```bash
    pytest tests/unit/test_llm_service.py
    pytest tests/unit/test_data_service.py
    pytest tests/unit/test_adaptive_learning_service.py
    pytest tests/unit/test_ui.py
    ```
    Or to run all unit tests:
    ```bash
    pytest tests/unit/
    ```
2.  **Run integration tests**: (Once `test_app_flow.py` is implemented)
    ```bash
    pytest tests/integration/test_app_flow.py
    ```
    Or to run all integration tests:
    ```bash
    pytest tests/integration/
    ```