from text_extraction_fail.modules.dictionary_utils import dictionary_utils


class DataHolder:
    def __init__(self, locked_attributes=None):
        self.__data = {}
        self._valid = self.load_data()
        self._updated_attributes = []
        self._locked_attributes = locked_attributes or []

    def load_data(self):
        self._updated_attributes = []

    def lock_attribute(self, attr):
        if attr in self._locked_attributes: return
        self._locked_attributes.append(attr)

    def unlock_attribute(self, attr):
        if attr not in self._locked_attributes: return
        self._locked_attributes.remove(attr)

    def save_data(self):
        self._assert_valid_data()
        self._valid = True

    def get_data_property(self, key, default=None):
        if isinstance(key, str):
            key = [key]
        val = dictionary_utils.get_from(self._get_data(), key, default)
        return val

    def get_data_copy(self):
        return self._get_data()

    def get_data_properties(self, keys):
        return dictionary_utils.select_keys(self._get_data(), keys)

    def delete_data_properties(self, keys):
        data = self._get_data()
        dictionary_utils.delete_keys(data, keys)
        self._set_data(data)

    def delete_data_property(self, key):
        data = self._get_data()
        data = dictionary_utils.delete_at(data, key)
        self._set_data(data)

    def keep_keys(self, keys):
        data = self._get_data()
        data = dictionary_utils.select_keys(data, keys)
        self._set_data(data)

    def set_data_property(self, key: list, value):
        if isinstance(key, str): key = [key]
        update_attribute = len(key) and key[0]
        if update_attribute:
            if update_attribute in self._locked_attributes: return
            self._set_attribute_updated(update_attribute)
        data = self._get_data()
        dictionary_utils.set_at(data, key, value)
        self._set_data(data)

    def update_data(self, update_obj, create_new_keys=True):
        if not create_new_keys:
            existing_keys = list(self.get_data_copy().keys())
            update_obj = dictionary_utils.select_keys(update_obj, existing_keys)
        dictionary_utils.delete_keys(update_obj, self._locked_attributes)
        for key in list(update_obj.keys()):
            self.set_data_property([key], update_obj[key])

    def copy_from(self, other):
        self._set_data(other.get_data_copy())

    def is_valid(self):
        return self._valid

    def delete(self):
        return

    def _set_data(self, new_data):
        self.__data = new_data.copy()

    def _get_data(self):
        return self.__data.copy()

    def _assert_valid_data(self):
        pass

    def _set_attribute_updated(self, attr):
        if attr in self._updated_attributes: return
        self._updated_attributes.append(attr)
