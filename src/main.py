from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QStackedWidget, QMessageBox
from ui.grade_selection_view import GradeSelectionView
from ui.topic_selection_view import TopicSelectionView
from ui.math_lesson_view import MathLessonView
from ui.english_exercise_view import EnglishExerciseView
from models.schema import create_schema
from services.data_seeder import seed_initial_data
from services.math_service import MathService
from services.english_service import EnglishService
from services.logging_service import setup_logging, log_event
import sys

class KidsLearningApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kids Learning App")
        self.setGeometry(100, 100, 800, 600)
        self.math_service = MathService()
        self.english_service = EnglishService() # Initialize English service
        self.init_db_and_data()
        self.init_ui()

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
                lesson, questions = self.math_service.get_lesson_and_questions_for_topic(selected_topic_id)
                self.math_lesson_view.set_lesson_data(lesson, questions)
                self.stacked_widget.setCurrentWidget(self.math_lesson_view)
            elif subject.name == "English":
                lesson, questions = self.english_service.get_lesson_and_questions_for_topic(selected_topic_id)
                self.english_exercise_view.set_lesson_data(lesson, questions)
                self.stacked_widget.setCurrentWidget(self.english_exercise_view)
            else:
                QMessageBox.warning(self, "Selection Error", "Unsupported subject type for learning session.")
        except Exception as e:
            QMessageBox.critical(self, "Application Error", f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    setup_logging()
    log_event('info', "Kids Learning App started.")
    app = QApplication(sys.argv)
    window = KidsLearningApp()
    window.show()
    sys.exit(app.exec())