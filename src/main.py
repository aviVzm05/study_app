import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QStackedWidget
from ui.grade_selection_view import GradeSelectionView
from ui.topic_selection_view import TopicSelectionView
from ui.math_lesson_view import MathLessonView
from models.schema import create_schema
from services.data_seeder import seed_initial_data
from services.math_service import MathService

class KidsLearningApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kids Learning App")
        self.setGeometry(100, 100, 800, 600)
        self.math_service = MathService()
        self.init_db_and_data()
        self.init_ui()

    def init_db_and_data(self):
        create_schema()
        seed_initial_data()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        self.grade_selection_view = GradeSelectionView()
        self.topic_selection_view = TopicSelectionView()
        self.math_lesson_view = MathLessonView()

        self.stacked_widget.addWidget(self.grade_selection_view)
        self.stacked_widget.addWidget(self.topic_selection_view)
        self.stacked_widget.addWidget(self.math_lesson_view)

        # Connect signals
        self.grade_selection_view.select_button.clicked.connect(self.show_topic_selection)
        self.topic_selection_view.start_button.clicked.connect(self.show_math_lesson)

        self.show_grade_selection()

    def show_grade_selection(self):
        self.stacked_widget.setCurrentWidget(self.grade_selection_view)

    def show_topic_selection(self):
        selected_grade = int(self.grade_selection_view.grade_combo.currentText())
        self.topic_selection_view.set_grade(selected_grade)
        self.stacked_widget.setCurrentWidget(self.topic_selection_view)

    def show_math_lesson(self):
        selected_topic_id = self.topic_selection_view.get_selected_topic_id()
        if selected_topic_id:
            lesson, questions = self.math_service.get_lesson_and_questions_for_topic(selected_topic_id)
            self.math_lesson_view.set_lesson_data(lesson, questions)
            self.stacked_widget.setCurrentWidget(self.math_lesson_view)
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a topic before starting.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KidsLearningApp()
    window.show()
    sys.exit(app.exec())