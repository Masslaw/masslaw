
class OpensearchInnerQuery():

    _inner_query_payload = {}

    def _set_innter_query_payload(self, payload):
        self._inner_query_payload = payload

    def get_inner_query(self) -> dict:
        return self._inner_query_payload


class OpensearchMatchInnerQuery(OpensearchInnerQuery):
    def __init__(self, field: str, query: str, fuzziness: str = "AUTO"):
        payload = {"match": {field: {"query": query, "fuzziness": fuzziness}}}
        self._set_innter_query_payload(payload)


class OpensearchTermInnerQuery(OpensearchInnerQuery):
    def __init__(self, field: str, query: str):
        payload = {"term": {field: query}}
        self._set_innter_query_payload(payload)


class OpensearchPrefixInnerQuery(OpensearchInnerQuery):
    def __init__(self, field: str, query: str):
        payload = {"prefix": {field: query}}
        self._set_innter_query_payload(payload)


class OpensearchWildcardInnerQuery(OpensearchInnerQuery):
    def __init__(self, field: str, query: str):
        payload = {"wildcard": {field: query}}
        self._set_innter_query_payload(payload)
