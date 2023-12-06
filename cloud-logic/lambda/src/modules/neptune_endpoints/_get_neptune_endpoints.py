
def get_neptune_read_endpoint_for_stage(stage) -> str:
    return f"masslaw-knowledge-data-{stage}.cluster-ro-c6rrtlqu4oqc.us-east-1.neptune.amazonaws.com"


def get_neptune_write_endpoint_for_stage(stage) -> str:
    return f"masslaw-knowledge-data-{stage}.cluster-c6rrtlqu4oqc.us-east-1.neptune.amazonaws.com"
