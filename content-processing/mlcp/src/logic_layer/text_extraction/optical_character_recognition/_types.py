from typing import Tuple
from typing import Type

# defined as (x1, y1, x2, y2)
OcrExtractedElementBoundingRectangle: Type = Tuple[float, float, float, float]

# defined as (value, bounding_rectangle)
OcrExtractedElement: Type = Tuple[str, OcrExtractedElementBoundingRectangle]
