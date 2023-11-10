from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure.structure_manipulation._structure_cleanups._structure_cleanup_logic import cleanup_structure
from logic_layer.text_structures.extracted_optical_text_structure.structure_manipulation._structure_merging import OpticalTextStructureElementMerger
from shared_layer.concurrency_utils import run_thread_batch
from shared_layer.mlcp_logger import logger


class OpticalTextStructureManipulator:
    def __init__(self, document: ExtractedOpticalTextDocument):
        self._document = document

    @logger.process_function('Merging mergeable structure children sequentially')
    def merge_mergeable_structure_children_sequentially(self):
        structure = self._document.get_structure_root()
        structure_groups = structure.get_children()
        run_thread_batch(func=(lambda group_element: OpticalTextStructureElementMerger(group_element).merge_element_children_sequentially()), batch_inputs=structure_groups)
        structure.set_children(structure_groups)

    @logger.process_function('Merging mergeable structure children using rectangle clustering')
    def merge_mergeable_structure_children_using_rectangle_clustering(self):
        structure = self._document.get_structure_root()
        structure_groups = structure.get_children()
        structure_groups = [OpticalTextStructureElementMerger(group_element).merge_element_children_using_clustering() for group_element in structure_groups]
        structure.set_children(structure_groups)

    @logger.process_function('Cleaning document structure')
    def clean_document_structure(self):
        cleaned_structure = cleanup_structure(self._document.get_structure_root())
        self._document.set_structure_root(cleaned_structure)
