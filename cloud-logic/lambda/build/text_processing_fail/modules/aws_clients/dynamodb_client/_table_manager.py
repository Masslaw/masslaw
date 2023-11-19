import math
import threading

from text_processing_fail.modules.aws_clients._types import AWSSessionKeys
from text_processing_fail.modules.aws_clients._aws_service_client import AWSServiceClient
from text_processing_fail.modules.dictionary_utils import dictionary_utils


class DynamoDBTableManager(AWSServiceClient):
    def __init__(self, table_name, region_name='us-east-1', session_keys: AWSSessionKeys = None):
        super().__init__(service_name='dynamodb', region_name=region_name, session_keys=session_keys)
        self.table_name = table_name
        self.table = self._resource.Table(self.table_name)
        self.primary_key = self.get_primary_key_name()

    def get_item(self, key, default=None):
        key = self.__ensure_key_object(key)
        response = self.table.get_item(Key=key)
        item = response.get('Item', default)
        item = dictionary_utils.ensure_dict(item)
        return item

    def update_item(self, item_id, data):
        update_expression = "SET " + ", ".join(f"#{k}=:{k}" for k in data)
        expression_attribute_names = {f"#{k}": k for k in data}
        expression_attribute_values = {f":{k}": v for k, v in data.items()}

        self.table.update_item(
            Key=self.__ensure_key_object(item_id),
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )

    def item_exists(self, key):
        return self.get_item(key, None) is not None

    def put_item(self, item):
        try: self.table.put_item(Item=item)
        except Exception as e: raise Exception(f"an error occurred trying to put an item in a dynamodb table \nerror: {e} \nitem: {item}")

    def delete_item(self, key):
        key = self.__ensure_key_object(key)
        self._resource.delete_item(TableName=self.table_name, Key=key)

    def query(self, key_condition_expression, expression_attribute_values):
        response = self._resource.query(TableName=self.table_name, KeyConditionExpression=key_condition_expression, ExpressionAttributeValues=expression_attribute_values)
        return response.get('Items', [])

    def scan(self, filter_expression=None, expression_attribute_values=None):
        response = self._resource.scan(TableName=self.table_name, FilterExpression=filter_expression, ExpressionAttributeValues=expression_attribute_values)
        return response.get('Items', [])

    def batch_get_items(self, keys):
        if len(keys) == 0: return []
        num_keys = len(keys)
        num_blocks = math.ceil(len(keys) / 100)
        block_size = math.floor(num_keys / num_blocks)
        key_blocks = [keys[i:min(i+block_size, len(keys))] for i in range(0, len(keys), block_size)]
        items = []
        item_fetching_threads = [
            threading.Thread(target=lambda block_keys: items.extend(self._batch_get_itmes(block_keys)), args=(_keys,))
            for _keys in key_blocks]
        for t in item_fetching_threads: t.start()
        for t in item_fetching_threads: t.join()
        return items

    def _batch_get_itmes(self, keys):
        keys = [self.__ensure_key_object(key) for key in keys]
        query_data = {self.table_name: {'Keys': keys}}
        items = []
        while len(list(query_data.keys())) > 0:
            response = self._resource.batch_get_item(RequestItems=query_data)
            query_data = response['UnprocessedKeys']
            items.extend(response.get('Responses', {}).get(self.table_name, []))
        items = [dictionary_utils.ensure_dict(item) for item in items]
        return items

    def get_primary_key_name(self):
        response = self.describe_table()
        key_schema = response['Table']['KeySchema']
        return next((key['AttributeName'] for key in key_schema if key['KeyType'] == 'HASH'), None)

    def describe_table(self):
        return self._client.describe_table(TableName=self.table_name)

    def __ensure_key_object(self, key):
        return isinstance(key, dict) and key or self.__primary_key_value_to_obj(key)

    def __primary_key_value_to_obj(self, val):
        return {self.primary_key: val}

    def __prepare_query_params(self, params):
        return (isinstance(params, dict) and 'name' in params and 'value' in params) and params or [{'name': k, 'value': v} for k, v in params.items()]
