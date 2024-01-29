from logic_layer.bidi import ReadDirection
from logic_layer.bidi import swap_ordering_between_read_direction_and_ltr
from logic_layer.file_processing._file_type_conversion._converter import FileConverter
from resources_layer.assets.assets_loader import get_asset_full_path
from shared_layer.mlcp_logger import logger
from fpdf import FPDF

free_sans_font_path = get_asset_full_path('fonts/freesans/FreeSans.ttf')


class TxtToPdf(FileConverter):
    supported_file_types = {"txt", "text", "log"}
    output_file_type = "pdf"

    @classmethod
    @logger.process_function("Converting a text file to PDF")
    def _do_convert(cls, txt_path: str, output_file_path: str):
        with open(txt_path, 'r') as f: text = f.read()
        text = ''.join(swap_ordering_between_read_direction_and_ltr(list(text), custom_text_direction=ReadDirection.LTR))
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('FreeSans', '', free_sans_font_path, uni=True)
        pdf.set_font('FreeSans', size=12)
        pdf.write(5, text)
        pdf.output(output_file_path)
