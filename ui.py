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
        self.input_field.setPlaceholderText("Nhập chủ đề cần tìm kiếm...")
        layout.addWidget(self.input_field)

        self.search_button = QPushButton("Tìm kiếm", self)
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
            self.result_area.setText("❌ Chủ đề không được để trống!")
            return

        self.result_area.setText("⏳ Đang xử lý dữ liệu...\n")
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
