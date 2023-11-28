import unittest

from logic_layer.language_handling.language_codes import Language
from logic_layer.language_handling.language_codes import convert


class TestFunctionConvert(unittest.TestCase):

    def setUp(self):
        self.language_code_set1 = {
            Language.English: 'en',
            Language.Spanish: 'es',
            Language.French: 'fr',
            Language.German: 'de',
            Language.Hebrew: 'he',
            Language.Hindi: 'hi',
        }

        self.language_code_set2 = {
            Language.English: 'eng',
            Language.Spanish: 'spa',
            Language.French: 'fre',
            Language.German: 'ger',
            Language.Arabic: 'ara',
            Language.Italian: 'ita',
        }

    def test_on_single(self):
        language = Language.English
        input = self.language_code_set1[language]
        converted = convert(input).from_set(self.language_code_set1).to_set(self.language_code_set2)
        self.assertEqual(converted, self.language_code_set2[language])

    def test_on_list(self):
        languages = [Language.English, Language.Spanish, Language.French]
        input = [self.language_code_set1[language] for language in languages]
        converted = convert(input).from_set(self.language_code_set1).to_set(self.language_code_set2)
        self.assertEqual(converted, [self.language_code_set2[language] for language in languages])

    def test_with_language_only_in_first_set(self):
        language = Language.Hebrew
        input = self.language_code_set1[language]
        converted = convert(input).from_set(self.language_code_set1).to_set(self.language_code_set2)
        self.assertEqual(converted, '')

    def test_with_language_only_in_second_set(self):
        input = 'ar'
        converted = convert(input).from_set(self.language_code_set2).to_set(self.language_code_set1)
        self.assertEqual(converted, '')

    def test_with_entire_set(self):
        languages = list(self.language_code_set1.keys())
        input = [self.language_code_set1[language] for language in languages]
        converted = convert(input).from_set(self.language_code_set1).to_set(self.language_code_set2)
        self.assertEqual(converted, [self.language_code_set2.get(language, '') for language in languages])
