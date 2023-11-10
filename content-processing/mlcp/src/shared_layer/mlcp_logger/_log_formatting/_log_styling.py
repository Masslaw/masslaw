def as_italic(message: str) -> str:
    return _style_log_message(message, 'italic')


def as_bold(message: str) -> str:
    return _style_log_message(message, 'bold')


def as_underline(message: str) -> str:
    return _style_log_message(message, 'underline')


def as_blink(message: str) -> str:
    return _style_log_message(message, 'blink')


def as_mark(message: str) -> str:
    return _style_log_message(message, 'mark')


def as_concealed(message: str) -> str:
    return _style_log_message(message, 'concealed')


def as_strike(message: str) -> str:
    return _style_log_message(message, 'strike')


def _style_log_message(message: str, styling: str) -> str:
    return f'<{styling}>{message}</{styling}>'


__all__ = ['as_italic', 'as_bold', 'as_underline', 'as_blink', 'as_mark', 'as_concealed', 'as_strike']
