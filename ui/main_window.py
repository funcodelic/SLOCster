import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QListWidget, QTextEdit,
    QSplitter, QMenuBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QFileDialog
from ui.app_toolbar import AppToolBar

from PyQt6.QtWidgets import QTreeView
from PyQt6.QtGui import QFileSystemModel

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QPlainTextEdit
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SLOCster")
        self.setFixedSize(1400, 800)

        self._createMenuBar()
        self._createToolbar()
        self._createCentralUI()

    def _createMenuBar(self):
        file_menu = self.menuBar().addMenu("File")

        self.openDirAction = QAction("Open Directory", self)
        self.openDirAction.triggered.connect(self.open_directory)

        file_menu.addAction(self.openDirAction)

    def _createToolbar(self):
        self.toolbar = AppToolBar(self)
        self.addToolBar(self.toolbar)

    def handle_directory(self, path):
        print(path)
        self.directoryPane.set_directory(path)

    def open_directory(self):
        path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if path:
            self.handle_directory(path)

    def _createCentralUI(self):
        central_widget = QWidget()
        layout = QHBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        splitter = self._createSplitter()
        layout.addWidget(splitter)

    def _createSplitter(self):
        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.directoryPane = self.DirectoryPane()
        self.contentPane = self.ContentPane()

        self.directoryPane.fileSelected.connect(self.load_file_into_content)

        splitter.addWidget(self.directoryPane)
        splitter.addWidget(self.contentPane)

        splitter.setSizes([280, 1120])  # 1:4 ratio

        return splitter

    def load_file_into_content(self, file_path: str):
        _, ext = os.path.splitext(file_path)
        allowed = {".py", ".swift", ".txt", ".md", ".json"}  # tweak as you like
        if ext.lower() not in allowed:
            self.contentPane.setPlainText(f"(Not a text file I’m showing yet)\n{file_path}")
            return

        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                self.contentPane.setPlainText(f.read())
        except Exception as e:
            self.contentPane.setPlainText(f"Error reading file:\n{file_path}\n\n{e}")

    class DirectoryPane(QTreeView):
        fileSelected = pyqtSignal(str) # new

        def __init__(self):
            super().__init__()
            self.model = QFileSystemModel()
            self.model.setRootPath("")
            self.setModel(self.model)

            self.setHeaderHidden(False)

            for col in range(1, self.model.columnCount()):
                self.hideColumn(col)

            self.setRootIsDecorated(True)  # keep expand arrows
            self.setAlternatingRowColors(False)
            self.setSortingEnabled(False)

            self.clicked.connect(self.handle_click)

        def set_directory(self, path):
            self.setRootIndex(self.model.index(path))

        def handle_click(self, index):
            path = self.model.filePath(index)
            print(path)
            if self.model.isDir(index):
                return
            self.fileSelected.emit(path)

    class ContentPane(QPlainTextEdit):
        def __init__(self):
            super().__init__()
            self.setStyleSheet("background-color: black; color: white;")
            self.setPlainText("Content area")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())