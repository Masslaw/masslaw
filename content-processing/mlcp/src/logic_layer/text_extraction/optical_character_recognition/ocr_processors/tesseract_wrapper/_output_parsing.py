from typing import List
from typing import Tuple

import pandas as pd
from shared_layer.list_utils import list_utils
from logic_layer.text_structures.extracted_optical_text_structure import OpticalElementRawDataEntry


def parse_tesseract_output(tesseract_output: pd.DataFrame) -> List[OpticalElementRawDataEntry]:
    elements_entries: List[OpticalElementRawDataEntry] = []
    for i in range(len(tesseract_output.get('text', []))):
        if len(tesseract_output['text'][i].replace(" ", "")) < 1: continue
        entry = get_entry_from_tesseract_output(tesseract_output, i)
        path = get_entry_path_from_tesseract_output(tesseract_output, i)
        put_entry_in_entry_structure(entry, elements_entries, path)
    return elements_entries


def get_entry_from_tesseract_output(tesseract_output: pd.DataFrame, index: int) -> OpticalElementRawDataEntry:
    text = tesseract_output['text'][index]
    left = tesseract_output['left'][index]
    top = tesseract_output['top'][index]
    width = tesseract_output['width'][index]
    height = tesseract_output['height'][index]
    bounding_rect = (left, top, left+width, top+height)
    entry = (text, bounding_rect)
    return entry


def get_entry_path_from_tesseract_output(tesseract_output: pd.DataFrame, index: int) -> Tuple:
    block_num = tesseract_output['block_num'][index] - 1
    par_num = tesseract_output['par_num'][index] - 1
    line_num = tesseract_output['line_num'][index] - 1
    word_num = tesseract_output['word_num'][index] - 1
    entry_path = (block_num, par_num, line_num, word_num)
    return entry_path


def put_entry_in_entry_structure(entry, structure, path):
    list_utils.force_element_in_index_path(structure, path, entry, default=list)
