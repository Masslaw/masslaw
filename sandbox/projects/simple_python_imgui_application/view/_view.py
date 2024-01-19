import os

from view._imgui.imgui_renderer import ImguiRenderer

FONT_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'font.ttf')


class View():

    def __init__(self, model):
        self._model = model
        self._imgui_renderer = ImguiRenderer()
        self._application_should_close = False

    def setup(self):
        self._imgui_renderer.setup()
        self._imgui_renderer.add_render_body_function(self._imgui_body_render_function)

    def render(self):
        self._imgui_renderer.render_frame()

    def destroy(self):
        self._imgui_renderer.destroy()

    def should_close(self):
        if self._application_should_close: return True
        if self._imgui_renderer.should_close(): return True
        return False

    def _imgui_body_render_function(self):
        ...
