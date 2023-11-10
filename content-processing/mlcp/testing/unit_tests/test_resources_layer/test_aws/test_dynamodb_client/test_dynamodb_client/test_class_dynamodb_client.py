import unittest

import boto3
import moto

from resources_layer.aws.dynamodb_client import DynamoDBClient


@moto.mock_dynamodb
class TestClassDynamoDBClient(unittest.TestCase):

    def setUp(self):
        self.table_name = 'test_table'
        self.aws_access_key_id = 'key'
        self.aws_secret_access_key = 'secret'
        self.session_token = 'token'

        self.conn = boto3.resource('dynamodb', region_name='us-east-1')
        self.conn.create_table(
            TableName=self.table_name,
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )

    def test_put_and_get_item(self):
        client = DynamoDBClient(self.table_name, (self.aws_access_key_id, self.aws_secret_access_key, self.session_token))

        test_item = {"id": "123", "name": "test_name"}
        client.put_item(test_item)

        retrieved_item = client.get_item({"id": "123"})
        self.assertEqual(test_item, retrieved_item)

    def test_delete_item(self):
        client = DynamoDBClient(self.table_name, (self.aws_access_key_id, self.aws_secret_access_key, self.session_token))

        test_item = {"id": "456", "name": "another_name"}
        client.put_item(test_item)
        self.assertTrue(client.item_exists({"id": "456"}))

        client.delete_item({"id": "456"})
        self.assertFalse(client.item_exists({"id": "456"}))

    def test_batch_write_items(self):
        client = DynamoDBClient(self.table_name, (self.aws_access_key_id, self.aws_secret_access_key, self.session_token))

        items = [
            {"id": "1", "name": "name_1"},
            {"id": "2", "name": "name_2"},
            {"id": "3", "name": "name_3"},
        ]
        client.batch_write_items(items)

        self.assertTrue(client.item_exists({"id": "1"}))
        self.assertTrue(client.item_exists({"id": "2"}))
        self.assertTrue(client.item_exists({"id": "3"}))
