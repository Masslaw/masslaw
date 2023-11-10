import logging


class MLCPLogFormatter(logging.Formatter):
    COLOR_MAP = {
        'black': '\033[30m', 'red': '\033[31m', 'green': '\033[32m', 'yellow': '\033[33m', 'blue': '\033[34m', 'magenta': '\033[35m', 'cyan': '\033[36m', 'white': '\033[37m', 'reset': '\033[0m',
    }

    STYLE_MAP = {
        'bold': '\033[1m', 'underline': '\033[4m', 'blink': '\033[5m', 'mark': '\033[7m', 'concealed': '\033[8m', 'strike': '\033[9m', 'italic': '\033[3m', 'reset': '\033[0m',
    }

    def __init__(self, apply_colors=False, apply_styles=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_colors = apply_colors
        self._apply_styles = apply_styles

    def set_colored(self, colored):
        self._apply_colors = colored

    def set_styled(self, styled):
        self._apply_styles = styled

    def format(self, record):
        msg = super().format(record)
        msg = self.apply_colors_to_message(msg)
        msg = self.apply_styling_to_message(msg)
        return msg

    def apply_colors_to_message(self, message):
        for color_name, color_value in self.COLOR_MAP.items():
            color_start_value = color_value
            color_reset_value = self.COLOR_MAP['reset']
            if not self._apply_colors:
                color_start_value = ''
                color_reset_value = ''
            message = message.replace(f'<{color_name}>', color_start_value).replace(f'</{color_name}>', color_reset_value)
        return message

    def apply_styling_to_message(self, message):
        for style_name, style_value in self.STYLE_MAP.items():
            style_start_value = style_value
            style_reset_value = self.STYLE_MAP['reset']
            if not self._apply_styles:
                style_start_value = ''
                style_reset_value = ''
            message = message.replace(f'<{style_name}>', style_start_value).replace(f'</{style_name}>', style_reset_value)
        return message
