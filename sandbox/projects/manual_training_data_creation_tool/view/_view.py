import os

import imgui

from service.masslaw_files_loader import load_masslaw_file
from view._imgui.imgui_renderer import ImguiRenderer

FONT_PATH = os.path.join(os.path.dirname(__file__), 'assets', 'font.ttf')

TOOLBAR_WINDOW_WIDTH = 300
FILE_DISPLAY_WINDOW_WIDTH = 500

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
        self._render_toolbar_window()
        self._render_file_display_window()

    def _render_toolbar_window(self):
        window_size = self._imgui_renderer.get_window_size()
        imgui.set_next_window_size(TOOLBAR_WINDOW_WIDTH, window_size[1])
        imgui.set_next_window_position(0, 0)
        if imgui.begin("toolbar", False, imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_COLLAPSE):
            imgui.button("BUTTON")
            imgui.end()

    def _render_file_display_window(self):
        window_size = self._imgui_renderer.get_window_size()
        imgui.set_next_window_size(max(FILE_DISPLAY_WINDOW_WIDTH, window_size[0] - TOOLBAR_WINDOW_WIDTH), window_size[1])
        imgui.set_next_window_position(TOOLBAR_WINDOW_WIDTH, 0)
        if imgui.begin("file_display", False, imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_COLLAPSE):
            imgui.button("BUTTON")
            imgui.end()
