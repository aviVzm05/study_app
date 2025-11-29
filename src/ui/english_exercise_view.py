from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt
import json
import logging
from services.llm_service import LLMService # Import LLMService

logger = logging.getLogger(__name__)

class EnglishExerciseView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.lesson_data = None
        self.llm_questions_data = [] # Store dynamically generated questions
        self.current_question_index = 0
        self.current_difficulty_band = "Beginner" # Default difficulty
        self.init_ui()

    def init_ui(self):
        self.lesson_title_label = QLabel("English Lesson")
        self.lesson_title_label.setObjectName("LessonTitleLabel")
        self.layout.addWidget(self.lesson_title_label)

        self.lesson_content_display = QTextEdit()
        self.lesson_content_display.setReadOnly(True)
        self.layout.addWidget(self.lesson_content_display)

        self.start_exercise_button = QPushButton("Start Dynamic English Quiz") # Updated button text
        self.start_exercise_button.clicked.connect(self.start_exercise)
        self.layout.addWidget(self.start_exercise_button)

        self.back_button = QPushButton("Back to Topics")
        self.back_button.setObjectName("BackButton")
        self.layout.addWidget(self.back_button)

        # Exercise section
        self.exercise_widget = QWidget()
        self.exercise_layout = QVBoxLayout()
        self.exercise_widget.setLayout(self.exercise_layout)

        self.question_text_label = QLabel("Question:") # Label for dynamic question text
        self.exercise_layout.addWidget(self.question_text_label)

        self.user_answer_input = QLineEdit() # For shorter answers (multiple choice, single word)
        self.user_answer_input.setPlaceholderText("Type your answer here...")
        self.exercise_layout.addWidget(self.user_answer_input)

        self.submit_answer_button = QPushButton("Submit Answer")
        self.submit_answer_button.clicked.connect(self.submit_answer)
        self.exercise_layout.addWidget(self.submit_answer_button)
        
        self.feedback_label = QLabel("")
        self.feedback_label.setObjectName("FeedbackLabel")
        self.exercise_layout.addWidget(self.feedback_label)

        self.next_question_button = QPushButton("Next Question")
        self.next_question_button.clicked.connect(self.display_next_question)
        self.next_question_button.hide()
        self.exercise_layout.addWidget(self.next_question_button)

        self.exercise_widget.hide()
        self.layout.addWidget(self.exercise_widget)

        self.layout.addStretch()

    def set_lesson_data(self, lesson): # Modified to only take lesson data
        self.lesson_data = lesson
        self.llm_questions_data = []
        self.current_question_index = 0
        self.show_lesson()

    def show_lesson(self):
        if self.lesson_data:
            self.lesson_title_label.setText(self.lesson_data.title)
            self.lesson_content_display.setText(self.lesson_data.content)
            self.start_exercise_button.show()
            self.exercise_widget.hide()
            self.feedback_label.setText("")
            self.user_answer_input.clear()
            self.next_question_button.hide()
        else:
            self.lesson_title_label.setText("No Lesson Available")
            self.lesson_content_display.setText("Please select a topic.")
            self.start_exercise_button.hide()

    def start_exercise(self):
        self.start_exercise_button.hide()
        self.exercise_widget.show()
        self._load_llm_question() # Call method to load question from LLM

    def _load_llm_question(self):
        """Loads a new question from the LLMService."""
        try:
            # Assuming subject is English, and difficulty is from self.current_difficulty_band
            # In a real app, context_history would be passed from a student's profile
            logger.info(f"Loading new English question (Difficulty: {self.current_difficulty_band})...")
            questions = LLMService.generate_question(
                subject="English", 
                difficulty_band=self.current_difficulty_band, 
                num_questions=1, 
                context_history=None # To be implemented later with actual history
            )
            if questions:
                self.llm_questions_data.extend(questions)
                self.display_current_question()
            else:
                QMessageBox.warning(self, "LLM Error", "Could not generate questions from LLM. Please try again.")
                self.exercise_widget.hide()
                self.start_exercise_button.show()
        except Exception as e:
            logger.error(f"Error loading LLM question: {e}")
            QMessageBox.critical(self, "LLM Error", f"Failed to load question: {e}. Please check your API key and network connection.")
            self.exercise_widget.hide()
            self.start_exercise_button.show()

    def display_current_question(self):
        if self.current_question_index < len(self.llm_questions_data):
            question = self.llm_questions_data[self.current_question_index]
            self.question_text_label.setText(question.get("question_text", "No question text."))
            self.user_answer_input.clear()
            self.feedback_label.setText("")
            self.submit_answer_button.show()
            self.next_question_button.hide()
        else:
            QMessageBox.information(self, "Quiz Complete", "You have completed all questions for this session!")
            self.exercise_widget.hide()
            self.start_exercise_button.show()

    def submit_answer(self):
        user_answer = self.user_answer_input.text().strip()
        current_question = self.llm_questions_data[self.current_question_index]
        
        # Display explanation from LLM response directly (T011, T012)
        explanation = current_question.get("explanation", "No explanation provided.")
        correct_answer = current_question.get("correct_answer", "N/A")

        if user_answer.lower() == correct_answer.lower():
            self.feedback_label.setText(f"<font color='green'>Correct! </font> Explanation: {explanation}")
        else:
            self.feedback_label.setText(f"<font color='red'>Incorrect. </font> The correct answer was: {correct_answer}. Explanation: {explanation}")
        
        self.submit_answer_button.hide()
        self.next_question_button.show()

    def display_next_question(self): # Renamed from display_next_exercise
        self.current_question_index += 1
        if self.current_question_index < len(self.llm_questions_data):
            self.display_current_question()
        else:
            # If no more questions in current batch, load another one
            self._load_llm_question()