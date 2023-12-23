from logic_layer.text_structures.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot


class ExtractedOpticalTextDocument:
    """
    The extracted optical text document, is the main data structure that is used to store the extracted optical text data.
    All the data is loaded into it, and all operations and calculations that need to be performed on the extracted optical
    text data are performed on it.
    """

    def __init__(self):
        self._structure_root = OpticalTextStructureRoot()
        self._metadata = {}

    def set_structure_root(self, structure_root: OpticalTextStructureRoot):
        self._structure_root = structure_root

    def get_structure_root(self) -> OpticalTextStructureRoot:
        return self._structure_root

    def set_metadata(self, metadata: dict):
        self._metadata = metadata

    def get_metadata(self):
        return self._metadata
