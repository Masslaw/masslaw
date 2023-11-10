import os
from typing import List

import numpy as np
import pandas as pd
import pytesseract
from PIL import Image

from logic_layer.text_extraction.optical_character_recognition._ocr_processor import OCRProcessor
from logic_layer.text_extraction.optical_character_recognition.ocr_processors.tesseract_wrapper._output_parsing import parse_tesseract_output
from logic_layer.text_structures.extracted_optical_text_structure import OpticalElementRawDataEntry

if 'tesseract_path' in os.environ: pytesseract.pytesseract.tesseract_cmd = os.environ['tesseract_path']


class TesseractWrapper(OCRProcessor):
    def _extract_text_in_image(self, image: np.array) -> List[OpticalElementRawDataEntry]:
        image_data: pd.DataFrame = pytesseract.pytesseract.image_to_data(Image.fromarray(image), output_type=pytesseract.Output.DICT, lang="+".join(self._languages))
        text_elements = parse_tesseract_output(image_data)
        return text_elements
