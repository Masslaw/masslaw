MASSLAW_CASES_ES_ENDPOINT = 'https://search-masslaw-cases-yi2q4reazwjmc3zxq7qrz67qrq.us-east-1.es.amazonaws.com'
MASSLAW_CASE_FILES_SEARCH_INDEX_SUFFIX = '-case-files-search-index'
MASSLAW_CASE_COMMENTS_SEARCH_INDEX_SUFFIX = '-case-comments-search-index'
MASSLAW_CASE_TEXT_INDEX_CREATION_CONFIGURATION = {"settings": {"index.knn": True},
                                                  "mappings": {"properties": {"text": {"type": "text"}, "file_id": {"type": "text"}, "name": {"type": "text"}, "case_id": {"type": "text"}, "par_idx": {"type": "integer"}, "embedding": {"type": "knn_vector", "dimension": 1536}}}}
