from typing import List

from src.modules.masslaw_cases_objects import MasslawCaseFileInstance
from src.modules.masslaw_cloud_configurations import get_configuration_value
from src.modules.masslaw_cloud_configurations import configuration_keys
from src.modules.mlcp_management import MLCPSubmission
from src.modules.aws_clients.batch_client import batch_management


def submit_knowledge_extraction_job(file_instance: MasslawCaseFileInstance, stage='prod') -> List[str]:
    languages = file_instance.get_data_property(["languages"], ['eng'])
    supported_languages = get_configuration_value(configuration_keys.SUPPORTED_MLCP_KNOWLEDGE_EXTRACTION_LANGUAGES)
    languages_to_process = list(set(languages) & set(supported_languages))
    processing_job_ids = []
    for language in languages_to_process:
        processing_job_id = _submit_knowledge_extraction_job_for_language(file_instance, language, stage)
        processing_job_ids.append(processing_job_id)
    return processing_job_ids


def _submit_knowledge_extraction_job_for_language(file_instance: MasslawCaseFileInstance, language: str, stage='prod'):
    file_id = file_instance.get_file_id()
    case_id = file_instance.get_data_property(['case_id'])

    text_file_key = f'{file_id}/client_exposed/extracted_text/plain_text.txt'
    text_file_name = f'{file_id}.txt'

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
        "name": "extract_knowledge",
        "params": {
            "files_data": [
                {
                    "file_name": text_file_name,
                    "languages": [language],
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
    mlcp_job.name = f'mlcp-knowledge-extraction-{language}-{stage}'
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
