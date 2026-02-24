class SourceTreeScanner:
    def __init__(self, root_path: str):
        self.root_path = root_path

    def scan(self):
        """Return list of file paths under root_path."""
        import os
        results = []
        for root, dirs, files in os.walk(self.root_path):
            for file in files:
                results.append(os.path.join(root, file))
        return results