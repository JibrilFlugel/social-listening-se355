from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal
import sys
from run_crewai import run_crewai  

class WorkerThread(QThread):
    result_signal = pyqtSignal(str)

    def __init__(self, topic):
        super().__init__()
        self.topic = topic

    def run(self):
        result = run_crewai(self.topic)
        self.result_signal.emit(result)

class SocialListeningApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter the name of the topic you want to research:...")
        layout.addWidget(self.input_field)

        self.search_button = QPushButton("Search", self)
        self.search_button.clicked.connect(self.start_search)
        layout.addWidget(self.search_button)

        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)

        self.setLayout(layout)
        self.setWindowTitle("Social Listening")
        self.setGeometry(100, 100, 400, 300)

    def start_search(self):
        topic = self.input_field.text().strip()
        if not topic:
            self.result_area.setText("Topic can't be empty!")
            return

        self.result_area.setText("Processing...\n")
        self.worker = WorkerThread(topic)
        self.worker.result_signal.connect(self.display_result)
        self.worker.start()

    def display_result(self, result):
        self.result_area.append(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SocialListeningApp()
    ex.show()
    sys.exit(app.exec_())
