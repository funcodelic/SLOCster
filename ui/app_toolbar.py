from PyQt6.QtWidgets import QToolBar, QFileDialog
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal


class AppToolBar(QToolBar):
    directorySelected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__("Main Toolbar", parent)

        open_action = QAction("Open Directory", self)
        open_action.triggered.connect(self.open_directory)
        self.addAction(open_action)

    def open_directory(self):
        path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if path:
            self.directorySelected.emit(path)