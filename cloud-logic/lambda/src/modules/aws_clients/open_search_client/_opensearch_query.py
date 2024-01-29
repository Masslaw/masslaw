from typing import List
from typing import Tuple

from src.modules.aws_clients.open_search_client._inner_queries import OpensearchInnerQuery
from src.modules.aws_clients.open_search_client._query_sort_orders import OpensearchQuerySortOrder


class OpensearchQuery:
    def __init__(self):
        self._inner_query: OpensearchInnerQuery = OpensearchInnerQuery()
        self._fuzziness: str = "AUTO"
        self._highlights: List[Tuple[str, int]] = []
        self._sorting: List[Tuple[str, OpensearchQuerySortOrder]] = []
        self._include_source_fields: List[str] = []
        self._documents: List[str] = []

    def get_payload(self):
        inner_query = self._inner_query.get_inner_query()

        payload = {"query": {"bool": {"must": [inner_query]}}}

        if self._documents:
            payload["query"]["bool"]["must"].append({"terms": {"_id": self._documents}})

        if self._include_source_fields:
            payload["_source"] = self._include_source_fields

        if self._highlights:
            payload['highlight'] = {
                "fields": {_highlight_field: {"fragment_size": _highlight_padding} for _highlight_field, _highlight_padding in self._highlights},
                "pre_tags": ["<search_result>"],
                "post_tags": ["</search_result>"]
            }

        if self._sorting:
            payload["sort"] = [{_sort_field: {"order": _sort_order.value}} for _sort_field, _sort_order in self._sorting]

        return payload

    def set_inner_query(self, inner_query: OpensearchInnerQuery):
        self._inner_query = inner_query

    def set_fuzziness(self, fuzziness):
        self._fuzziness = fuzziness

    def include_source_fields(self, source_fields):
        self._include_source_fields = source_fields

    def enable_highlight(self, highlight_field: str, highlight_padding: int = 50):
        self._highlights.append((highlight_field, highlight_padding))

    def add_sorting(self, sort_field: str, sort_order: OpensearchQuerySortOrder):
        self._sorting.append((sort_field, sort_order))

    def set_documents(self, documents: List[str]):
        self._documents = documents