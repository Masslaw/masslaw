

class DocumentLoadingInputFileTypeException(ValueError):
    def __init__(self, provided_type: str, required_type: str, context: str = None):
        super().__init__(f'The provided file type "{provided_type}" does not match '
                         f'the required type "{required_type}"' + (context and f' :: context - {context}' or ''))


class DocumentLoadingMetadataItemNoLabelException(ValueError):
    def __init__(self):
        super().__init__('A metadata item has no label.')
