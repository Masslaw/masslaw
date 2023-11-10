class EntityDictionaryDataPropertyMissing(ValueError):

    def __init__(self, property_name: str):
        super().__init__(f"A requires property is missing from an entity's dictionary data :: \"{property_name}\"")


class ConnectionDictionaryDataPropertyMissing(ValueError):

    def __init__(self, property_name: str):
        super().__init__(f"A requires property is missing from a connection's dictionary data :: \"{property_name}\"")


class RecordDictionaryDataPropertyMissing(ValueError):

    def __init__(self, property_name: str):
        super().__init__(f"A requires property is missing from a record's dictionary data :: \"{property_name}\"")
