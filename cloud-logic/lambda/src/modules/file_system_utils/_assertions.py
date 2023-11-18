import os

from shared_layer.file_system_utils._exceptions import InvalidPathOrDirectory


def assert_directory_exists(directory: str):
    if os.path.exists(directory): return
    raise InvalidPathOrDirectory("the provided file directory is not a valid file or directory")
