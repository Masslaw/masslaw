from typing import List

from logic_layer.bidi._read_directions import ReadDirection
from shared_layer.mlcp_logger import logger

_RTL_CHAR_RANGES = [('\u0590', '\u07FF'),  # Hebrew, Arabic, Syriac, Thaana, Nko, etc.
                    ('\u2D30', '\u2D7F'),  # Tifinagh
                    ('\u0800', '\u083F'),  # Samaritan
                    ('\uFB1D', '\uFDFF'),  # Hebrew and Arabic presentation forms
                    ('\uFE70', '\uFEFF'),  # Arabic presentation forms
                    ('\U00010E60', '\U00010E7F'),  # Rumi numeral symbols
                    ('\U0001EE00', '\U0001EEFF'),  # Arabic mathematical alphabetic symbols
                    ]


def get_text_direction(input_text) -> ReadDirection:
    input_text = str(input_text)
    rtl_chars = [c for c in input_text if any(start <= c <= end for start, end in _RTL_CHAR_RANGES)]
    ltr_chars = [c for c in input_text if c.isalpha() and c not in rtl_chars]
    has_rtl_chars = len(rtl_chars) > 0
    has_ltr_chars = len(ltr_chars) > 0
    if has_rtl_chars and not has_ltr_chars: return ReadDirection.RTL
    elif has_ltr_chars and not has_rtl_chars: return ReadDirection.LTR
    else: return ReadDirection.AMBIGUOUS


def swap_ordering_between_read_direction_and_ltr(text_parts: List, custom_text_direction: ReadDirection = None) -> List:
    rtl_accumulator: List = []
    result_parts: List = []
    text_direction = custom_text_direction or get_text_direction(text_parts[0])
    for part in text_parts:
        if get_text_direction(part) != text_direction:
            rtl_accumulator.append(part)
            continue
        if rtl_accumulator:
            result_parts.extend(rtl_accumulator[::-1])
            rtl_accumulator = []
        result_parts.append(part)
    if rtl_accumulator:
        result_parts.extend(rtl_accumulator[::-1])
    if text_direction == ReadDirection.RTL:
        result_parts = result_parts[::-1]
    return result_parts


def correct_ltr_sequenced_text(text: str):
    if len(text) == 0:
        return text
    words = text.split()
    words = [word[::-1] if get_text_direction(word) == ReadDirection.RTL else word for word in words]
    words = swap_ordering_between_read_direction_and_ltr(words)
    text = ' '.join(words)
    return text
