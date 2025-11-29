# Data Model

**Feature**: Kids Learning App
**Storage**: SQLite

This document defines the database schema for the `content.db` SQLite database.

---

## ERD (Entity Relationship Diagram) - Conceptual

```
+----------+       +---------+       +---------+
| Subject  |-------|  Topic  |-------|  Lesson |
+----------+       +---------+       +---------+
     |                   |
     |                   |
     +-------------------|
                         |
                     +----------+
                     | Question |
                     +----------+

+----------+       +----------+
| Progress |-------|  Topic   |
+----------+       +----------+
```

---

## Tables

### `subjects`

Stores the main learning subjects.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY | Unique identifier for the subject. |
| `name` | TEXT | NOT NULL | The name of the subject (e.g., "Mathematics", "English"). |

### `topics`

Stores the topics within each subject.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY | Unique identifier for the topic. |
| `subject_id` | INTEGER | FOREIGN KEY (subjects.id) | The subject this topic belongs to. |
| `grade` | INTEGER | NOT NULL | The grade level for this topic (5-10). |
| `name` | TEXT | NOT NULL | The name of the topic (e.g., "Fractions", "Verb Tenses"). |

### `lessons`

Stores the instructional content for each topic.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY | Unique identifier for the lesson. |
| `topic_id` | INTEGER | FOREIGN KEY (topics.id) | The topic this lesson belongs to. |
| `title` | TEXT | NOT NULL | The title of the lesson. |
| `content` | TEXT | NOT NULL | The instructional content (can be Markdown or plain text). |

### `questions`

Stores the quiz questions for each topic.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY | Unique identifier for the question. |
| `topic_id` | INTEGER | FOREIGN KEY (topics.id) | The topic this question belongs to. |
| `question_type` | TEXT | NOT NULL | Type of question (e.g., "multiple_choice", "fill_in_the_blank", "sentence_construction"). |
| `prompt` | TEXT | NOT NULL | The question prompt or text. |
| `options` | TEXT | | JSON-formatted string for multiple choice options. |
| `correct_answer` | TEXT | NOT NULL | The correct answer. For sentence construction, this could be a reference answer or validation rule. |

### `progress`

Stores the user's progress on different topics. Since the user is anonymous, this table tracks progress for the local device.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY | Unique identifier for the progress entry. |
| `topic_id` | INTEGER | UNIQUE, FOREIGN KEY (topics.id) | The topic for which progress is being tracked. |
| `score` | INTEGER | NOT NULL | The highest score achieved on the quiz for this topic. |
| `last_attempted` | DATETIME | NOT NULL | The date and time of the last attempt. |
| `completed` | BOOLEAN | NOT NULL, DEFAULT 0 | Whether the topic has been successfully completed. |
