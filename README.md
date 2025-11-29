# Kids Learning App

This is a desktop learning application for students in Grade 5, focusing on Mathematics and English. The application is built using Python with the PyQt6 GUI framework and uses a local SQLite database for offline content storage.

---

## Features

- **Grade and Topic Selection**: Users can select from various Math and English topics available exclusively for Grade 5.
- **Math Skill Building**: Interactive lessons and practice problems for Grade 5 Math, covering Decimals, Number System & Operations (Word Problems, LCM, HCF, Mean, Median, Mode, Multiplication, Division), Integers, Rational Numbers, Geometry, Algebra, and Data Handling.
- **English Writing Practice**: Exercises for Grade 5 English, including Nouns, Spelling Tests (simple and moderate words), and Grammar Practice (fundamentals, punctuation, capitalization), with immediate feedback.
- **Offline Accessibility**: All learning content and progress tracking are available without an internet connection.
- **Progress Tracking**: Local storage of user progress for each topic.

---

## Technology Stack

- **Language**: Python 3.11+
- **GUI Framework**: PyQt6
- **Database**: SQLite (local, file-based)
- **Testing**: pytest

---

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment**:
    
    On Windows (PowerShell):
    ```powershell
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```
    On macOS/Linux (Bash):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

---

## Database Initialization and Seeding

The application uses a local SQLite database (`database/content.db`). The schema is automatically created and initial data (all content exclusively for Grade 5) is seeded when the application starts for the first time.

---

## Running the Application

After setup, activate your virtual environment and run:

```bash
python src/main.py
```

---

## Running Tests

Activate your virtual environment and run `pytest` from the project root:

```bash
pytest
```

---

## Project Structure

```
.
├── .gitignore
├── pytest.ini
├── requirements.txt
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── models.py       # Data models for tables
│   │   └── schema.py       # Database schema creation
│   ├── services/
│   │   ├── __init__.py
│   │   ├── database.py     # SQLite connection and queries
│   │   ├── data_seeder.py  # Initial data seeding
│   │   ├── english_service.py # Fetch English lessons/questions
│   │   ├── english_validation.py # English grammar/spelling validation
│   │   ├── logging_service.py # Application logging
│   │   ├── math_service.py # Fetch Math lessons/questions
│   │   └── math_validation.py # Math answer validation
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── english_exercise_view.py # UI for English exercises
│   │   ├── grade_selection_view.py # UI for grade selection
│   │   ├── math_lesson_view.py # UI for Math lessons/problems
│   │   └── topic_selection_view.py # UI for subject/topic selection
│   └── main.py             # Application entry point
├── tests/
│   ├── integration/
│   │   └── test_app_flow.py # Integration tests for main app flow
│   └── unit/
│       ├── test_database.py # Unit tests for database service
│       ├── test_english_service.py # Unit tests for English service
│       └── test_math_service.py # Unit tests for Math service
└── database/
    └── content.db          # SQLite database file (generated on first run)
```
