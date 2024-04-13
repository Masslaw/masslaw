import os
from openai import OpenAI


def generate_text_embeddings_suitable_for_masslaw_system(text: str):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    response = client.embeddings.create(model='text-embedding-ada-002', input=text)
    embeddings = response.data[0].embedding
    return embeddings
