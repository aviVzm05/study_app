import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

class KidsLearningApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kids Learning App")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Welcome to Kids Learning App!")
        layout.addWidget(label)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KidsLearningApp()
    window.show()
    sys.exit(app.exec())