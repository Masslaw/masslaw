CUSTOM_ENTITY_MATCHING = {
    "PERSON": [
        [
            {"LOWER": {"IN": ["dr", "mr", "mrs", "ms", "miss", "sir", "madam", "prof", "professor", "president", "chairman", "chairwoman", "chairperson", "ceo", "cfo", "cto", ]}},  # Titles
            {"TEXT": ".", "OP": "?"},
            {"IS_SPACE": True, "OP": "*"},
            {"IS_ALPHA": True}
        ],
    ],
    "DATE": [
        [
            {"IS_DIGIT": True, "IS_ALPHA": False},
            {"TEXT": {"IN": ["/", "\\", ",", "-", "."]}},
            {"IS_DIGIT": True, "IS_ALPHA": False},
            {"TEXT": {"IN": ["/", "\\", ",", "-", "."]}},
            {"IS_DIGIT": True, "IS_ALPHA": False},
        ],
        [
            {"TEXT": {"IN": ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]}},
        ],
    ],
}