from typing import Callable

from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record._record import KnowledgeRecord


def knowledge_record_to_mermaid(record: KnowledgeRecord, filename: str = 'record.mermaid', entity_title_generator: Callable[[KnowledgeRecordEntity], str] = None):
    mermaid_script = "graph LR\n"
    for entity in record.get_entities():
        entity_id = entity.get_id()
        entity_title = entity_title_generator and entity_title_generator(entity) or entity_id
        entity_title = '"' + entity_title.replace('"', '') + '"'
        mermaid_script += f"{entity_id}({entity_title})\n"
    for connection in record.get_connections():
        from_id = connection.get_from_entity().get_id()
        to_id = connection.get_to_entity().get_id()
        mermaid_script += f"{from_id} -->|{connection.get_label()}| {to_id}\n"
    with open(filename, 'w') as file:
        file.write(mermaid_script)
