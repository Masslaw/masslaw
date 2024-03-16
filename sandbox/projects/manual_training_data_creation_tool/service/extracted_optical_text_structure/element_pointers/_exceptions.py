from service.extracted_optical_text_structure._types import OpticalDocumentElementsPointer


class InvalidPointerException(ValueError):

    def __init__(self, pointer: OpticalDocumentElementsPointer, reason: str = ''):
        super().__init__(f'Invalid pointer: {pointer} {reason and f"( :: {reason})" or ""}')
