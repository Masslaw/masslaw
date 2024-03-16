class DocumentExportingOutputFileAccessException(ValueError):
    def __init__(self, required_access: str):
        super().__init__(f'The provided file must be opened with the following access(es) : {required_access} ')


class DocumentExportingOutputFileTypeException(ValueError):
    def __init__(self, provided_type: str, required_type: str, context: str = None):
        super().__init__(f'The provided file type "{provided_type}" does not match '
                         f'the required type "{required_type}"' + (context and f' :: context - {context}' or ''))


class DocumentExportingMetadataItemNoLabelException(KeyError):
    def __init__(self, metadata_item: dict):
        super().__init__(f'No label was provided in metadata item: {metadata_item}')


class DocumentExportingNonDictionaryMetadataItemException(ValueError):
    def __init__(self, metadata_item: dict):
        super().__init__(f'A non dictionary metadata item is present in the document\'s metadata :: {metadata_item}')
