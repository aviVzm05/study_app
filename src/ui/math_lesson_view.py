from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt
import json
from services.math_validation import MathValidationService

class MathLessonView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.lesson_data = None
        self.questions_data = []
        self.current_question_index = 0
        self.init_ui()

    def init_ui(self):
        self.lesson_title_label = QLabel("Lesson Title")
        self.lesson_title_label.setObjectName("LessonTitleLabel")
        self.layout.addWidget(self.lesson_title_label)

        self.lesson_content_display = QTextEdit()
        self.lesson_content_display.setReadOnly(True)
        self.layout.addWidget(self.lesson_content_display)

        self.start_quiz_button = QPushButton("Start Practice")
        self.start_quiz_button.clicked.connect(self.start_practice)
        self.layout.addWidget(self.start_quiz_button)

        # Question section (hidden initially)
        self.question_widget = QWidget()
        self.question_layout = QVBoxLayout()
        self.question_widget.setLayout(self.question_layout)

        self.question_prompt_label = QLabel("Question Prompt")
        self.question_layout.addWidget(self.question_prompt_label)

        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Enter your answer")
        self.question_layout.addWidget(self.answer_input)

        self.submit_answer_button = QPushButton("Submit Answer")
        self.submit_answer_button.clicked.connect(self.submit_answer)
        self.question_layout.addWidget(self.submit_answer_button)
        
        self.feedback_label = QLabel("")
        self.feedback_label.setObjectName("FeedbackLabel")
        self.question_layout.addWidget(self.feedback_label)

        self.next_question_button = QPushButton("Next Question")
        self.next_question_button.clicked.connect(self.display_next_question)
        self.next_question_button.hide() # Hide until answer is submitted
        self.question_layout.addWidget(self.next_question_button)

        self.question_widget.hide() # Hide question widget initially
        self.layout.addWidget(self.question_widget)

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
            self.start_quiz_button.show()
            self.question_widget.hide()
            self.feedback_label.setText("")
            self.answer_input.clear()
            self.next_question_button.hide()
        else:
            self.lesson_title_label.setText("No Lesson Available")
            self.lesson_content_display.setText("Please select a topic.")
            self.start_quiz_button.hide()

    def start_practice(self):
        if self.questions_data:
            self.start_quiz_button.hide()
            self.question_widget.show()
            self.display_current_question()
        else:
            QMessageBox.information(self, "No Questions", "No practice questions available for this topic.")

    def display_current_question(self):
        if self.current_question_index < len(self.questions_data):
            question = self.questions_data[self.current_question_index]
            self.question_prompt_label.setText(question.prompt)
            self.answer_input.clear()
            self.feedback_label.setText("")
            self.submit_answer_button.show()
            self.next_question_button.hide()
            
            # Display options for multiple choice
            if question.question_type == "multiple_choice" and question.options:
                options = json.loads(question.options)
                options_str = "\n".join([f"- {opt}" for opt in options])
                self.question_prompt_label.setText(f"{question.prompt}\n\nOptions:\n{options_str}")

        else:
            QMessageBox.information(self, "Practice Complete", "You have completed all practice questions!")
            self.question_widget.hide()
            self.start_quiz_button.show() # Option to restart or go back

    def submit_answer(self):
        user_answer = self.answer_input.text().strip()
        current_question = self.questions_data[self.current_question_index]
        
        validator = MathValidationService()
        is_correct = validator.validate_answer(current_question.question_type, user_answer, current_question.correct_answer)
        feedback_text = validator.get_feedback(is_correct, current_question.correct_answer)
        self.feedback_label.setText(feedback_text)
        
        self.submit_answer_button.hide()
        self.next_question_button.show()

    def display_next_question(self):
        self.current_question_index += 1
        self.display_current_question()
