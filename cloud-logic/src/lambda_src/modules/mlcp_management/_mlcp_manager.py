import json

from lambda_src.modules.aws_clients.batch_client import BatchJob


class MLCPInstance:
    def __init__(self, stage='prod'):
        self.stage = stage
        self.env_variables = []
        self.process_configuration = {}

    def get_job(self) -> BatchJob:
        self.add_env_variable('mlcp_process_configuration', json.dumps(self.process_configuration))
        job = BatchJob()
        job.name = f"mlcp-{self.stage}"
        job.definition = f"mlcp-{self.stage}"
        job.share_identifier = None
        job.env_variables = self.env_variables
        return job

    def add_env_variable(self, name, value):
        self.env_variables.append({
            'name': name,
            'value': value
        })

    def add_action(self, action: dict):
        self.process_configuration['actions'] = self.process_configuration.get('actions', []) + [action]