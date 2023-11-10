class NoProcessorForFileException(ValueError):
    def __init__(self, file_type: str):
        super().__init__(f"No processor found for file type: {file_type}")
