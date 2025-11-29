from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
from models.models import Subject, Topic

class TopicSelectionView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.grade = 5 # Default or set dynamically
        self.init_ui()
        self.load_subjects()

    def init_ui(self):
        title_label = QLabel("Select Subject and Topic")
        title_label.setObjectName("TitleLabel")
        self.layout.addWidget(title_label)

        # Subject Selection
        subject_layout = QHBoxLayout()
        self.subject_label = QLabel("Subject:")
        self.subject_combo = QComboBox()
        self.subject_combo.currentIndexChanged.connect(self.load_topics)
        subject_layout.addWidget(self.subject_label)
        subject_layout.addWidget(self.subject_combo)
        self.layout.addLayout(subject_layout)

        # Topic Selection
        topic_layout = QHBoxLayout()
        self.topic_label = QLabel("Topic:")
        self.topic_combo = QComboBox()
        topic_layout.addWidget(self.topic_label)
        topic_layout.addWidget(self.topic_combo)
        self.layout.addLayout(topic_layout)

        self.start_button = QPushButton("Start Learning")
        self.start_button.setObjectName("StartButton")
        self.layout.addWidget(self.start_button)

        self.back_button = QPushButton("Back")
        self.back_button.setObjectName("BackButton")
        self.layout.addWidget(self.back_button)

        self.layout.addStretch()



    def load_subjects(self):
        self.subject_combo.clear()
        subjects = Subject.find_all()
        for subject in subjects:
            self.subject_combo.addItem(subject.name, subject.id)
        self.load_topics() # Load topics for the first subject

    def load_topics(self):
        self.topic_combo.clear()
        selected_subject_id = self.subject_combo.currentData()
        if selected_subject_id:
            # Assuming one topic per subject per grade for MVP
            # In a real app, this would query topics for the selected_subject_id AND self.grade
            topics = [t for t in Topic.find_all() if t.subject_id == selected_subject_id and t.grade == self.grade]
            for topic in topics:
                self.topic_combo.addItem(topic.name, topic.id)

    def set_grade(self, grade):
        self.grade = grade
        self.load_topics()

    def get_selected_topic_id(self):
        return self.topic_combo.currentData()
