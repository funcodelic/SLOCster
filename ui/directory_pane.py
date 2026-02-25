# ui/directory_pane.py

from PyQt6.QtWidgets import QTreeView
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import pyqtSignal


class DirectoryPane(QTreeView):
    fileSelected = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Create the directory model
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.setModel(self.model)

        # Hide the header
        self.setHeaderHidden(True)

        # Hide all columns other than name
        for col in range(1, self.model.columnCount()):
            self.hideColumn(col)

        # Other tweaks
        self.setRootIsDecorated(True)
        self.setAlternatingRowColors(False)
        self.setSortingEnabled(False)

        # Connect to handle the click
        self.clicked.connect(self.handle_click)

    # Set the directory
    def set_directory(self, path):
        self.setRootIndex(self.model.index(path))

    # Handle the click
    def handle_click(self, index):
        path = self.model.filePath(index)
        if self.model.isDir(index):
            return
        self.fileSelected.emit(path) # Emit path of selected file