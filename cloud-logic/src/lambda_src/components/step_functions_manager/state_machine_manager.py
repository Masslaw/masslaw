import boto3
import json


class StateMachineManager:
    def __init__(self, state_machine_name: str):
        self.client = boto3.client('stepfunctions')
        self.state_machine_arn = self._get_state_machine_arn(state_machine_name)

    def _get_state_machine_arn(self, state_machine_name: str) -> str:
        response = self.client.list_state_machines()
        for state_machine in response['stateMachines']:
            if state_machine['name'] == state_machine_name:
                return state_machine['stateMachineArn']

        raise ValueError(f'State machine {state_machine_name} not found.')

    def start_execution(self, input_data: dict, name: str = None) -> str:
        params = {
            'stateMachineArn': self.state_machine_arn,
            'input': json.dumps(input_data)
        }

        if name:
            params['name'] = name

        response = self.client.start_execution(**params)
        return response['executionArn']

    def describe_execution(self, execution_arn: str) -> dict:
        response = self.client.describe_execution(
            executionArn=execution_arn
        )
        return response

    def stop_execution(self, execution_arn: str, error: str = "", cause: str = "") -> dict:
        response = self.client.stop_execution(
            executionArn=execution_arn,
            error=error,
            cause=cause
        )
        return response
