import secrets
import time

from src.modules.masslaw_case_users_management import MasslawCaseUserAccessManager
from src.modules.masslaw_cases_config import access_config
from src.modules.masslaw_cases_objects import MasslawCaseInstance


def create_a_new_case(creator_user_id, case_creation_data):
    case_instance = None
    creation_success = False
    while not creation_success:
        case_id = secrets.token_hex(16)
        case_instance = MasslawCaseInstance(case_id)
        creation_success = not case_instance.is_valid()

    now = str(int(time.time()))
    case_instance.update_data({
        'information': {
            'title': case_creation_data.get('title', ''),
            'description': case_creation_data.get('description', ''),
            'last_modified_time': now,
            'creation_time': now
        },
        'languages': case_creation_data.get('languages', ['eng']),
        'users': {},
        'content': {},
        'files': {}
    })

    case_user_access_manager = MasslawCaseUserAccessManager(case_instance)
    case_user_access_manager.set_case_user_permissions(
        creator_user_id,
        access_config.CaseAccessEntities.OWNER_CLIENT,
        {
            'files': {
                'allowed_paths': [[]],  # all hierarchy
                'prohibited_paths': [],  # no paths
            }
        }
    )
    return case_instance
