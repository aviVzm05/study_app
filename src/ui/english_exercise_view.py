from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt
import json
from services.english_validation import EnglishValidationService

class EnglishExerciseView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.lesson_data = None
        self.questions_data = []
        self.current_question_index = 0
        self.init_ui()

    def init_ui(self):
        self.lesson_title_label = QLabel("English Lesson")
        self.lesson_title_label.setObjectName("LessonTitleLabel")
        self.layout.addWidget(self.lesson_title_label)

        self.lesson_content_display = QTextEdit()
        self.lesson_content_display.setReadOnly(True)
        self.layout.addWidget(self.lesson_content_display)

        self.start_exercise_button = QPushButton("Start Writing Exercise")
        self.start_exercise_button.clicked.connect(self.start_exercise)
        self.layout.addWidget(self.start_exercise_button)

        # Exercise section (hidden initially)
        self.exercise_widget = QWidget()
        self.exercise_layout = QVBoxLayout()
        self.exercise_widget.setLayout(self.exercise_layout)

        self.prompt_label = QLabel("Writing Prompt")
        self.exercise_layout.addWidget(self.prompt_label)

        self.user_input_text = QTextEdit()
        self.user_input_text.setPlaceholderText("Write your sentence here...")
        self.exercise_layout.addWidget(self.user_input_text)

        self.submit_sentence_button = QPushButton("Submit Sentence")
        self.submit_sentence_button.clicked.connect(self.submit_sentence)
        self.exercise_layout.addWidget(self.submit_sentence_button)
        
        self.feedback_label = QLabel("")
        self.feedback_label.setObjectName("FeedbackLabel")
        self.exercise_layout.addWidget(self.feedback_label)

        self.next_exercise_button = QPushButton("Next Exercise")
        self.next_exercise_button.clicked.connect(self.display_next_exercise)
        self.next_exercise_button.hide()
        self.exercise_layout.addWidget(self.next_exercise_button)

        self.exercise_widget.hide()
        self.layout.addWidget(self.exercise_widget)

        self.layout.addStretch()

    def set_lesson_data(self, lesson, questions):
        self.lesson_data = lesson
        self.questions_data = questions
        self.current_question_index = 0
        self.show_lesson()

    def show_lesson(self):
        if self.lesson_data:
            self.lesson_title_label.setText(self.lesson_data.title)
            self.lesson_content_display.setText(self.lesson_data.content)
            self.start_exercise_button.show()
            self.exercise_widget.hide()
            self.feedback_label.setText("")
            self.user_input_text.clear()
            self.next_exercise_button.hide()
        else:
            self.lesson_title_label.setText("No Lesson Available")
            self.lesson_content_display.setText("Please select a topic.")
            self.start_exercise_button.hide()

    def start_exercise(self):
        if self.questions_data:
            self.start_exercise_button.hide()
            self.exercise_widget.show()
            self.display_current_exercise()
        else:
            QMessageBox.information(self, "No Exercises", "No writing exercises available for this topic.")

    def display_current_exercise(self):
        if self.current_question_index < len(self.questions_data):
            question = self.questions_data[self.current_question_index]
            self.prompt_label.setText(question.prompt)
            self.user_input_text.clear()
            self.feedback_label.setText("")
            self.submit_sentence_button.show()
            self.next_exercise_button.hide()
        else:
            QMessageBox.information(self, "Exercise Complete", "You have completed all writing exercises!")
            self.exercise_widget.hide()
            self.start_exercise_button.show()

    def submit_sentence(self):
        user_sentence = self.user_input_text.toPlainText().strip()
        current_question = self.questions_data[self.current_question_index]
        
        validator = EnglishValidationService()
        is_correct, feedback, corrected_sentence = validator.validate_sentence(user_sentence)
        
        if is_correct:
            self.feedback_label.setText("<font color='green'>Correct!</font>")
        else:
            feedback_str = "<br>".join(feedback)
            self.feedback_label.setText(f"<font color='red'>Issues found:</font><br>{feedback_str}<br>Corrected: {corrected_sentence}")
        
        self.submit_sentence_button.hide()
        self.next_exercise_button.show()

    def display_next_exercise(self):
        self.current_question_index += 1
        self.display_current_exercise()