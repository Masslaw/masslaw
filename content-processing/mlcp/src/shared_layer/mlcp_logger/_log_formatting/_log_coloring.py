def as_black(message: str) -> str:
    return _color_log_message(message, 'black')


def as_red(message: str) -> str:
    return _color_log_message(message, 'red')


def as_green(message: str) -> str:
    return _color_log_message(message, 'green')


def as_yellow(message: str) -> str:
    return _color_log_message(message, 'yellow')


def as_blue(message: str) -> str:
    return _color_log_message(message, 'blue')


def as_magenta(message: str) -> str:
    return _color_log_message(message, 'magenta')


def as_cyan(message: str) -> str:
    return _color_log_message(message, 'cyan')


def as_white(message: str) -> str:
    return _color_log_message(message, 'white')


def _color_log_message(message: str, color: str) -> str:
    return f'<{color}>{message}</{color}>'


__all__ = ['as_black', 'as_red', 'as_green', 'as_yellow', 'as_blue', 'as_magenta', 'as_cyan', 'as_white']
