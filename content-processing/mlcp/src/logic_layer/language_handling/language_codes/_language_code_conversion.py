from typing import List

from logic_layer.language_handling.language_codes._types import Language
from logic_layer.language_handling.language_codes._types import LanguageCodeSet
from shared_layer.dictionary_utils import dictionary_utils


class _Converter:

    def __init__(self, codes: str | List[str]):
        self._codes = codes
        self._from_dict = {}
        self._to_set = {}

    def from_set(self, from_set: LanguageCodeSet) -> '_Converter':
        self._from_dict = dictionary_utils.invert_dict(from_set)
        return self

    def to_set(self, to_set: LanguageCodeSet) -> str | List[str]:
        codes = self._codes
        if isinstance(codes, str): codes = [codes]
        converted_codes = [to_set.get(self._from_dict.get(c, Language.__), '') for c in codes]
        if isinstance(self._codes, str): return converted_codes[0]
        return converted_codes


def convert(codes: str | List[str]) -> _Converter:
    return _Converter(codes)
