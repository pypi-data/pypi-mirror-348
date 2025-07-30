import subprocess
import threading

class ScriptRunner:
    def __init__(self, script_path):
        self.script_path = script_path
        self.process = None
        self.output_lines = []

    def start(self):
        if self.process is None:
            def run():
                self.process = subprocess.Popen(
                    ['python3', self.script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )
                for line in self.process.stdout:
                    self.output_lines.append(line.strip())
                self.process = None

            threading.Thread(target=run).start()
            return "Started"
        return "Already running"

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None
            return "Stopped"
        return "Not running"

    def get_output(self, last_n=50):
        return "\n".join(self.output_lines[-last_n:])
