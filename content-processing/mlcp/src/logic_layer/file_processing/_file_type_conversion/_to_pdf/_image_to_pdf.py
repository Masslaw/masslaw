import os

from PIL import Image
from reportlab.pdfgen import canvas

from logic_layer.file_processing._file_type_conversion._converter import FileConverter
from shared_layer.mlcp_logger import logger


class ImageToPdf(FileConverter):
    supported_file_types = {"bmp", "pbm", "pgm", "ppm", "sr", "ras",
                         "jpeg", "jpg", "jpe", "jp2", "tiff", "tif",
                         "png", "exr", "hdr", "pic", "webp"}
    output_file_type = "pdf"

    @classmethod
    @logger.process_function("Converting an Image file to PDF")
    def _do_convert(cls, image_path: str, output_file_path: str):
        with Image.open(image_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img_width, img_height = img.size
            c = canvas.Canvas(output_file_path, pagesize=(img_width, img_height))
            temp_img_path = 'temp.jpg'
            img.save(temp_img_path)
            c.drawImage(temp_img_path, 0, 0, img_width, img_height)
            c.showPage()
            c.save()
            os.remove(temp_img_path)
