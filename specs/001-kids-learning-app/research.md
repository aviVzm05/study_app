# Technology Research & Decisions

**Feature**: Kids Learning App

This document records the key technology decisions made for the project.

---

## GUI Framework

- **Decision**: PyQt6
- **Rationale**: The user requested a Python technical stack. PyQt6 is a modern, feature-rich, and widely used library for creating desktop applications with Python. It provides a good set of UI components that will be needed for this interactive learning application. It also has good cross-platform support.
- **Alternatives considered**:
    - **Tkinter**: Built-in to Python, but the UI can look dated and it has fewer advanced widgets compared to PyQt.
    - **Kivy**: Good for multi-touch applications and has a novel UI design approach, but can have a steeper learning curve for standard desktop applications. PyQt is more traditional and straightforward for this project's needs.

---

## Database

- **Decision**: SQLite
- **Rationale**: The user requested a local database, and the application has an offline-first requirement. SQLite is a serverless, self-contained, transactional SQL database engine that is included in Python's standard library. It's the perfect choice for a local, file-based database. It requires no separate server process and is easy to bundle with the application.
- **Alternatives considered**:
    - **JSON files**: Simple to implement, but can become unwieldy for relational data (like students, subjects, topics, questions). A proper database like SQLite is better for managing these relationships and ensuring data integrity.
    - **Other embedded databases (e.g., TinyDB)**: While viable, SQLite's inclusion in the standard library and its robust SQL support make it the default, most reliable choice for this type of application.
