from typing import List
from typing import Type

from logic_layer.knowledge_record import KnowledgeRecord
from logic_layer.knowledge_record.record_merging import RecordMerger
from logic_layer.knowledge_record.record_merging import RecordMergingConfiguration
from logic_layer.text_processing.knowledge_extraction._knowledge_extractor import KnowledgeExtractor


def execute_knowledge_extraction_with_extractors_on_file(extractors: List[Type[KnowledgeExtractor]], file_name: str, languages: List[str], merging_configuration: RecordMergingConfiguration=None):
    merging_configuration = merging_configuration or RecordMergingConfiguration()
    knowledge_record = KnowledgeRecord()
    merger = RecordMerger(knowledge_record, merging_configuration)
    for extractor in extractors:  # TODO - implement concurrent processing
        extractor_instance: KnowledgeExtractor = extractor(languages)
        extractor_instance.set_knowledge_merging_configuration(merging_configuration)
        extractor_instance.load_file(file_name)
        record = extractor_instance.get_record()
        merger.merge_record(record)
    return knowledge_record
