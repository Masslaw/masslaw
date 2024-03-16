from typing import Callable
from typing import List

import numpy as np

from service.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureCharacter
from service.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from service.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from service.extracted_optical_text_structure.structure_calculations import StructureGeometryCalculator
from service.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from service.extracted_optical_text_structure._types import OpticalStructureElementBoundingRectangle
from service.extracted_optical_text_structure.structure_manipulation._structure_merging._base_merge_logic import MergeLogicImplementation


class ClusterMerging(MergeLogicImplementation):
    @classmethod
    def _merge_line_elements(cls, line_elements: List[OpticalTextStructureLine]) -> List[OpticalTextStructureLine]:
        merged_lines = cls.__merge_elements_using_clustering(elements=line_elements, clustering_generator=cls._DistanceGenerators.continuous_horizontal_line_clustering,
            clusterer=cls._ClusteringAlgorithms.HDBSCAN(min_cluster_size=2, min_samples=None, cluster_selection_epsilon=0.1, metric='precomputed', algorithm='best', cluster_selection_method='eom',
                allow_single_cluster=True))
        return merged_lines

    @classmethod
    def _merge_word_elements(cls, word_elements: List[OpticalTextStructureWord]) -> List[OpticalTextStructureWord]:
        return word_elements

    @classmethod
    def _merge_character_elements(cls, character_elements: List[OpticalTextStructureCharacter]) -> List[OpticalTextStructureCharacter]:
        return character_elements

    @classmethod
    def __merge_elements_using_clustering(cls, elements: List[OpticalTextStructureElement], clustering_generator: Callable, clusterer: any) -> List[OpticalTextStructureElement]:
        element_clusters = cls.__cluster_elements(elements=elements, clustering_generator=clustering_generator, clusterer=clusterer)
        merged_elements = [cls._merge_elements_to_one(cluster) for cluster in element_clusters]
        return merged_elements

    @classmethod
    def __cluster_elements(cls, elements: List[OpticalTextStructureElement], clustering_generator: Callable, clusterer: any) -> List[List[OpticalTextStructureElement]]:
        rectangles = [StructureGeometryCalculator(element).calculate_bounding_rect() for element in elements]
        clusters = cls.cluster_rectangles(rectangles=rectangles, distance_generator=clustering_generator, clusterer=clusterer)
        element_clusters = [[elements[i] for i in cluster] for cluster in clusters]
        return element_clusters

    @classmethod
    def cluster_rectangles(cls, rectangles: List[OpticalStructureElementBoundingRectangle], distance_generator: Callable, clusterer, ) -> List[List[int]]:
        distance_matrix = np.array(distance_generator(rectangles))

        clusters = clusterer.fit_predict(distance_matrix)

        cluster_map = {}
        for idx, cluster_label in enumerate(clusters):
            if cluster_label == -1: continue
            if cluster_label not in cluster_map:
                cluster_map[cluster_label] = []
            cluster_map[cluster_label].append(idx)

        rectangle_clusters = list(cluster_map.values())

        return rectangle_clusters

    class _ClusteringAlgorithms:
        pass  # we used to have algorithms here, but since installing them makes the docker build be stuck, and since  # they are not used in the code, we removed them.

    class _DistanceGenerators:
        @staticmethod
        def continuous_horizontal_line_clustering(rectangles: List[OpticalStructureElementBoundingRectangle]) -> np.array:
            """
            this calculates a matrix in that satisfies:
            M[x, y] = distance(rectangles[x], rectangles[y])
            where distance(rect1, rect2) =
                  abs(rect1[1] - rect2[1]) +
                  abs(rect1[3] - rect2[3]) +
                  min(abs(rect1[0] - rect2[2]), abs(rect1[2] - rect2[0]))
              or mathematically : |r1.y1 - r2.y1| + |r1.y2 - r2.y2| + min(|r1.x1 - r2.x2|, |r1.x2 - r2.x1|)
              or in english : the distance is the sum of the difference in both y coordinates (the smaller it is the more
                  aligned the two rectangles are horizontally) and the gap between the rectangles horizontally
                  |====|<--gap-->|====|
            """

            np_rectangles = np.array(rectangles)

            y1_diff = np.abs(np_rectangles[:, 1, None] - np_rectangles[:, 1])
            y2_diff = np.abs(np_rectangles[:, 3, None] - np_rectangles[:, 3])
            x_diff = np.minimum(np.abs(np_rectangles[:, 0, None] - np_rectangles[:, 2]), np.abs(np_rectangles[:, 2, None] - np_rectangles[:, 0]))

            y1_diff /= y1_diff.max()
            y2_diff /= y2_diff.max()
            x_diff /= x_diff.max()

            distance_matrix = y1_diff + y2_diff + x_diff

            return distance_matrix

        continuous_horizontal_line_clustering = continuous_horizontal_line_clustering

        @staticmethod
        def continuous_vertical_line_clustering(rectangles: List[OpticalStructureElementBoundingRectangle]) -> np.array:
            """
            this calculates a matrix in that satisfies:
            M[x, y] = distance(rectangles[x], rectangles[y])
            where distance(rect1, rect2) =
                  abs(rect1[0] - rect2[0]) +
                  abs(rect1[2] - rect2[2]) +
                  min(abs(rect1[1] - rect2[3]), abs(rect1[3] - rect2[0]))
              or mathematically : |r1.x1 - r2.x1| + |r1.x2 - r2.x2| + min(|r1.y1 - r2.y2|, |r1.y2 - r2.y1|)
              or in english : the distance is the sum of the difference in both x coordinates (the smaller it is the more
                  aligned the two rectangles are horizontally) and the gap between the rectangles vertically
                  ====
                  ^
                  gap
                  v
                  ====
            """

            np_rectangles = np.array(rectangles)

            x1_diff = np.abs(np_rectangles[:, 0, None] - np_rectangles[:, 0])
            x2_diff = np.abs(np_rectangles[:, 2, None] - np_rectangles[:, 2])
            y_diff = np.minimum(np.abs(np_rectangles[:, 1, None] - np_rectangles[:, 3]), np.abs(np_rectangles[:, 3, None] - np_rectangles[:, 1]))

            distance_matrix = x1_diff + x2_diff + y_diff

            return distance_matrix

        continuous_vertical_line_clustering = continuous_vertical_line_clustering

        @staticmethod
        def horizontal_aligned_clustering(rectangles: List[OpticalStructureElementBoundingRectangle]) -> np.array:
            """
            this calculates a matrix in that satisfies:
            M[x, y] = distance(rectangles[x], rectangles[y])
            where distance(rect1, rect2) =
                  abs(rect1[1] - rect2[1]) +
                  abs(rect1[3] - rect2[3])
              or mathematically : |r1.y1 - r2.y1| + |r1.y2 - r2.y2|
              or in english : the distance is the sum of the difference in both y coordinates (the smaller it is the more
                  aligned the two rectangles are horizontally)
            """

            np_rectangles = np.array(rectangles)

            y1_diff = np.abs(np_rectangles[:, 1, None] - np_rectangles[:, 1])
            y2_diff = np.abs(np_rectangles[:, 3, None] - np_rectangles[:, 3])

            distance_matrix = y1_diff + y2_diff

            return distance_matrix

        horizontal_aligned_clustering = horizontal_aligned_clustering

        @staticmethod
        def vertical_aligned_clustering(rectangles: List[OpticalStructureElementBoundingRectangle]) -> np.array:
            """
            this calculates a matrix in that satisfies:
            M[x, y] = distance(rectangles[x], rectangles[y])
            where distance(rect1, rect2) =
                  abs(rect1[0] - rect2[0]) +
                  abs(rect1[2] - rect2[2])
              or mathematically : |r1.x1 - r2.x1| + |r1.x2 - r2.x2|
              or in english : the distance is the sum of the difference in both x coordinates (the smaller it is the more
                  aligned the two rectangles are vertically)x
            """

            np_rectangles = np.array(rectangles)

            x1_diff = np.abs(np_rectangles[:, 0, None] - np_rectangles[:, 0])
            x2_diff = np.abs(np_rectangles[:, 2, None] - np_rectangles[:, 2])

            distance_matrix = x1_diff + x2_diff

            return distance_matrix

        vertical_aligned_clustering = vertical_aligned_clustering
