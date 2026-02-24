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



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vibe App")
        self.setFixedSize(1400, 800)

        self._createMenuBar()
        self._createToolbar()
        self._createCentralUI()

    # def _createMenuBar(self):
    #     menu_bar = self.menuBar()
    #     file_menu = menu_bar.addMenu("File")

    def _createMenuBar(self):
        file_menu = self.menuBar().addMenu("File")

        self.openDirAction = QAction("Open Directory", self)
        self.openDirAction.triggered.connect(self.open_directory)

        file_menu.addAction(self.openDirAction)

    # def _createToolbar(self):
    #     self.toolbar = AppToolBar(self)
    #     self.addToolBar(self.toolbar)
    #     self.toolbar.directorySelected.connect(self.handle_directory)

    def _createToolbar(self):
        self.toolbar = self.addToolBar("Main")
        self.toolbar.addAction(self.openDirAction)

    def handle_directory(self, path):
        print(path)

    def open_directory(self):
        path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if path:
            print(path)

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

        splitter.addWidget(self.directoryPane)
        splitter.addWidget(self.contentPane)

        splitter.setSizes([280, 1120])  # 1:4 ratio

        return splitter

    class DirectoryPane(QListWidget):
        def __init__(self):
            super().__init__()
            self.setStyleSheet("background-color: black; color: white;")
            self.addItems(["Item 1", "Item 2", "Item 3"])

    class ContentPane(QTextEdit):
        def __init__(self):
            super().__init__()
            self.setStyleSheet("background-color: black; color: white;")
            self.setText("Content area")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())