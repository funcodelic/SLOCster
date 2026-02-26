import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QSplitter
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence, QShortcut
from PyQt6.QtWidgets import QFileDialog
from ui.app_toolbar import AppToolBar
from ui.directory_pane import DirectoryPane
from ui.content_pane import ContentPane
from core.sloc_analyzer import SlocAnalyzer
import tempfile
import os

# The app GUI, and mediator between the directory and content pane
# and the toolbar and SLOC analyzer
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SLOCster")
        self.setFixedSize(1400, 800)

        # Create the UI components
        self._createMenuBar()
        self._createToolbar()
        self._createCentralUI()

        # Create the SLOC analyzer and the path to rescan/recount
        self.slocAnalyzer = SlocAnalyzer()
        self.current_directory = None
        self.current_file_path = None

        # Just press the spacebar to rescan and update the UI
        self.spaceShortcut = QShortcut(QKeySequence(Qt.Key.Key_Space), self)
        self.spaceShortcut.activated.connect(self.rescan_directory)

    # Create the menu bar
    def _createMenuBar(self):
        file_menu = self.menuBar().addMenu("File")

        # Open Directory
        self.openDirAction = QAction("Open Directory", self)
        self.openDirAction.setShortcut(QKeySequence("Meta+O"))
        self.openDirAction.triggered.connect(self.open_directory)
        file_menu.addAction(self.openDirAction)

        # Scan (Cmd+S)
        self.scanAction = QAction("Scan", self)
        self.scanAction.setShortcut(QKeySequence("Meta+R"))
        self.scanAction.triggered.connect(self.rescan_directory)
        file_menu.addAction(self.scanAction)

    # Create the toolbar
    def _createToolbar(self):
        self.toolbar = AppToolBar(self)
        self.addToolBar(self.toolbar)

    # Handle directory selection
    def handle_directory(self, path):
        self.directoryPane.set_directory(path)

    # Open directory (from File)
    def open_directory(self):
        path = QFileDialog.getExistingDirectory(self, "Select Directory")

        # If switching directories, clear content pane
        if path != self.current_directory:
            self.contentPane.clear()
            self.current_file_path = None
            self.toolbar.set_file_sloc(0)

        if path:
            self.current_directory = path
            self.handle_directory(path)
            total = self.slocAnalyzer.analyze_directory(path)
            self.toolbar.set_total_sloc(total)  # or create set_directory_sloc()

    # Rescan the directory rather than having to open and select it again
    def rescan_directory(self):
        if not self.current_directory:
            return

        # 1️⃣ Rescan directory
        total = self.slocAnalyzer.analyze_directory(self.current_directory)
        self.toolbar.set_total_sloc(total)
        self.handle_directory(self.current_directory)

        # 2️⃣ If a file is currently open, refresh it
        if self.current_file_path:
            try:
                # Check file is still inside current directory
                if os.path.commonpath(
                        [self.current_file_path, self.current_directory]
                ) == self.current_directory:
                    # Re-analyze file
                    analysis, sloc_count = self.slocAnalyzer.analyze_file(
                        self.current_file_path
                    )

                    # Redraw content
                    formatted_text = self.contentPane.build_formatted_text(analysis)
                    self.contentPane.setPlainText(formatted_text)

                    # Update file SLOC in toolbar
                    self.toolbar.set_file_sloc(sloc_count)

            except Exception as e:
                self.current_file_path = None
                self.toolbar.set_file_sloc(0)
                self.contentPane.setPlainText(
                    f"File no longer available or failed to analyze:\n\n{e}"
                )

    # Create center UI (split view holding directory and content panes)
    def _createCentralUI(self):
        central_widget = QWidget()
        layout = QHBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        splitter = self._createSplitter()
        layout.addWidget(splitter)

    # Create splitter (and make connections)
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
        # Only allow Swift and python files
        if not file_path.lower().endswith((".swift", ".py")):
            return

        try:
            analysis, sloc_count = self.slocAnalyzer.analyze_file(file_path)
            self.current_file_path = file_path
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