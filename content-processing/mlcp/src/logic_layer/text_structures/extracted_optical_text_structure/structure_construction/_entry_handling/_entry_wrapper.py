from logic_layer.text_structures.extracted_optical_text_structure import OpticalElementRawDataEntry
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureElementBoundingRectangle


class EntryWrapper:

    def __init__(self, entry: OpticalElementRawDataEntry):
        self._entry = entry

    def get_entry(self):
        return self._entry

    def get_text(self) -> str:
        return self._entry[0]

    def set_text(self, text: str):
        self._entry = (text, self.get_bounding_rect())

    def get_bounding_rect(self) -> OpticalStructureElementBoundingRectangle:
        return self._entry[1]

    def set_bounding_rect(self, bounding_rect: OpticalStructureElementBoundingRectangle):
        self._entry = (self.get_text(), bounding_rect)

    def __str__(self):
        return self.get_text()
