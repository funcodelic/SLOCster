from PyQt6.QtWidgets import QToolBar, QLabel, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class AppToolBar(QToolBar):

    def __init__(self, parent=None):
        super().__init__("Main Toolbar", parent)

        container = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        container.setLayout(layout)

        # Make the SLOC counts easy to read

        font = QFont()
        font.setPointSize(16)

        # Left label (total)
        self.totalLabel = QLabel("Total SLOC: 0")
        self.totalLabel.setFont(font)
        layout.addWidget(self.totalLabel)

        layout.addStretch()  # pushes next widget to right side

        # Right label (file)
        self.fileLabel = QLabel("File SLOC: 0")
        self.fileLabel.setFont(font)
        layout.addWidget(self.fileLabel)

        self.addWidget(container)

    # public update methods
    def set_total_sloc(self, value: int):
        self.totalLabel.setText(f"Total SLOC: {value}")

    def set_file_sloc(self, value: int):
        self.fileLabel.setText(f"File SLOC: {value}")