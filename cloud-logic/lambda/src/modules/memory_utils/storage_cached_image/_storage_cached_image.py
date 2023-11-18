import os.path
import secrets
import tempfile

import cv2
import numpy as np

cached_images_dir = tempfile.TemporaryDirectory()


class StorageCachedImage:
    """
    This class is used to store images in a temporary directory, and then retrieve them later.
    This class trade off speed for memory, as it is slower than just storing the image in memory,
    but it uses much less memory.
    """

    def __init__(self, save_format='png'):
        self.__save_format = save_format
        while True:
            self.__image_dir = os.path.join(cached_images_dir.name, f"{secrets.token_hex(16)}.{save_format}")
            if not os.path.exists(self.__image_dir):
                break

    def get_image(self) -> np.array:
        return cv2.imread(self.__image_dir)

    def set_image(self, img: np.array):
        cv2.imwrite(self.__image_dir, img)

    def get_dir(self) -> str:
        return self.__image_dir

    def duplicate(self) -> 'StorageCachedImage':
        new_image = StorageCachedImage(self.__save_format)
        new_image.set_image(self.get_image())
        return new_image

    def copy_to(self, other: 'StorageCachedImage'):
        other.set_image(self.get_image())

    def save_to(self, directory: str):
        cv2.imwrite(directory, self.get_image())
