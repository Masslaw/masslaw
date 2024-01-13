import unittest

from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.text_processing.knowledge_extraction.knowledge_extractors.spacy_wrapper._knowledge_merging_logic._entity_mergability_check_logic import check_spacy_entities_mergeable


class TestFunctionCheckSpacyEntitiesMergeable(unittest.TestCase):

    def test_entities_mergeable_with_same_id(self):
        entity = KnowledgeRecordEntity(entity_id="1", label="PERSON", properties={
            "title": "John Doe"
        })
        self.assertTrue(check_spacy_entities_mergeable(entity, KnowledgeRecordEntity(entity_id="1", label="PERSON", properties={
            "title": "Bob Doe"
        })))

    def test_entities_mergeable_with_person_typed_entities_with_same_title(self):
        entity = KnowledgeRecordEntity(label="PERSON", properties={
            "title": "John Doe"
        })
        self.assertTrue(check_spacy_entities_mergeable(entity, KnowledgeRecordEntity(label="PERSON", properties={
            "title": "John Doe"
        })))

    def test_entities_un_mergeable_with_person_typed_entities_with_title_overlap(self):
        entity = KnowledgeRecordEntity(label="PERSON", properties={
            "title": "John Doe"
        })
        self.assertFalse(check_spacy_entities_mergeable(entity, KnowledgeRecordEntity(label="PERSON", properties={
            "title": "Bob Doe"
        })))

    def test_entities_mergeable_with_person_typed_entities_with_valid_non_equal_titles(self):
        entity = KnowledgeRecordEntity(label="PERSON", properties={
            "title": "John Williams"
        })
        self.assertTrue(check_spacy_entities_mergeable(entity, KnowledgeRecordEntity(label="PERSON", properties={
            "title": "John"
        })))
        self.assertTrue(check_spacy_entities_mergeable(entity, KnowledgeRecordEntity(label="PERSON", properties={
            "title": "Mr. John"
        })))
        self.assertTrue(check_spacy_entities_mergeable(entity, KnowledgeRecordEntity(label="PERSON", properties={
            "title": "Mr. Williams"
        })))
        self.assertTrue(check_spacy_entities_mergeable(entity, KnowledgeRecordEntity(label="PERSON", properties={
            "title": "Williams"
        })))
        self.assertTrue(check_spacy_entities_mergeable(entity, KnowledgeRecordEntity(label="PERSON", properties={
            "title": "Dr. Williams"
        })))
        self.assertTrue(check_spacy_entities_mergeable(entity, KnowledgeRecordEntity(label="PERSON", properties={
            "title": "Dr. John Williams"
        })))
        self.assertTrue(check_spacy_entities_mergeable(entity, KnowledgeRecordEntity(label="PERSON", properties={
            "title": "Dr. John"
        })))

    def test_entities_mergeable_with_date_typed_entities_with_same_date(self):
        entity = KnowledgeRecordEntity(label="DATE", properties={
            "datetime": {
                "date": {
                    "Y": 2020,
                    "M": 6,
                    "D": 12,
                }
            }
        })
        self.assertTrue(check_spacy_entities_mergeable(entity, KnowledgeRecordEntity(label="DATE", properties={
            "datetime": {
                "date": {
                    "Y": 2020,
                    "M": 6,
                    "D": 12,
                }
            }
        })))

    def test_entities_un_mergeable_with_date_typed_entities_with_different_date(self):
        entity = KnowledgeRecordEntity(label="DATE", properties={
            "datetime": {
                "date": {
                    "Y": 2020,
                    "M": 6,
                    "D": 12,
                }
            }
        })
        self.assertFalse(check_spacy_entities_mergeable(entity, KnowledgeRecordEntity(label="DATE", properties={
            "datetime": {
                "date": {
                    "Y": 2020,
                    "M": 6,
                    "D": 13,
                }
            }
        })))
        self.assertFalse(check_spacy_entities_mergeable(entity, KnowledgeRecordEntity(label="DATE", properties={
            "datetime": {
                "date": {
                    "Y": 2020,
                    "M": 7,
                    "D": 12,
                }
            }
        })))
        self.assertFalse(check_spacy_entities_mergeable(entity, KnowledgeRecordEntity(label="DATE", properties={
            "datetime": {
                "date": {
                    "Y": 2021,
                    "M": 6,
                    "D": 12,
                }
            }
        })))

    def test_entities_mergeable_with_general_type_entities_with_same_title(self):
        entity = KnowledgeRecordEntity(label="PLACE", properties={
            "title": "The Tower Of Piza"
        })
        self.assertTrue(check_spacy_entities_mergeable(entity, KnowledgeRecordEntity(label="PLACE", properties={
            "title": "The Tower Of Piza"
        })))

    def test_entities_un_mergeable_with_general_type_entities_with_different_titles(self):
        entity = KnowledgeRecordEntity(label="PLACE", properties={
            "title": "The Tower Of Piza"
        })
        self.assertFalse(check_spacy_entities_mergeable(entity, KnowledgeRecordEntity(label="PLACE", properties={
            "title": "Eiffel Tower"
        })))

    def test_entities_mergeable_with_general_type_entities_with_vaild_title_overlap(self):
        entity = KnowledgeRecordEntity(label="PLACE", properties={
            "title": "The Tower Of Piza"
        })
        self.assertTrue(check_spacy_entities_mergeable(entity, KnowledgeRecordEntity(label="PLACE", properties={
            "title": "The Tower"
        })))
        self.assertTrue(check_spacy_entities_mergeable(entity, KnowledgeRecordEntity(label="PLACE", properties={
            "title": "Piza"
        })))
        self.assertTrue(check_spacy_entities_mergeable(entity, KnowledgeRecordEntity(label="PLACE", properties={
            "title": "At Piza"
        })))

    def test_entities_un_mergeable_with_general_type_entities_but_different_labels(self):
        entity = KnowledgeRecordEntity(label="PLACE", properties={
            "title": "The Tower Of Piza"
        })
        self.assertFalse(check_spacy_entities_mergeable(entity, KnowledgeRecordEntity(label="OBJECT", properties={
            "title": "The Tower Of Piza"
        })))
