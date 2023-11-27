import json
import os
import spacy

scripts_dir = os.path.dirname(os.path.realpath(__file__))
models_config_file = os.path.join(scripts_dir, '_models_config.json')

with open(models_config_file, 'r') as f: models_config = json.load(f)


def load_spacy_model_for_language(language: str) -> spacy.language.Language | None:
    model_name = models_config.get(language)
    if not model_name: return None
    model = spacy.load(model_name)
    return model
