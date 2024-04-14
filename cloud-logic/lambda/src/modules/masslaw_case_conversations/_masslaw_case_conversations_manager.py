import json
import os
import secrets
from typing import Tuple

import time
from openai import OpenAI

from src.modules.aws_clients.s3_client import S3BucketManager
from src.modules.dictionary_utils import dictionary_utils
from src.modules.masslaw_case_conversations._masslaw_case_conversations_message_factory import build_prompt
from src.modules.masslaw_cases_config import storage_config
from src.modules.masslaw_cases_config import openai_config

conversations_bucket_manager = S3BucketManager(storage_config.CASES_CONVERSATIONS_BUCKET_ID)


class MasslawCaseConversationsManager:

    def __init__(self, case_instance):
        self.__case_instance = case_instance

    def get_user_case_conversations(self, user_id: str) -> dict:
        user_conversations = self.__case_instance.get_data_property(['users', user_id, 'conversations'], {})
        return user_conversations

    def get_conversation_data(self, user_id: str, conversation_id: str) -> dict:
        user_conversations = self.get_user_case_conversations(user_id)
        conversation_data = user_conversations.get(conversation_id, {})
        return conversation_data

    def set_conversation_data(self, user_id: str, conversation_id: str, new_data: dict):
        user_conversations = self.get_user_case_conversations(user_id)
        user_conversations[conversation_id] = new_data
        self.__case_instance.set_data_property(['users', user_id, 'conversations'], user_conversations)
        self.__case_instance.save_data()

    def start_conversation_as_user(self, user_id: str, conversation_name: str) -> Tuple[str, dict]:
        user_conversations = self.get_user_case_conversations(user_id)
        while True:
            new_conversation_id = str(secrets.token_hex(16))
            if new_conversation_id not in user_conversations: break
        new_conversation_data = {'name': conversation_name, 'creation': str(int(time.time())), 'last_message': str(int(time.time()))}
        self.set_conversation_data(user_id, new_conversation_id, new_conversation_data)
        return new_conversation_id, new_conversation_data

    def get_conversation_content(self, user_id: str, conversation_id: str) -> dict:
        conversation_data = self.get_conversation_data(user_id, conversation_id)
        if not conversation_data: return {}
        conversation_key = f'{self.__case_instance.get_case_id()}/{user_id}/{conversation_id}.json'
        conversation_content = conversations_bucket_manager.get_object(conversation_key) or {}
        conversation_content = dictionary_utils.ensure_dict(conversation_content)
        return conversation_content

    def update_conversation_content(self, user_id: str, conversation_id: str, conversation_content: dict):
        conversation_data = self.get_conversation_data(user_id, conversation_id)
        if not conversation_data: return {}
        conversation_key = f'{self.__case_instance.get_case_id()}/{user_id}/{conversation_id}.json'
        json_data = json.dumps(conversation_content)
        encoded_json_data = json_data.encode('utf-8')
        conversations_bucket_manager.put_object(key=conversation_key, body=encoded_json_data)

    def send_message_to_conversation_as_user(self, user_id: str, conversation_id: str, message_content: str, message_context: str = '') -> dict:
        conversation_data = self.get_conversation_data(user_id, conversation_id)
        if not conversation_data: return {}
        conversation_content = self.get_conversation_content(user_id, conversation_id)
        messages = conversation_content.get('messages', [])
        message_sequence = messages[-10:]
        formatted_message = build_prompt(message_content, message_context)
        message_sequence += [{'role': 'user', 'content': formatted_message}]
        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        response = client.chat.completions.create(model=openai_config.CHATBOT_MODEL, messages=message_sequence)
        response_message = response.choices[0].message
        messages.append({'role': 'user', 'content': message_content})
        conversation_content['messages'] = messages
        messages.append({'role': response_message.role, 'content': response_message.content})
        conversation_content['messages'] = messages
        self.update_conversation_content(user_id, conversation_id, conversation_content)
        conversation_data['last_message'] = str(int(time.time()))
        self.set_conversation_data(user_id, conversation_id, conversation_data)
        return conversation_content
