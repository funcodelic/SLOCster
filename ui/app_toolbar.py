from PyQt6.QtWidgets import QToolBar, QLabel, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt


class AppToolBar(QToolBar):

    def __init__(self, parent=None):
        super().__init__("Main Toolbar", parent)

        container = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)
        container.setLayout(layout)

        # Left label (total)
        self.totalLabel = QLabel("Total SLOC: 0")
        layout.addWidget(self.totalLabel)

        layout.addStretch()  # pushes next widget to right side

        # Right label (file)
        self.fileLabel = QLabel("File SLOC: 0")
        layout.addWidget(self.fileLabel)

        self.addWidget(container)

    # public update methods
    def set_total_sloc(self, value: int):
        self.totalLabel.setText(f"Total SLOC: {value}")

    def set_file_sloc(self, value: int):
        self.fileLabel.setText(f"File SLOC: {value}")