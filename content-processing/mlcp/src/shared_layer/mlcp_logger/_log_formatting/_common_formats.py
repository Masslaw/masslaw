from shared_layer.mlcp_logger._log_formatting._log_coloring import as_green
from shared_layer.mlcp_logger._log_formatting._log_coloring import as_magenta
from shared_layer.mlcp_logger._log_formatting._log_coloring import as_red
from shared_layer.mlcp_logger._log_formatting._log_coloring import as_yellow
from shared_layer.mlcp_logger._log_formatting._log_styling import as_bold
from shared_layer.mlcp_logger._log_formatting._log_styling import as_mark
from shared_layer.mlcp_logger._log_formatting._log_styling import as_underline


def value(message: any) -> str:
    message = str(message)
    return as_magenta(as_underline(message))


def good(message: str) -> str:
    message = str(message)
    message = '✓ ' + message
    return as_green(as_bold(message))


def bad(message: str) -> str:
    message = str(message)
    message = '✗ ' + message
    return as_red(as_bold(message))


def important(message: str) -> str:
    message = str(message)
    return as_yellow(as_underline(message))


def critical(message: str) -> str:
    message = str(message)
    return as_red(as_mark(message))


__all__ = ['value', 'important', 'critical']
