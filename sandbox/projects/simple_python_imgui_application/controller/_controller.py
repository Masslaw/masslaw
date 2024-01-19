class Controller():

    def __init__(self, model):
        self._model = model
        self._application_should_close = False

    def setup(self):
        pass

    def update(self):
        pass

    def destroy(self):
        pass

    def should_close(self):
        return self._application_should_close
