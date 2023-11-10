class KnowledgeRecordExportingOutputFileAccessException(ValueError):
    def __init__(self, required_access: str):
        super().__init__(f'The provided file must be opened with the following access(es) : {required_access} ')


class KnowledgeRecordExportingOutputFileTypeException(ValueError):
    def __init__(self, provided_type: str, required_type: str, context: str = None):
        super().__init__(f'The provided file type "{provided_type}" does not match '
                         f'the required type "{required_type}"' + (context and f' :: context - {context}' or ''))
