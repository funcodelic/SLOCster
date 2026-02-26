from dataclasses import dataclass

# Line-by-line analysis to maintain the line number, slock count,
# and code alongside each other for pretty-printing.
# Each of these entries is one line with {line no, sloc cnt, code text}
@dataclass
class LineAnalysis:
    line_number: int
    sloc_number: int | None
    text: str

# Analyzes SLOC for directories and files
# Holds the rules as to what constitutes a true SLOC
# Lines that are blank or single comments (// or #)
# And lines with combinations of ()[]{};: only and no code
# are NOT true SLOCs and are not counted
class SlocAnalyzer:

    # Tally the SLOC of an entire directory, only .swift files for now
    def analyze_directory(self, root_path: str):
        import os

        total_sloc = 0

        for root, dirs, files in os.walk(root_path):
            for file in files:
                if file.endswith((".swift", ".py")):
                    full_path = os.path.join(root, file)

                    with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                        for line in f:
                            if self.is_sloc(line):
                                total_sloc += 1

        return total_sloc

    # Analyze a specific file for its SLOC count
    # The results returned is an array of {line no, sloc cnt, code}
    # used to pretty-print the file with annotated line numbers and sloc cnt
    def analyze_file(self, file_path: str):
        results = []
        sloc_count = 0

        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f, start=1):

                if self.is_sloc(line):
                    sloc_count += 1
                    results.append(LineAnalysis(i, sloc_count, line.rstrip("\n")))
                else:
                    results.append(LineAnalysis(i, None, line.rstrip("\n")))

        return results, sloc_count

    # Returns if it's a SLOC driven by simple rules
    # Does not account for block comments for simplicity
    # but does ignore blank lines, comments, and
    # combinations of " ()  []  {}  ;  : "  without any code
    def is_sloc(self, line: str) -> bool:
        stripped = line.strip()

        # Blank
        if not stripped:
            return False

        # Single-line comment
        if stripped.startswith("//") or stripped.startswith("#"):
            return False

        # Remove all whitespace (spaces/tabs)
        normalized = "".join(stripped.split())

        # Pure structural line: only (), {}, []
        if normalized and all(c in "(){}[];:" for c in normalized):
            return False

        return True