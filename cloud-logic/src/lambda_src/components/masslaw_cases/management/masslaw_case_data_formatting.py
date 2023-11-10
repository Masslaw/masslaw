from ..config.access_config import CaseAccessEntities
from ...util import json_utils


def get_case_data_full_format_from_db_item(item_data, user_id=''):
    base_data = get_case_data_base_format_from_db_item(item_data, user_id)
    data = base_data # add any additional attributes and data needed apart from the base data
    return data


def get_case_data_base_format_from_db_item(item_data, user_id=''):
    return {
        'case_id': json_utils.get_from(item_data, ['case_id'], ''),
        'title': json_utils.get_from(item_data, ['information', 'title'], ''),
        'description': json_utils.get_from(item_data, ['information', 'description'], ''),
        'num_users': len(json_utils.get_from(item_data, ['users'], {})),
        'num_files': len(json_utils.get_from(item_data, ['files'], [])),
        'creation_time': json_utils.get_from(item_data, ['information', 'creation_time'], -1),
        'last_interaction': json_utils.get_from(item_data, ['information', 'last_modified_time'], -1),
        'access_level': json_utils.get_from(item_data, ['users', user_id, 'access_level'], CaseAccessEntities.EXTERNAL_CLIENT),
    }


def get_case_file_data_full_format_from_db_item(item_data):
    base_data = get_case_file_data_base_format_from_db_item(item_data)
    data = base_data # add any additional attributes and data needed apart from the base data
    data['description'] = json_utils.get_from(item_data, ['description'], '')
    return data


def get_case_file_data_base_format_from_db_item(item_data):
    return {
        'id': json_utils.get_from(item_data, ['file_id'], ''),
        'name': json_utils.get_from(item_data, ['name'], ''),
        'type': json_utils.get_from(item_data, ['type'], ''),
        'uploaded': json_utils.get_from(item_data, ['upload_time'], ''),
        'modified': json_utils.get_from(item_data, ['last_modified'], ''),
        'languages': json_utils.get_from(item_data, ['languages'], ''),
        'processing': json_utils.get_from(item_data, ['processing', 'stage_information'], {}),
        'case_id': json_utils.get_from(item_data, ['case_id'], {}),
        'description': f'{(description := json_utils.get_from(item_data, ["description"], ""))[:50]}{len(description) > 50 and "..." or ""}',
        'num_annotations': len(json_utils.get_from(item_data, ['annotations'], [])),
    }


def get_case_file_annotations_full_format_from_db_item(item_data):
    return {
        'id': json_utils.get_from(item_data, ['annotation_id'], ''),
        'type': json_utils.get_from(item_data, ['type'], ''),
        'creator': json_utils.get_from(item_data, ['creator'], ''),
        'file_id': json_utils.get_from(item_data, ['file_id'], ''),
        'case_id': json_utils.get_from(item_data, ['case_id'], ''),
        'modified': json_utils.get_from(item_data, ['last_modified'], ''),
        'from_char': json_utils.get_from(item_data, ['from_char'], 0),
        'to_char': json_utils.get_from(item_data, ['to_char'], 0),
        'text': json_utils.get_from(item_data, ['text'], 0),
        'annotated_text': json_utils.get_from(item_data, ['annotated_text'], 0),
        'color': json_utils.get_from(item_data, ['color'], ''),
    }
