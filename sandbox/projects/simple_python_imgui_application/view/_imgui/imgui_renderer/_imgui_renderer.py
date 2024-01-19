import os

import OpenGL.GL as gl
import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer


DEFAULT_FONT_PATH = os.path.join(os.path.dirname(__file__), 'default_font.ttf')


class ImguiRenderer:

    def __init__(self):
        self._impl = None
        self._window = None
        self._loaded_font = None
        self._background_color = (0, 0, 0, 1)
        self._render_body_functions = []
        self._should_close = False

    def setup(self):
        imgui.create_context()
        self._create_window()
        io = imgui.get_io()
        self._loaded_font = io.fonts.add_font_from_file_ttf(DEFAULT_FONT_PATH, 30)
        self._impl = GlfwRenderer(self._window)
        gl.glClearColor(*self._background_color)

    def render_frame(self):
        self._imgui_frame_start()
        self._imgui_render_body()
        self._imgui_frame_finish()

    def _imgui_frame_start(self):
        glfw.poll_events()
        self._impl.process_inputs()
        imgui.new_frame()
        gl.glClearColor(*self._background_color)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.push_font(self._loaded_font)

    def _imgui_render_body(self):
        for function in self._render_body_functions: function()

    def _imgui_frame_finish(self):
        imgui.pop_font()
        imgui.render()
        self._impl.render(imgui.get_draw_data())
        glfw.swap_buffers(self._window)
        self._should_close = self._should_close or glfw.window_should_close(self._window)

    def destroy(self):
        self._impl.shutdown()
        glfw.terminate()

    def _create_window(self, window_name="", width=500, height=500):
        if not glfw.init(): raise Exception("Could not initialize Window")
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
        self._window = glfw.create_window(int(width), int(height), window_name, None, None)
        glfw.make_context_current(self._window)
        if not self._window: raise Exception("Could not initialize Window")

    def add_render_body_function(self, function):
        self._render_body_functions.append(function)

    def get_window_size(self):
        return glfw.get_window_size(self._window)

    def should_close(self):
        return self._should_close
