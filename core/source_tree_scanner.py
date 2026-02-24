class SourceTreeScanner:

    def scan(self, root_path: str):
        import os

        results = []

        for root, dirs, files in os.walk(root_path):
            for file in files:
                if file.endswith(".swift"):
                    full_path = os.path.join(root, file)
                    results.append(full_path)

        return results