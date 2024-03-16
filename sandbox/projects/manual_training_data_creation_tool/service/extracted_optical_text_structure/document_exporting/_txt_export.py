from typing import IO

from service.extracted_optical_text_structure import ExtractedOpticalTextDocument
from service.extracted_optical_text_structure.document_exporting._assertions import assert_export_output_file


def export_document_to_txt_format(optical_text_document: ExtractedOpticalTextDocument, output_file: IO):
    assert_export_output_file(file=output_file, expected_type='txt')

    document_text = _get_plain_text_from_document(optical_text_document)

    output_file.write(document_text)


def _get_plain_text_from_document(optical_text_document: ExtractedOpticalTextDocument):
    structure_root = optical_text_document.get_structure_root()
    text_parts = [child.get_value() for child in structure_root.get_children()]
    text = '\n'.join(text_parts)
    return text
