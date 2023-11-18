class InvalidPathOrDirectory(ValueError):
    def __init__(self, path: str):
        super().__init__(f'The provided path "{path}" is not a valid path or directory')
