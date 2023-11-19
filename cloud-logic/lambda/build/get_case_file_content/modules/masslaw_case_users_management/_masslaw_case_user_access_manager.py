from get_case_file_content.modules.masslaw_cases_objects import MasslawCaseInstance
from get_case_file_content.modules.masslaw_cases_config import access_config
from get_case_file_content.modules.dictionary_utils import dictionary_utils
from get_case_file_content.modules.masslaw_users_objects import MasslawUserInstance


class MasslawCaseUserAccessManager:
    def __init__(self, case_instance: MasslawCaseInstance):
        self.__case_instance = case_instance

    def get_formatted_case_instance_for_user(self, user_id):
        access_level = self.determine_user_access_level(user_id=user_id)
        formatted_case_instance = self.get_formatted_case_instance_for_entity(access_level)

        user_access_files = self.get_user_access_files(user_id)
        formatted_case_instance.set_data_property(['files'], user_access_files)
        return formatted_case_instance

    def get_formatted_case_instance_for_entity(self, access_level):
        formatted_case_instance = UserReadFormattedCaseInstance(self.__case_instance.get_case_id())
        entity_permitted_data_keys = self.get_permitted_keys_for_access(access_config.AccessActions.READ, access_level)
        formatted_case_instance.keep_keys(entity_permitted_data_keys)
        return formatted_case_instance

    def update_data_as_user(self, user_id, update_obj):
        access_level = self.determine_user_access_level(user_id=user_id)
        self.update_data_as_entity(access_level, update_obj)

    def update_data_as_entity(self, access_level, update_obj):
        entity_permitted_data_keys = self.get_permitted_keys_for_access(access_config.AccessActions.EDIT, access_level)
        update_obj = dictionary_utils.select_keys(update_obj, entity_permitted_data_keys)
        self.__case_instance.update_data(update_obj)

    def set_case_user_permissions_as_user(self, case_user_id, case_user_permission_level, case_user_restrictions):
        user_access_level = self.determine_user_access_level(case_user_id)
        self.set_case_user_permissions_as_entity(user_access_level, case_user_id, case_user_permission_level, case_user_restrictions)

    def set_case_user_permissions_as_entity(self, as_entity, case_user_id, case_user_permission_level, case_user_restrictions):
        case_users = self.__case_instance.get_data_property('users')
        case_users = isinstance(case_users, dict) and case_users or {}
        if case_user_id in case_users:
            user_access_data = case_users.get(case_user_id, {})
            level = user_access_data.get('access_level')
            if level == access_config.CaseAccessEntities.OWNER_CLIENT:
                # if the user that's requested to change is the owner of the case, return and block the change
                return False
            if level == access_config.CaseAccessEntities.MANAGER_CLIENT and as_entity not in [access_config.CaseAccessEntities.OWNER_CLIENT]:
                # if the user that's requested to change is a manager of the case, only the owner can change
                return False

        self.set_case_user_permissions(case_user_id, case_user_permission_level, case_user_restrictions)

        return True

    def set_case_user_permissions(self, case_user_id, case_user_permission_level, case_user_restrictions):
        self.__case_instance.set_data_property(['users', case_user_id], {'access_level': case_user_permission_level, 'access_restrictions': case_user_restrictions, })

        user_instance = MasslawUserInstance(case_user_id)
        user_instance.set_data_property(['cases', self.__case_instance.get_case_id()], {'access_level': case_user_permission_level})

        user_instance.save_data()

    def get_user_access_files(self, user_id):
        access_level = self.determine_user_access_level(user_id)
        if access_level in [access_config.CaseAccessEntities.OWNER_CLIENT, access_config.CaseAccessEntities.MANAGER_CLIENT]:
            all_files = self.__case_instance.get_data_property(['files'], [])
            return all_files
        if access_level in [access_config.CaseAccessEntities.EXTERNAL_CLIENT]:
            return []
        access_restrictions = self.get_user_access_restrictions(user_id)
        access_files = access_restrictions.get('access_files', [])
        return access_files

    def determine_can_upload_file(self, user_id):
        user_access_level = self.determine_user_access_level(user_id)
        if user_access_level in [access_config.CaseAccessEntities.OWNER_CLIENT, access_config.CaseAccessEntities.MANAGER_CLIENT]:
            return True
        elif user_access_level in [access_config.CaseAccessEntities.EDITOR_CLIENT]:
            access_restrictions = self.get_user_access_restrictions(user_id=user_id)
            access_files = access_restrictions.get('access_files')
            access_files = isinstance(access_files, dict) and access_files or {}
            can_upload = access_restrictions.get('can_upload')
            return len(access_files.keys()) and can_upload != 'false'
        return False

    def get_permitted_keys_for_access(self, for_action, as_entity):
        return dictionary_utils.get_from(access_config.ACCESS_PERMITTED_KEYS, [for_action, as_entity])

    def get_user_access_restrictions(self, user_id):
        return self.__case_instance.get_data_property(['users', user_id, 'access_restrictions'], {})

    def get_user_access_level_name(self, user_id):
        return self.determine_user_access_level(user_id=user_id)

    def determine_user_access_level(self, user_id):
        return self.__case_instance.get_data_property(['users', user_id, 'access_level'], access_config.CaseAccessEntities.EXTERNAL_CLIENT)


class UserReadFormattedCaseInstance(MasslawCaseInstance):
    def __init__(self, case_id: str):
        MasslawCaseInstance.__init__(self, case_id)

    def save_data(self):
        pass  # do nothing - data in a read only formatted case instance cannot be saved

    def _assert_valid_data(self):
        pass  # do nothing - we don't assert the structure of a read only formatted case instance
