import os
import subprocess


class NeptuneStubTestLoader:
    def __init__(self):
        self.process = None

    def start_gremlin_server(self):
        server_executable_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'apache-tinkerpop-gremlin-server-3.7.0')
        self.process = subprocess.Popen([f'{server_executable_path}/bin/gremlin-server.sh', f'start'])

    def stop_gremlin_server(self):
        if self.process:
            try:
                self.process.terminate()  # Send termination signal
                self.process.wait(timeout=10)  # Wait for up to 10 seconds for process to terminate
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()

            self.process = None
