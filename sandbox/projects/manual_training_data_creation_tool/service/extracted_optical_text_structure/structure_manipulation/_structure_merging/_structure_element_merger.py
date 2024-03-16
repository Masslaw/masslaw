from service.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from service.extracted_optical_text_structure.structure_manipulation._structure_merging._cluster_merging import ClusterMerging
from service.extracted_optical_text_structure.structure_manipulation._structure_merging._sequential_merging import SequentialMerging


class OpticalTextStructureElementMerger:

    def __init__(self, element: OpticalTextStructureElement):
        self._element = element

    def merge_element_children_using_clustering(self, recursive: bool = True):
        ClusterMerging.merge_mergeable_element_children(element=self._element, recursive=recursive)

    def merge_element_children_sequentially(self, recursive: bool = True):
        SequentialMerging.merge_mergeable_element_children(element=self._element, recursive=recursive)
