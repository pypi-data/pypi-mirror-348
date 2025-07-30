
from .run_class import ScriptRunner
from flask import send_from_directory
from flask import Flask, send_from_directory, Response

class ScriptServer:
    def __init__(self, script_path: str, port: int = 5000):
        self.script_path = script_path
        self.port = port
        self.runner = ScriptRunner(script_path=script_path)
        self.app = Flask(__name__)
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route('/')
        def index():
            return send_from_directory('.', 'static/index.html')

        @self.app.route('/start', methods=['GET'])
        def start():
            return self.runner.start()

        @self.app.route('/stop', methods=['GET'])
        def stop():
            return self.runner.stop()

        @self.app.route('/status')
        def status():
            return "Running" if self.runner.process else "Stopped"

        @self.app.route('/log', methods=['GET'])
        def log():
            return Response(self.runner.get_output(), mimetype='text/plain')

    def run(self):
        self.app.run(host="0.0.0.0", port=self.port)

if __name__ == "__main__":
    server = ScriptServer(script_path="active/NetScript/v0.0/src/scripts/script_1.py", port=5000)
    server.run()