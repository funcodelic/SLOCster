from PyQt6.QtWidgets import QTreeView
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFontDatabase

# Presents the directory tree structure to select files
# to visually confirm the SLOC counting algorithm
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

        # Increase the font size and add padding between rows
        font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        font.setPointSize(14)
        self.setFont(font)
        self.setStyleSheet("QTreeView::item { padding: 4px; }")

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