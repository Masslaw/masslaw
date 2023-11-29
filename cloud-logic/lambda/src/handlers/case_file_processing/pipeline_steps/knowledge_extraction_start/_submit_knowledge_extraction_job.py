from src.modules.masslaw_cases_objects import MasslawCaseFileInstance
from src.modules.mlcp_management import MLCPSubmission
from src.modules.aws_clients.batch_client import batch_management


def submit_knowledge_extraction_job(file_instance: MasslawCaseFileInstance, stage='prod'):
    file_id = file_instance.get_file_id()
    case_id = file_instance.get_data_property(['case_id'])
    file_type = file_instance.get_data_property(["type"])
    languages = file_instance.get_data_property(["languages"], ['eng'])

    text_file_key = f'{file_id}/raw.{file_type}'
    text_file_name = f'{file_id}.{file_type}'

    mlcp = MLCPSubmission(stage=stage)
    mlcp.add_action({
        "name": "s3_download",
        "params": {
            "bucket": "masslaw-cases-content",
            "files_data": [{
                "key": text_file_key,
                "save_as": text_file_name
            }]
        },
        "required": "True"
    })
    mlcp.add_action({
        "name": "process_files",
        "params": {
            "files_data": [
                {
                    "file_name": text_file_name,
                    "languages": languages,
                    "case_id": case_id,
                    "file_id": file_id,
                    "neptune_endpoints": {
                        "read": {
                            "endpoint": _get_neptune_read_endpoint_for_stage(stage),
                            "port": "8182",
                            "type": "gremlin"
                        },
                        "write": {
                            "endpoint": _get_neptune_write_endpoint_for_stage(stage),
                            "port": "8182",
                            "type": "gremlin"
                        }
                    },
                    "knowledge_record_data": {
                        "node_properties": {
                            "file_id": file_id,
                            "case_id": case_id
                        },
                        "edge_properties": {
                            "file_id": file_id,
                            "case_id": case_id
                        }
                    }
                }
            ]
        },
        "required": "True"
    })

    mlcp_job = mlcp.get_job()
    mlcp_job.queue = f'mlcp-knowledge-extraction-queue-{stage}'

    processing_job_id = batch_management.submit_job(mlcp_job)

    return processing_job_id


def _get_neptune_read_endpoint_for_stage(stage) -> str:
    if stage == 'dev':
        return "masslaw-knowledge-dev.cluster-ro-c6rrtlqu4oqc.us-east-1.neptune.amazonaws.com"
    return ''


def _get_neptune_write_endpoint_for_stage(stage) -> str:
    if stage == 'dev':
        return "masslaw-knowledge-dev.cluster-c6rrtlqu4oqc.us-east-1.neptune.amazonaws.com"
    return ''
