from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox, QRadioButton, QButtonGroup
import logging
from services.llm_service import LLMService # Import LLMService

logger = logging.getLogger(__name__)

class MathLessonView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.lesson_data = None
        self.llm_questions_data = [] # Store dynamically generated questions
        self.current_question_index = 0
        self.current_difficulty_band = "Beginner" # Default difficulty, can be dynamic
        self.score = 0 # Initialize score
        self.total_questions = 0 # Initialize total questions
        self.selected_answer = None # To store the selected radio button answer
        self.options_button_group = QButtonGroup(self) # Group for radio buttons
        self.options_button_group.buttonClicked.connect(self._on_option_selected)
        self.init_ui()

    def init_ui(self):


        self.lesson_content_display = QTextEdit()
        self.lesson_content_display.setReadOnly(True)
        self.layout.addWidget(self.lesson_content_display)

        self.start_quiz_button = QPushButton("Start Dynamic Math Quiz")
        self.start_quiz_button.clicked.connect(self.start_practice)
        self.layout.addWidget(self.start_quiz_button)

        self.back_button = QPushButton("Back to Topics")
        self.back_button.setObjectName("BackButton")
        self.layout.addWidget(self.back_button)

        # Question section (hidden initially)
        self.question_widget = QWidget()
        self.question_layout = QVBoxLayout()
        self.question_widget.setLayout(self.question_layout)

        self.question_prompt_label = QLabel("Question Prompt")
        self.question_layout.addWidget(self.question_prompt_label)

        # Container for multiple choice options (Radio Buttons)
        self.options_container_widget = QWidget() # New container for radio buttons
        self.options_container_layout = QVBoxLayout()
        self.options_container_widget.setLayout(self.options_container_layout)
        self.question_layout.addWidget(self.options_container_widget) # Add this container to the question layout

        self.options_widget = QWidget() # Widget that will hold the radio buttons
        self.options_layout = QVBoxLayout()
        self.options_widget.setLayout(self.options_layout)
        self.options_container_layout.addWidget(self.options_widget) # Add options_widget to its container

        # Text input for free-form answers
        self.answer_input = QTextEdit()
        self.answer_input.setPlaceholderText("Enter your answer here...")
        self.question_layout.addWidget(self.answer_input)
        self.answer_input.hide() # Hide by default

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

    def _clear_options(self):
        """Clears all radio buttons from the options layout."""
        while self.options_layout.count():
            button = self.options_layout.takeAt(0).widget()
            self.options_button_group.removeButton(button)
            button.deleteLater()
        self.selected_answer = None # Reset selected answer when clearing radio buttons

    def _on_option_selected(self, button):
        """Stores the text of the selected radio button."""
        self.selected_answer = button.text()

    def set_lesson_data(self, lesson): # Modified to only take lesson data
        self.lesson_data = lesson
        self.llm_questions_data = []
        self.current_question_index = 0
        self.score = 0 # Reset score for new lesson
        self.total_questions = 0 # Reset total questions for new lesson
        self.show_lesson()

    def show_lesson(self):
        if self.lesson_data:
            self.lesson_content_display.setText(self.lesson_data.content)
            self.start_quiz_button.show()
            self.question_widget.hide()
            self.feedback_label.setText("")
            self._clear_options() # Clear options when showing lesson
            self.next_question_button.hide()
        else:
            self.lesson_content_display.setText("Please select a topic.")
            self.start_quiz_button.hide()

    def start_practice(self):
        self.start_quiz_button.hide()
        self.question_widget.show()
        self.score = 0
        self.total_questions = 0
        self.llm_questions_data = [] # Clear previous questions
        self.current_question_index = 0
        self.answer_input.clear() # Clear text input for new exercise
        self._load_llm_question() # Call method to load question from LLM

    def _load_llm_question(self):
        """Loads new questions from the LLMService."""
        try:
            topic = self.lesson_data.title if self.lesson_data else "General Math" # Get topic from lesson_data
            logger.info(f"Loading 20 new Math questions on topic '{topic}' (Difficulty: {self.current_difficulty_band})...")
            
            # Refined prompt for LLMService
            llm_prompt_context = {
                "user_level": self.current_difficulty_band,
                "topic": topic,
                "num_options": 4, # Explicitly request 4 options for multiple-choice questions
                "additional_instructions": "Generate clear, concise, and educational multiple-choice questions with exactly {num_options} possible answers. Ensure questions are not ambiguous and have a single correct answer. Avoid questions that require subjective interpretation."
            }

            questions = LLMService.generate_question(
                subject="Math", 
                difficulty_band=self.current_difficulty_band, 
                num_questions=20, # Request 20 questions
                context_history=llm_prompt_context # Pass the refined prompt context
            )
            if questions:
                self.llm_questions_data.extend(questions)
                self.display_current_question()
            else:
                QMessageBox.warning(self, "LLM Error", "Could not generate questions from LLM. Please try again.")
                self.question_widget.hide()
                self.start_quiz_button.show()
        except Exception as e:
            logger.error(f"Error loading LLM question: {e}")
            QMessageBox.critical(self, "LLM Error", f"Failed to load question: {e}. Please check your API key and network connection.")
            self.question_widget.hide()
            self.start_quiz_button.show()

    def display_current_question(self):
        self._clear_options() # Clear previous options
        self.selected_answer = None # Reset selected answer for radio buttons
        self.answer_input.clear() # Clear the text input field

        if self.current_question_index < len(self.llm_questions_data):
            question = self.llm_questions_data[self.current_question_index]
            self.question_prompt_label.setText(f"Question {self.current_question_index + 1}/{len(self.llm_questions_data)}: {question.get('question_text', 'No question text.')}")
            
            possible_answers = question.get("possible_answers", [])
            
            if possible_answers:
                self.options_container_widget.show() # Show radio button container
                self.answer_input.hide()            # Hide text input
                for i, option_text in enumerate(possible_answers):
                    radio_button = QRadioButton(option_text)
                    self.options_layout.addWidget(radio_button)
                    self.options_button_group.addButton(radio_button)
            else:
                self.options_container_widget.hide() # Hide radio button container
                self.answer_input.show()             # Show text input
            
            self.feedback_label.setText("")
            self.submit_answer_button.setEnabled(True) # Enable submit button
            self.next_question_button.hide()
        else:
            self._finish_quiz()

    def submit_answer(self):
        user_answer = ""
        if self.options_container_widget.isVisible(): # If radio buttons are visible
            if not self.selected_answer:
                QMessageBox.warning(self, "No Answer Selected", "Please select an answer before submitting.")
                return
            user_answer = self.selected_answer
        elif self.answer_input.isVisible(): # If text input is visible
            user_answer = self.answer_input.toPlainText().strip()
            if not user_answer:
                QMessageBox.warning(self, "No Answer Entered", "Please enter your answer before submitting.")
                return
        else: # Should not happen, but as a safeguard
            QMessageBox.warning(self, "No Input Method", "No answer input method is available.")
            return

        current_question = self.llm_questions_data[self.current_question_index]
        correct_answer = current_question.get("correct_answer", "").strip()
        explanation = current_question.get("explanation", "No explanation provided.")

        self.total_questions += 1
        # Case-insensitive comparison for text input and radio button answers
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            self.feedback_label.setText(f"<font color='green'>Correct! </font> Explanation: {explanation}")
        else:
            self.feedback_label.setText(f"<font color='red'>Incorrect. </font> The correct answer was: {correct_answer}. Explanation: {explanation}")
        
        self.submit_answer_button.setEnabled(False) # Disable submit button after answer
        self.next_question_button.show()
    
    def display_next_question(self):
        self.current_question_index += 1
        if self.current_question_index < len(self.llm_questions_data):
            self.display_current_question()
        else:
            self._finish_quiz()

    def _finish_quiz(self):
        """Reports the score and closes the exercise widget."""
        QMessageBox.information(self, "Quiz Complete", 
                                f"You have completed the Math quiz!\nYour score: {self.score}/{self.total_questions}")
        self.question_widget.hide()
        self.start_quiz_button.show()
        # Emit a signal or call a method on the parent to go back to main topic selection
        # For now, just hide the exercise, the parent can decide what to do.
