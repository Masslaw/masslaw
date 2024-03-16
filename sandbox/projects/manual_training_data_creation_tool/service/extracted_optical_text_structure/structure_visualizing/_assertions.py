from typing import List

from service.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot
from service.extracted_optical_text_structure.structure_visualizing._exceptions import InvalidNumberOfPrintTargetImages


def assert_number_of_images_matches_number_of_structure_groups(structure_root: OpticalTextStructureRoot, image_directories: List[str]):
    assert_num_images(len(structure_root.get_children()), len(image_directories))


def assert_num_images(target, num_images):
    if target == num_images: return
    raise InvalidNumberOfPrintTargetImages(target, num_images)


def assert_real_image(image):
    if image is not None: return
    raise ValueError(f'Expected image to be real, got None')
