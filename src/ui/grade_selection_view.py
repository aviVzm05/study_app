from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton

class GradeSelectionView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.init_ui()

    def init_ui(self):
        title_label = QLabel("Select Your Grade")
        title_label.setObjectName("TitleLabel") # For styling
        self.layout.addWidget(title_label)

        grade_layout = QHBoxLayout()
        self.grade_label = QLabel("Grade:")
        self.grade_combo = QComboBox()
        self.grade_combo.addItems([str(5)]) # Only 5th grade available
        grade_layout.addWidget(self.grade_label)
        grade_layout.addWidget(self.grade_combo)
        self.layout.addLayout(grade_layout)

        self.select_button = QPushButton("Continue")
        self.select_button.setObjectName("SelectButton") # For styling
        self.layout.addWidget(self.select_button)

        self.layout.addStretch() # Pushes content to the top


