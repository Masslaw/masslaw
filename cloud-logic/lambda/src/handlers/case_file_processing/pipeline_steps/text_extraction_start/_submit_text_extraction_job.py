from typing import List

from src.modules.masslaw_cases_objects import MasslawCaseFileInstance
from src.modules.mlcp_management import MLCPSubmission
from src.modules.aws_clients.batch_client import batch_management


def submit_text_extraction_job(file_instance: MasslawCaseFileInstance, stage='prod') -> List[str]:
    file_id = file_instance.get_file_id()
    case_id = file_instance.get_data_property(['case_id'])
    file_type = file_instance.get_data_property(["type"])
    languages = file_instance.get_data_property(["languages"], ['eng'])

    file_key = f'{file_id}/raw.{file_type}'
    file_name = f'{file_id}.{file_type}'

    mlcp = MLCPSubmission(stage=stage)
    mlcp.add_action({"name": "s3_download", "params": {"bucket": "masslaw-cases-content", "files_data": [{"key": file_key, "save_as": file_name}]}, "required": "True"})
    mlcp.add_action({"name": "process_files", "params": {"files_data": [{"file_name": file_name, "languages": languages, "case_id": case_id, "file_id": case_id, "extracted_text_output_dir": "extracted_text", "assets_output_dir": "processed_assets", "converted_file_output_dir": "converted_file"}]},
        "required": "True"})
    mlcp.add_action({"name": "s3_upload", "params": {"bucket": "masslaw-cases-content",
        "files_data": [{"key": f"{file_id}/client_exposed/extracted_text", "saved_as": "extracted_text"}, {"key": f"{file_id}/client_exposed/processed_assets", "saved_as": "processed_assets"}, {"key": f"{file_id}/client_exposed/converted_file", "saved_as": "converted_file"}]}, "required": "True"})

    mlcp_job = mlcp.get_job()
    mlcp_job.name = f'mlcp-text-extraction-{stage}'
    mlcp_job.definition = f'mlcp-text-extraction-{stage}'
    mlcp_job.queue = f'mlcp-text-extraction-queue-{stage}'

    processing_job_id = batch_management.submit_job(mlcp_job)

    return [processing_job_id]
