class PDFDocumentTextExtractor:
    def __init__(self, file):
        self._file = file

    """
    resolutions:
     - glyphs :: characters
     - words  :: words
     - blocks :: paragraphs (text blocks)
    """  # def extract_text_structure(self, target_page_sizes: list, resolution='words'):  #      --- this doesn't work properly for some very odd reason  #     file_text_groups=[]  #     target_page_sizes = target_page_sizes or []  #     for i, page in enumerate(fitz.open(self._file)):  #         page_width, page_height = page.rect.width, page.rect.height  #         target_page_size = i < len(target_page_sizes) and target_page_sizes[i] or (page_width, page_height)  #         page_elements = []  #         for text_element in page.get_text(resolution):  #             text = text_element[4].strip()  #             element_bounding_rect = Rectangle(  #                 x1=target_page_size[0] * text_element[0] / page_width,  #                 y1=target_page_size[1] * text_element[1] / page_height,  #                 x2=target_page_size[0] * text_element[2] / page_width,  #                 y2=target_page_size[1] * text_element[3] / page_height,  #             )  #             if get_text_direction(text) < 0: text = text[::-1]  #             structure_element = get_appropriate_element(text, element_bounding_rect)  #             page_elements.append(structure_element)  #         page_text_group = build_group(page_elements)  #         page_text_group.set_width(page_width)  #         page_text_group.set_height(page_height)  #         page_text_group.restructure_children(merge=False)  #         file_text_groups.append(page_text_group)  #     return file_text_groups
