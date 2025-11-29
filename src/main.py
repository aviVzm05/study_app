from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget, QMessageBox
from ui.grade_selection_view import GradeSelectionView
from ui.topic_selection_view import TopicSelectionView
from ui.math_lesson_view import MathLessonView
from ui.english_exercise_view import EnglishExerciseView
from models.schema import create_schema
from services.data_seeder import seed_initial_data
from services.logging_service import setup_logging, log_event
from services.data_service import DataService
from models.models import Lesson
import sys

class KidsLearningApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kids Learning App")
        self.setGeometry(100, 100, 600, 400)
        # self.math_service = MathService() # Removed
        # self.english_service = EnglishService() # Removed
        self.current_student_id = None # To store the ID of the current student
        self.init_db_and_data()
        self._ensure_default_student() # Ensure a default student exists
        self.init_ui()

    def _ensure_default_student(self):
        """Ensures a default student profile exists, creating one if necessary."""
        # For simplicity, we'll use student ID 1 as the default.
        # In a real app, this would involve proper user management.
        student = DataService.get_student_profile(1)
        if not student:
            student = DataService.create_student_profile(nickname="GuestKid")
            log_event('info', f"Created default student: {student.nickname} (ID: {student.id})")
        else:
            log_event('info', f"Using existing default student: {student.nickname} (ID: {student.id})")
        self.current_student_id = student.id


    def init_db_and_data(self):
        try:
            create_schema()
            seed_initial_data()
            log_event('info', "Database initialized and seeded successfully.")
        except Exception as e:
            log_event('critical', f"Failed to initialize or seed database: {e}")
            QMessageBox.critical(self, "Database Error", f"Failed to initialize or seed database: {e}")
            sys.exit(1)

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        self.grade_selection_view = GradeSelectionView()
        self.topic_selection_view = TopicSelectionView()
        self.math_lesson_view = MathLessonView()
        self.english_exercise_view = EnglishExerciseView() # Initialize English exercise view

        self.stacked_widget.addWidget(self.grade_selection_view)
        self.stacked_widget.addWidget(self.topic_selection_view)
        self.stacked_widget.addWidget(self.math_lesson_view)
        self.stacked_widget.addWidget(self.english_exercise_view) # Add English view

        # Connect signals
        self.grade_selection_view.select_button.clicked.connect(self.show_topic_selection)
        self.topic_selection_view.start_button.clicked.connect(self.start_learning_session)
        self.topic_selection_view.back_button.clicked.connect(self.show_grade_selection) # Back from topics to grade
        self.math_lesson_view.back_button.clicked.connect(self.show_topic_selection) # Back from math lesson to topics
        self.english_exercise_view.back_button.clicked.connect(self.show_topic_selection) # Back from english exercise to topics

        self.show_grade_selection()

    def show_grade_selection(self):
        self.stacked_widget.setCurrentWidget(self.grade_selection_view)

    def show_topic_selection(self):
        selected_grade = int(self.grade_selection_view.grade_combo.currentText())
        self.topic_selection_view.set_grade(selected_grade)
        self.stacked_widget.setCurrentWidget(self.topic_selection_view)

    def start_learning_session(self):
        selected_topic_id = self.topic_selection_view.get_selected_topic_id()
        if not selected_topic_id:
            QMessageBox.warning(self, "Selection Error", "Please select a topic before starting.")
            return

        try:
            from models.models import Topic, Subject
            selected_topic = Topic.find_by_id(selected_topic_id)
            if not selected_topic:
                QMessageBox.warning(self, "Selection Error", "Selected topic not found in database.")
                return
            
            subject = Subject.find_by_id(selected_topic.subject_id)
            if not subject:
                QMessageBox.warning(self, "Selection Error", "Subject for selected topic not found.")
                return

            if subject.name == "Mathematics":
                lesson = Lesson.find_by_id(selected_topic_id) # Need to fetch lesson data
                if not lesson:
                    QMessageBox.warning(self, "Lesson Error", "Lesson for selected topic not found.")
                    return
                self.math_lesson_view.set_lesson_data(lesson)
                self.math_lesson_view.student_id = self.current_student_id # Pass student ID to the view
                self.stacked_widget.setCurrentWidget(self.math_lesson_view)
            elif subject.name == "English":
                # For English, use the new LLM-based approach
                # lesson, questions = self.english_service.get_lesson_and_questions_for_topic(selected_topic_id) # Removed
                
                # We only need to set the lesson data in the view.
                # The view itself will handle loading questions dynamically using LLMService.
                # We also pass the student_id to the view for performance tracking.
                lesson = Lesson.find_by_id(selected_topic_id) # Need to fetch lesson data
                if not lesson:
                    QMessageBox.warning(self, "Lesson Error", "Lesson for selected topic not found.")
                    return

                self.english_exercise_view.set_lesson_data(lesson)
                self.english_exercise_view.student_id = self.current_student_id # Pass student ID to the view
                self.stacked_widget.setCurrentWidget(self.english_exercise_view)
            else:
                QMessageBox.warning(self, "Selection Error", "Unsupported subject type for learning session.")
        except Exception as e:
            log_event('critical', f"An unexpected error occurred in start_learning_session: {e}")
            QMessageBox.critical(self, "Application Error", f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    setup_logging()
    log_event('info', "Kids Learning App started.")
    app = QApplication(sys.argv)
    window = KidsLearningApp()
    window.show()
    sys.exit(app.exec())