import cv2
import numpy as np

from service.memory_utils.controlled_data_loading._controlled_data_loader import MemoryControlledDataLoader


class MemoryControlledOpenCVImageLoader(MemoryControlledDataLoader):
    def load_data(self, load_input: str) -> np.array:
        return cv2.imread(load_input)
