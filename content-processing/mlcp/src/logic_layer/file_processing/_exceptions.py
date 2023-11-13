class FileTypeNotSupportedException(ValueError):
    def __init__(self, file_path: str):
        super().__init__(f"File: {file_path} is not supported")
