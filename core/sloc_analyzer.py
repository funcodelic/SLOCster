from dataclasses import dataclass

@dataclass
class LineAnalysis:
    line_number: int
    sloc_number: int | None
    text: str

class SlocAnalyzer:

    def analyze_directory(self, root_path: str):
        import os

        total_sloc = 0

        for root, dirs, files in os.walk(root_path):
            for file in files:
                if file.endswith(".swift"):
                    full_path = os.path.join(root, file)

                    with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                        for line in f:
                            if self.is_sloc(line):
                                total_sloc += 1

        return total_sloc

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

    def is_sloc(self, line: str) -> bool:
        stripped = line.strip()

        if not stripped:
            return False

        if stripped.startswith("//"):
            return False

        if stripped in {"{", "}"}:
            return False

        return True