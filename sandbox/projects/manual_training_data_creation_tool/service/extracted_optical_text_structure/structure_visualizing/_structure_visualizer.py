from typing import List

from service.extracted_optical_text_structure import ExtractedOpticalTextDocument
from service.extracted_optical_text_structure.structure_visualizing._image_printing import print_structure_children_to_images


class StructureVisualizer:
    def __init__(self, document: ExtractedOpticalTextDocument):
        self._document = document

    def print_group_visualizations_to_images(self, image_directories: List[str], line_thickness: int = 4):
        structure_root = self._document.get_structure_root()
        print_structure_children_to_images(structure_root, image_directories, line_thickness)
