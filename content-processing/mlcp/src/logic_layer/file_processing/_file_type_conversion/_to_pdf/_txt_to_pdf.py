from logic_layer.file_processing._file_type_conversion._converter import FileConverter
from shared_layer.mlcp_logger import logger
from fpdf import FPDF


class TxtToPdf(FileConverter):
    supported_file_types = {"txt", "text", "log"}
    output_file_type = "pdf"

    @classmethod
    @logger.process_function("Converting a text file to PDF")
    def _do_convert(cls, txt_path: str, output_file_path: str):
        with open(txt_path, 'r') as f: text = f.read()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', size=12)
        pdf.write(5, text)
        pdf.output(output_file_path)
