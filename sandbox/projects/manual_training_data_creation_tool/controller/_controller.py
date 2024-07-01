import os.path
import tempfile

from service.masslaw_files_loader import load_masslaw_file


class Controller():

    def __init__(self, model):
        self._model = model
        self._application_should_close = False

    def setup(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self._model['temp_dir'] = temp_dir
            self._model['loaded_file_data'] = {}
            load_masslaw_file(_, _, _, os.path.dirname(__file__), self._model['loaded_file_data'])

    def update(self):
        pass

    def destroy(self):
        pass

    def should_close(self):
        return self._application_should_close
