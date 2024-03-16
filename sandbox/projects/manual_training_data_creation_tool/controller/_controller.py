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
            load_masslaw_file("99839ded8e0af1e1cc72009a45357243", "AKIA23YSSEHNKULCRGOJ", "2kglfrMjfhdpggmkN90T6o6BWcnBL+R8aTaML0a7", os.path.dirname(__file__), self._model['loaded_file_data'])

    def update(self):
        pass

    def destroy(self):
        pass

    def should_close(self):
        return self._application_should_close
