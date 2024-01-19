from controller import Controller
from view import View


class App():

    def __init__(self):
        self._model = {}
        self._controller = Controller(self._model)
        self._view = View(self._model)

    def start(self):
        self._setup()
        self._start_update_loop()

    def _setup(self):
        self._reset_model()
        self._controller.setup()
        self._view.setup()

    def _start_update_loop(self):
        while True: self._on_update()

    def _on_update(self):
        self._controller.update()
        self._view.render()

    def destroy(self):
        self._view.destroy()
        self._controller.destroy()
        self._reset_model()

    def _reset_model(self):
        self._model = {}
