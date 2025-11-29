# Quickstart Guide

**Feature**: Kids Learning App

This guide explains how to set up the development environment and run the application.

---

## Prerequisites

- Python 3.11 or later
- `pip` for package management
- `venv` for creating virtual environments

---

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment**:
    
    On Windows:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

    On macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    Create a `requirements.txt` file with the following content:
    ```
    PyQt6
    pytest
    ```
    Then install the packages:
    ```bash
    pip install -r requirements.txt
    ```

---

## Database

The application uses a pre-populated SQLite database named `content.db`. This file should be placed in the `database/` directory at the root of the project.

For the initial MVP, this database will need to be created and populated manually with the curriculum content (1 topic per subject per grade).

---

## Running the Application

Once the setup is complete, you can run the application from the project root directory:

```bash
python src/main.py
```

---

## Running Tests

To run the unit and integration tests, use `pytest`:

```bash
pytest
```
