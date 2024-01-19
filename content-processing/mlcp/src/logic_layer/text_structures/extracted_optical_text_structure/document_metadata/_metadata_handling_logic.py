from typing import List
from xml.etree import ElementTree as ET


def put_metadata_item(metadata_tree: ET.Element, metadata_path: List[str], metadata_item_label: str, metadata_item_data: dict):
    if len(metadata_path) == 0:
        metadata_item = ET.SubElement(metadata_tree, metadata_item_label)
        for k, v in metadata_item_data.items(): metadata_item.set(k, str(v))
        return metadata_item
    element = metadata_tree.find(metadata_path[0]) or ET.SubElement(metadata_tree, metadata_path[0])
    put_metadata_item(element, metadata_path[1:], metadata_item_label, metadata_item_data)
    return metadata_tree
