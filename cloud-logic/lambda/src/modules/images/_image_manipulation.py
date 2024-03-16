import base64
from io import BytesIO
from PIL import Image


class ImageManipulator:
    __image: Image.Image

    def set_image(self, image: Image.Image):
        self.__image = image

    def from_base64(self, base64_string: str):
        image_data = base64.b64decode(base64_string)
        image_file = BytesIO(image_data)
        self.__image = Image.open(image_file)

    def resize_width(self, new_width: int):
        aspect_ratio = self.__image.height / self.__image.width
        new_height = int(aspect_ratio * new_width)
        self.resize(new_width, new_height)

    def resize_height(self, new_height: int):
        aspect_ratio = self.__image.width / self.__image.height
        new_width = int(aspect_ratio * new_height)
        self.resize(new_width, new_height)

    def resize(self, new_width: int, new_height: int):
        self.__image = self.__image.resize((new_width, new_height))

    def to_jpeg_format(self, quality: int = 85) -> bytes:
        buffered = BytesIO()
        self.__image.convert('RGB').save(buffered, format="JPEG", quality=quality)
        byte_data = buffered.getvalue()
        return byte_data

    def to_png_format(self) -> bytes:
        buffered = BytesIO()
        self.__image.save(buffered, format="PNG")
        byte_data = buffered.getvalue()
        return byte_data


