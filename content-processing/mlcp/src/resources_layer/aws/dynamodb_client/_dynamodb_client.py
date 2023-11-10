import boto3

from resources_layer.aws._types import AWSSessionKeys
from resources_layer.aws.aws_service_client import AWSServiceClient


class DynamoDBClient(AWSServiceClient):
    def __init__(self, table_name, aws_keys: AWSSessionKeys, region_name='us-east-1'):
        super().__init__(service_name='dynamodb', region_name=region_name, session_keys=aws_keys)
        self.table_name = table_name
        self.table = self._resource.Table(table_name)
        self.primary_key = self.get_primary_key_name()

    def describe_table(self):
        return self._client.describe_table(TableName=self.table_name)

    def put_item(self, item, safe=False):
        if safe:
            saved_item = self.get_item(item.get(self.primary_key)) or {}
            saved_item.update(item)
            item = saved_item
        self.table.put_item(Item=item)

    def get_item(self, key=None):
        response = self.table.get_item(Key=self.__ensure_key_object(key))
        item = response.get('Item') or self.get_empty_item()
        return item

    def get_items_by_attribute(self, key: dict):
        attribute_name = list(key.keys())[0]
        secondary_key_value = key[attribute_name]

        response = self.table.query(IndexName=f'{attribute_name}-index', KeyConditionExpression=f'{attribute_name} = :{attribute_name}',
            ExpressionAttributeValues={f':{attribute_name}': secondary_key_value})

        return response['Count'] > 0 and response['Items'] or [None]

    def item_exists(self, key):
        return 'Item' in self.table.get_item(Key=self.__ensure_key_object(key))

    def delete_item(self, key):
        self.table.delete_item(Key=self.__ensure_key_object(key))

    def batch_write_items(self, items):
        with self.table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)

    def batch_delete_items(self, items):
        with self.table.batch_writer() as batch:
            for item in items:
                batch.delete_item(Key=item)

    def batch_get_items(self, keys):
        response = self.table.batch_get_item(RequestItems={self.table_name: {'Keys': [self.__ensure_key_object(k) for k in keys]}})

        items = response['Responses'][self.table_name]
        while 'UnprocessedKeys' in response:
            response = self.table.batch_get_item(RequestItems=response['UnprocessedKeys'])
            items.extend(response['Responses'][self.table_name])

        return items

    def get_primary_key_name(self):
        response = self.describe_table()
        key_schema = response['Table']['KeySchema']

        for key in key_schema:
            if key['KeyType'] == 'HASH':
                return key['AttributeName']

    def get_empty_item(self):
        response = self.describe_table()
        schema = response['Table']['AttributeDefinitions']
        attribute_names = [attr['AttributeName'] for attr in schema]
        empty_item = {name: None for name in attribute_names}
        return empty_item

    def __ensure_key_object(self, key):
        return isinstance(key, dict) and key or self.__primary_key_value_to_obj(key)

    def __primary_key_value_to_obj(self, val):
        return {self.primary_key: val}
