class Report:
    def __init__(self):
        self.logs = []

    def log(self, message):
        print(f"[LOG] {message}")
        self.logs.append(message)

    def generate(self):
        with open("report.txt", "w") as f:
            for line in self.logs:
                f.write(line + "\n")
        print("[*] Report generated: report.txt")
