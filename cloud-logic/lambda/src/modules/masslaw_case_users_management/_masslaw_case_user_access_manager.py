from src.modules.masslaw_cases_objects import MasslawCaseInstance
from src.modules.masslaw_cases_config import access_config
from src.modules.dictionary_utils import dictionary_utils
from src.modules.masslaw_users_objects import MasslawUserInstance


class MasslawCaseUserAccessManager:
    def __init__(self, case_instance: MasslawCaseInstance):
        self.__case_instance = case_instance

    def get_formatted_case_instance_for_user(self, user_id) -> 'UserReadFormattedCaseInstance':
        access_level = self.determine_user_access_level(user_id=user_id)
        formatted_case_instance = self.get_formatted_case_instance_for_entity(access_level)
        accessible_hierarchy = self.get_user_accessible_case_content_hierarchy(user_id)
        formatted_case_instance.set_data_property(['content'], accessible_hierarchy)
        return formatted_case_instance

    def get_formatted_case_instance_for_entity(self, access_level) -> 'UserReadFormattedCaseInstance':
        formatted_case_instance = UserReadFormattedCaseInstance(self.__case_instance.get_case_id())
        entity_permitted_data_keys = self.get_permitted_keys_for_access(access_config.AccessActions.READ, access_level)
        formatted_case_instance.keep_keys(entity_permitted_data_keys)
        return formatted_case_instance

    def set_case_user_permissions_as_user(self, as_user_id, case_user_id, case_user_access_level, case_access_policy):
        user_access_level = self.determine_user_access_level(as_user_id)
        self.set_case_user_permissions_as_entity(user_access_level, case_user_id, case_user_access_level, case_access_policy)

    def set_case_user_permissions_as_entity(self, as_entity, case_user_id, case_user_access_level, case_access_policy=None):
        access_level = self.determine_user_access_level(case_user_id)
        case_access_policy = case_access_policy or self.get_user_access_policy(case_user_id)
        if access_level == access_config.CaseAccessEntities.OWNER_CLIENT: return False # if the user that's requested to change is the owner of the case, return and block the change
        if access_level == access_config.CaseAccessEntities.MANAGER_CLIENT and as_entity not in [access_config.CaseAccessEntities.OWNER_CLIENT]: return False # if the user that's requested to be changed is a manager of the case, only the owner can change
        self.apply_hardcoded_policy_for_entity(access_level, case_access_policy)
        self.set_case_user_permissions(case_user_id, case_user_access_level, case_access_policy)
        return True

    def set_case_user_permissions(self, case_user_id, case_user_access_level, case_user_access_policy):
        self.__case_instance.set_data_property(['users', case_user_id], {'access_level': case_user_access_level, 'access_policy': case_user_access_policy, })
        user_instance = MasslawUserInstance(case_user_id)
        user_instance.set_data_property(['cases', self.__case_instance.get_case_id()], {'access_level': case_user_access_level})
        user_instance.save_data()

    def get_user_accessible_files(self, user_id):
        access_level = self.determine_user_access_level(user_id)
        if access_level in [access_config.CaseAccessEntities.EXTERNAL_CLIENT]: return []
        accessible_hierarchy = self.get_user_accessible_case_content_hierarchy(user_id)
        accessible_files = self.collect_case_files_in_hierarchy(accessible_hierarchy)
        return accessible_files

    def get_user_accessible_case_content_hierarchy(self, user_id):
        access_level = self.determine_user_access_level(user_id)
        if access_level in [access_config.CaseAccessEntities.EXTERNAL_CLIENT]: return {}
        access_policy = self.get_user_access_policy(user_id)
        accessible_hierarchy = self.get_case_content_hierarchy_for_access_policy(access_policy)
        return accessible_hierarchy

    def get_case_content_hierarchy_for_access_policy(self, access_policy):
        case_content_hierarchy = self.__case_instance.get_data_property(['content'], {})
        accessible_hierarchy = self.select_accessible_from_dictionary_hierarchy(access_policy, case_content_hierarchy)
        return accessible_hierarchy

    def check_content_path_accessible_by_access_policy(self, access_policy, content_path):
        case_content_hierarchy = self.__case_instance.get_data_property(['content'], {})
        dictionary_utils.set_at(case_content_hierarchy, content_path, {})
        accessible_hierarchy = self.select_accessible_from_dictionary_hierarchy(access_policy, case_content_hierarchy)
        path_accessible = dictionary_utils.has_path(accessible_hierarchy, content_path)
        return path_accessible

    def select_accessible_from_dictionary_hierarchy(self, access_policy, dictionary):
        files_access_policy = access_policy.get('files', {})
        allowed_paths = files_access_policy.get('allowed_paths', [])
        prohibited_paths = files_access_policy.get('prohibited_paths', [])
        accessible_hierarchy = dictionary_utils.select_keys(dictionary, allowed_paths)
        dictionary_utils.delete_keys(accessible_hierarchy, prohibited_paths)
        return accessible_hierarchy

    def determine_can_upload_file(self, user_id, to_path):
        user_access_level = self.determine_user_access_level(user_id)
        if user_access_level in [access_config.CaseAccessEntities.OWNER_CLIENT, access_config.CaseAccessEntities.MANAGER_CLIENT]:
            return True
        elif user_access_level in [access_config.CaseAccessEntities.EDITOR_CLIENT]:
            access_policy = self.get_user_access_policy(user_id)
            can_upload = self.check_content_path_accessible_by_access_policy(access_policy, to_path)
            return can_upload
        return False

    def apply_hardcoded_policy_for_entity(self, entity, policy):
        hardcoded_policy_updates = access_config.HARD_CODED_POLICIES[entity] or []
        for policy_update_path, policy_update_value in hardcoded_policy_updates:
            dictionary_utils.set_at(policy, policy_update_path, policy_update_value)

    def get_permitted_keys_for_access(self, for_action, as_entity):
        keys = dictionary_utils.get_from(access_config.ACCESS_PERMITTED_KEYS, [for_action, as_entity])
        return keys

    def get_user_access_policy(self, user_id):
        access_level = self.determine_user_access_level(user_id)
        access_policy = self.__case_instance.get_data_property(['users', user_id, 'access_policy'], {})
        self.apply_hardcoded_policy_for_entity(access_level, access_policy)
        return access_policy

    def get_user_access_level_name(self, user_id):
        access_level = self.determine_user_access_level(user_id=user_id)
        return access_level

    def determine_user_access_level(self, user_id):
        access_level = self.__case_instance.get_data_property(['users', user_id, 'access_level'], access_config.CaseAccessEntities.EXTERNAL_CLIENT)
        return access_level

    def collect_case_files_in_hierarchy(self, content_hierarchy):
        all_files = [item_data for item_name, item_data in dictionary_utils.iterate_nested_items(content_hierarchy) if isinstance(item_data, str)]
        return all_files


class UserReadFormattedCaseInstance(MasslawCaseInstance):
    def __init__(self, case_id: str):
        MasslawCaseInstance.__init__(self, case_id)

    def save_data(self):
        pass  # do nothing - data in a read only formatted case instance cannot be saved

    def _assert_valid_data(self):
        pass  # do nothing - we don't assert the structure of a read only formatted case instance
