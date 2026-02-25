import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QSplitter
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QFileDialog
from ui.app_toolbar import AppToolBar
from ui.directory_pane import DirectoryPane
from ui.content_pane import ContentPane
from core.sloc_analyzer import SlocAnalyzer
import tempfile
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SLOCster")
        self.setFixedSize(1400, 800)

        # Create the components
        self._createMenuBar()
        self._createToolbar()
        self._createCentralUI()
        self.slocAnalyzer = SlocAnalyzer()

    # Create the menu bar
    def _createMenuBar(self):
        file_menu = self.menuBar().addMenu("File")

        self.openDirAction = QAction("Open Directory", self)
        self.openDirAction.triggered.connect(self.open_directory)

        file_menu.addAction(self.openDirAction)

    # Create the toolbar
    def _createToolbar(self):
        self.toolbar = AppToolBar(self)
        self.addToolBar(self.toolbar)

    # Handle directory selection
    def handle_directory(self, path):
        print(path)
        self.directoryPane.set_directory(path)

    # Open directory (from File)
    def open_directory(self):
        print("in open_directory")
        path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if path:
            self.handle_directory(path)
            total = self.slocAnalyzer.analyze_directory(path)
            self.toolbar.set_total_sloc(total)  # or create set_directory_sloc()

    # Create center UI (split view holding directory and content panes)
    def _createCentralUI(self):
        central_widget = QWidget()
        layout = QHBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        splitter = self._createSplitter()
        layout.addWidget(splitter)

    # Create splitter (and make connections
    def _createSplitter(self):
        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.directoryPane = DirectoryPane()
        self.contentPane = ContentPane()

        # Key connection - Selected file from directory pane is loaded and processed
        self.directoryPane.fileSelected.connect(self.load_file_into_content)

        splitter.addWidget(self.directoryPane)
        splitter.addWidget(self.contentPane)

        splitter.setSizes([280, 1120])  # 1:4 ratio

        return splitter

    # Load the file to be processed
    def load_file_into_content(self, file_path: str):
        try:
            analysis, sloc_count = self.slocAnalyzer.analyze_file(file_path)

            formatted_text = self.contentPane.build_formatted_text(analysis)

            with tempfile.NamedTemporaryFile(
                    mode="w", delete=False, suffix=".txt"
            ) as tmp:
                tmp.write(formatted_text)
                temp_path = tmp.name

            with open(temp_path, "r") as f:
                self.contentPane.setPlainText(f.read())

            self.toolbar.set_file_sloc(sloc_count)

        except Exception as e:
            self.contentPane.setPlainText(
                f"Error reading file:\n{file_path}\n\n{e}"
            )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())