from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting import DocumentExporter
from logic_layer.text_structures.extracted_optical_text_structure.structure_visualizing import StructureVisualizer
from logic_layer.file_processing._processors import FileProcessor
from logic_layer.file_processing._processors._optical_shared import OpticalDocumentExtractor
from logic_layer.file_processing._processors.pdf_processor._pdf_file_loader import PdfFileLoader
from shared_layer.file_system_utils import file_system_utils


class PdfProcessor(FileProcessor):
    _extracted_text_document: ExtractedOpticalTextDocument

    def __init__(self, *args, **kwargs):
        FileProcessor.__init__(self, *args, **kwargs)

        self._pdf_loader = PdfFileLoader(self._file)

    def _process(self):
        image_directories = self._pdf_loader.get_page_images_as_directories()

        document_extractor = OpticalDocumentExtractor(self._languages)

        self._extracted_text_document = document_extractor.extract_text_document(image_directories)

    def _export_metadata(self, output_dir=""):
        return  # this is a placeholder

    def _export_text(self, output_dir=""):
        file_system_utils.clear_directory(output_dir)

        exporter = DocumentExporter(self._extracted_text_document)
        with open(file_system_utils.join_paths(output_dir, "text_structure.xml"), "wb") as f:
            exporter.export_xml(f)

        with open(file_system_utils.join_paths(output_dir, "plain_text.txt"), "w", encoding='utf-8') as f:
            exporter.export_text(f)

    def _export_assets(self, output_dir=""):
        file_system_utils.clear_directory(output_dir)

        exporter = DocumentExporter(self._extracted_text_document)
        with open(file_system_utils.join_paths(output_dir, "display.html"), "wb") as f:
            exporter.export_html(f, self._pdf_loader.get_page_images())

        self._pdf_loader.export_images(output_dir)

    def _export_debug_data(self, output_dir=""):
        file_system_utils.clear_directory(output_dir)

        self.export_text(file_system_utils.join_paths(output_dir, 'text_output'))
        self.export_assets(file_system_utils.join_paths(output_dir, 'assets_output'))
        self._visualize_structure(file_system_utils.join_paths(output_dir, 'structure_visualization'))

    def _visualize_structure(self, output_dir=""):
        file_system_utils.clear_directory(output_dir)

        self._pdf_loader.export_images(output_dir)

        image_directories = [file_system_utils.join_paths(output_dir, f) for f in file_system_utils.list_dir(output_dir)]
        image_directories.sort()

        visualizer = StructureVisualizer(self._extracted_text_document)
        visualizer.print_group_visualizations_to_images(image_directories)
