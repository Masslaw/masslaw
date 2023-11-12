import base64
from io import BytesIO
from typing import IO, List
from xml.etree import ElementTree

from PIL import Image

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure._structure_calculations import \
    StructureGeometryCalculator
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._assertions import \
    assert_export_output_file
from shared_layer.memory_utils.storage_cached_image import StorageCachedImage
from shared_layer.list_utils import list_utils


def export_document_to_html_format(optical_text_document: ExtractedOpticalTextDocument, output_file: IO, structure_children_background_images: List[StorageCachedImage] = None):
    assert_export_output_file(file=output_file, expected_type='html')
    document_element = _document_to_html_element(optical_text_document=optical_text_document, structure_children_background_images=structure_children_background_images or [])
    ElementTree.ElementTree(document_element).write(output_file, encoding='utf-8', xml_declaration=False)


def _document_to_html_element(optical_text_document: ExtractedOpticalTextDocument, structure_children_background_images: List[StorageCachedImage]) -> ElementTree.Element:
    document_html_element = ElementTree.Element('div')
    document_html_element.set('class', 'ml-document')

    structure_root = optical_text_document.get_structure_root()
    structure_html_element = _structure_root_to_html_element(structure_root, structure_children_background_images)
    document_html_element.append(structure_html_element)

    return document_html_element


def _structure_root_to_html_element(structure_root: OpticalTextStructureRoot, structure_children_background_images: List[StorageCachedImage]) -> ElementTree.Element:
    html_element = ElementTree.Element('div')
    html_element.set('class', 'ml-document-structure')

    for chile_num, child in enumerate(structure_root.get_children()):
        background_image = list_utils.get_element_at(structure_children_background_images, chile_num)
        html_element.append(_structure_child_to_html_element(child, background_image))

    return html_element


def _structure_child_to_html_element(structure_child: OpticalTextStructureElement, background_image: StorageCachedImage = None) -> ElementTree.Element:
    html_element = ElementTree.Element('div')
    structure_element_label = structure_child.__class__.get_label()
    html_element.set('class', f'{structure_element_label}')

    element_style = f'position: relative;'
    if background_image is not None:
        image = background_image.get_image()
        image_size = image.shape[:2]
        element_style += f' width: {image_size[1]}px; height: {image_size[0]}px;'
        pil_image = Image.fromarray(image)
        buffered = BytesIO()
        pil_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        element_style += f' background-image: url("data:image/png;base64,{img_str}");'

    html_element.set('style', element_style)
    if structure_child.is_leaf():
        html_element.text = structure_child.get_value()
        return html_element

    element_children = structure_child.get_children()
    for child in element_children:
        child_html_element = _structure_element_to_html_element(child)
        html_element.append(child_html_element)

    return html_element


def _structure_element_to_html_element(structure_element: OpticalTextStructureElement) -> ElementTree.Element:
    html_element = ElementTree.Element('p')
    structure_element_label = structure_element.__class__.get_label()
    html_element.set('class', f'{structure_element_label}')
    geometry_calculator = StructureGeometryCalculator(structure_element)
    bounding_rect = geometry_calculator.calculate_bounding_rect()
    bounding_rect = [int(v) for v in bounding_rect]
    element_style = f'position: absolute; margin: 0; padding: 0; font-size: {bounding_rect[2] - bounding_rect[0]}px; left: {bounding_rect[0]}; top: {bounding_rect[1]}px; width: {bounding_rect[2] - bounding_rect[0]}px; height: {bounding_rect[3] - bounding_rect[1]}px;'
    html_element.set('style', element_style)

    if structure_element.is_leaf():
        html_element.text = structure_element.get_value()
        return html_element

    element_children = structure_element.get_children()
    for child in element_children:
        child_html_element = _structure_element_to_html_element(child)
        html_element.append(child_html_element)

    return html_element
