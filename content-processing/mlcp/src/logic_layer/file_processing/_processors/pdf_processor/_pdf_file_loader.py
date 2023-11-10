import os
from typing import List

import cv2
import numpy as np
from pdf2image import convert_from_path
from pdf2image import pdfinfo_from_path

from shared_layer.file_system_utils import file_system_utils
from shared_layer.memory_utils.storage_cached_image import StorageCachedImage

_poppler_path = os.environ.get("poppler_path") or os.environ.get("POPPLER_PATH")


class PdfFileLoader:

    def __init__(self, file: str):
        self._file = file

        self._cache = {}

    def get_page_sizes(self) -> List[tuple]:
        page_images = self._get_page_images()

        image_sizes = []
        for page_image in page_images:
            image_sizes.append(page_image.get_image().shape[:2])

        return image_sizes

    def get_page_images_as_numpy_arrays(self) -> List[np.array]:
        page_images = self._get_page_images()

        image_sizes = []
        for page_image in page_images:
            image_sizes.append(page_image.get_image())

        return image_sizes

    def get_page_images_as_directories(self) -> List[str]:
        page_images = self._get_page_images()

        image_sizes = []
        for page_image in page_images:
            image_sizes.append(page_image.get_dir())

        return image_sizes

    def _get_page_images(self) -> List[StorageCachedImage]:
        page_images_cache_key = 'page_images'

        cached_page_images = self._cache.get(page_images_cache_key)
        if cached_page_images: return cached_page_images

        page_images = []
        for i in range(self.get_num_pages()):
            cached_image = StorageCachedImage()
            img = self._load_page_image(i)
            cached_image.set_image(img)
            page_images.append(cached_image)

        self._cache[page_images_cache_key] = page_images

        return page_images

    def _load_page_image(self, page_num, width=2_560, dpi=400):
        page = convert_from_path(pdf_path=self._file, dpi=dpi, first_page=page_num + 1, last_page=page_num + 1, poppler_path=_poppler_path)[0]
        img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, (int(width), int(img.shape[0] * width / img.shape[1])), interpolation=cv2.INTER_LANCZOS4)
        return img

    def get_num_pages(self):
        num_pages_cached_key = 'num_pages'

        cached_num_pages = self._cache.get(num_pages_cached_key)
        if cached_num_pages: return cached_num_pages

        num_pages = pdfinfo_from_path(pdf_path=self._file, poppler_path=_poppler_path).get("Pages")

        self._cache[num_pages_cached_key] = num_pages

        return num_pages

    def export_images(self, output_directory: str, image_prefix='image_', export_format='png'):
        page_images = self._get_page_images()
        for i, page_image in enumerate(page_images):
            image = page_image.get_image()
            image = cv2.resize(image, (int(2_560), int(image.shape[0] * 2_560 / image.shape[1])), interpolation=cv2.INTER_LANCZOS4)
            directory = file_system_utils.join_paths(output_directory, f"{image_prefix}{i}.{export_format}")
            cv2.imwrite(directory, image)
