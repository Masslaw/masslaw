import os
from openai import OpenAI
from src.modules.masslaw_cases_config import openai_config


def generate_text_embeddings_suitable_for_masslaw_system(text: str):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    response = client.embeddings.create(model=openai_config.EMBEDDINGS_MODEL, input=text)
    embeddings = response.data[0].embedding
    return embeddings
