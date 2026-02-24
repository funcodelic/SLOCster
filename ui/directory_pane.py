# ui/directory_pane.py

from PyQt6.QtWidgets import QTreeView
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import pyqtSignal


class DirectoryPane(QTreeView):
    fileSelected = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.setModel(self.model)

        self.setHeaderHidden(True)

        for col in range(1, self.model.columnCount()):
            self.hideColumn(col)

        self.setRootIsDecorated(True)
        self.setAlternatingRowColors(False)
        self.setSortingEnabled(False)

        self.clicked.connect(self.handle_click)

    def set_directory(self, path):
        self.setRootIndex(self.model.index(path))

    def handle_click(self, index):
        path = self.model.filePath(index)
        if self.model.isDir(index):
            return
        self.fileSelected.emit(path)