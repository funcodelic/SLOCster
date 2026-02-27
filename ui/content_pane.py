from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtGui import QFontDatabase

# Displays annotated code with line numbers and sloc count
# alongside the code to visually verify the SLOC count for a single file
class ContentPane(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: black; color: white;")
        self.setPlainText("Content area")

        font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        font.setPointSize(14)
        self.setFont(font)

    # Displays columns for line no, then SLOC count, then the code
    def build_formatted_text(self, analysis):
        lines = []
        lines.append("\n--- SLOC Analysis ---")
        lines.append(f"{'Line':>5}  {'SLOC':>5}  Text")
        lines.append("-" * 60)

        for entry in analysis:
            line_no = f"{entry.line_number:>5}"
            sloc_no = f"{entry.sloc_number:>5}" if entry.sloc_number else " " * 5
            lines.append(f"{line_no}  {sloc_no}  {entry.text}")

        total_sloc = sum(1 for e in analysis if e.sloc_number)
        lines.append("-" * 60)
        lines.append(f"Total SLOC: {total_sloc}")
        lines.append("")  # match print newline

        return "\n".join(lines)

    # Clears the display
    def clear_content(self):
        self.setPlainText("")