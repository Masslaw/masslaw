from get_case_file_data.modules.dictionary_utils import dictionary_utils
from get_case_file_data.modules.masslaw_cases_config import access_config


def get_case_data_full_format_from_db_item(item_data, user_id=''):
    base_data = get_case_data_base_format_from_db_item(item_data, user_id)
    data = base_data  # add any additional attributes and data needed apart from the base data
    return data


def get_case_data_base_format_from_db_item(item_data, user_id=''):
    return {
        'case_id': dictionary_utils.get_from(item_data, ['case_id'], ''),
        'title': dictionary_utils.get_from(item_data, ['information', 'title'], ''),
        'description': dictionary_utils.get_from(item_data, ['information', 'description'], ''),
        'num_users': len(dictionary_utils.get_from(item_data, ['users'], {})),
        'num_files': len(dictionary_utils.get_from(item_data, ['files'], [])),
        'creation_time': dictionary_utils.get_from(item_data, ['information', 'creation_time'], -1),
        'last_interaction': dictionary_utils.get_from(item_data, ['information', 'last_modified_time'], -1),
        'access_level': dictionary_utils.get_from(item_data, ['users', user_id, 'access_level'], access_config.CaseAccessEntities.EXTERNAL_CLIENT),
    }


def get_case_file_data_full_format_from_db_item(item_data):
    base_data = get_case_file_data_base_format_from_db_item(item_data)
    data = base_data # add any additional attributes and data needed apart from the base data
    data['description'] = dictionary_utils.get_from(item_data, ['description'], '')
    return data


def get_case_file_data_base_format_from_db_item(item_data):
    return {
        'id': dictionary_utils.get_from(item_data, ['file_id'], ''),
        'name': dictionary_utils.get_from(item_data, ['name'], ''),
        'type': dictionary_utils.get_from(item_data, ['type'], ''),
        'uploaded': dictionary_utils.get_from(item_data, ['upload_time'], ''),
        'modified': dictionary_utils.get_from(item_data, ['last_modified'], ''),
        'languages': dictionary_utils.get_from(item_data, ['languages'], ''),
        'processing': dictionary_utils.get_from(item_data, ['processing', 'stage_information'], {}),
        'case_id': dictionary_utils.get_from(item_data, ['case_id'], {}),
        'description': f'{(description := dictionary_utils.get_from(item_data, ["description"], ""))[:50]}{len(description) > 50 and "..." or ""}',
        'num_annotations': len(dictionary_utils.get_from(item_data, ['annotations'], [])),
    }


def get_case_file_annotations_full_format_from_db_item(item_data):
    return {
        'id': dictionary_utils.get_from(item_data, ['annotation_id'], ''),
        'type': dictionary_utils.get_from(item_data, ['type'], ''),
        'creator': dictionary_utils.get_from(item_data, ['creator'], ''),
        'file_id': dictionary_utils.get_from(item_data, ['file_id'], ''),
        'case_id': dictionary_utils.get_from(item_data, ['case_id'], ''),
        'modified': dictionary_utils.get_from(item_data, ['last_modified'], ''),
        'from_char': dictionary_utils.get_from(item_data, ['from_char'], 0),
        'to_char': dictionary_utils.get_from(item_data, ['to_char'], 0),
        'text': dictionary_utils.get_from(item_data, ['text'], 0),
        'annotated_text': dictionary_utils.get_from(item_data, ['annotated_text'], 0),
        'color': dictionary_utils.get_from(item_data, ['color'], ''),
    }
