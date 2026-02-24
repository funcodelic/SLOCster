from PyQt6.QtWidgets import QPlainTextEdit

class ContentPane(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: black; color: white;")
        self.setPlainText("Content area")