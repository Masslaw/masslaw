from controller import Controller
from view import View


class App():

    def __init__(self):
        self._model = {}
        self._controller = Controller(self._model)
        self._view = View(self._model)
        self._should_close = False
        self._running = False

    def run(self):
        self._start()
        self._run_update_loop()
        self._destroy()

    def _start(self):
        self._reset_model()
        self._controller.setup()
        self._view.setup()
        self._running = True

    def _run_update_loop(self):
        while self._running:
            self._update()
            self._check_should_close()
            if self._should_close: self._running = False

    def _update(self):
        self._controller.update()
        self._view.render()

    def _check_should_close(self):
        self._should_close = self._should_close or self._view.should_close()

    def _destroy(self):
        self._view.destroy()
        self._controller.destroy()
        self._reset_model()

    def _reset_model(self):
        self._model = {}
