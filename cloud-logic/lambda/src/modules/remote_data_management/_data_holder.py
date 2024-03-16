from src.modules.dictionary_utils import dictionary_utils


class DataHolder:

    _initialized_items = {}

    def __new__(cls, *args, **kwargs):
        key = (cls, args, tuple(sorted(kwargs.items())))
        if key in cls._initialized_items: return cls._initialized_items[key]
        instance = super().__new__(cls)
        cls._initialized_items[key] = instance
        return instance

    @classmethod
    def reset_cache(cls):
        cls._initialized_items = {}

    def __init__(self, locked_attributes=None):
        self.__data = {}
        self._valid = self.load_data()
        self._updated_attributes = set()
        self._locked_attributes = set(locked_attributes or [])
        self._local = False

    def load_data(self):
        self._updated_attributes = set()

    def lock_attribute(self, attr):
        if attr in self._locked_attributes: return
        self._locked_attributes.add(attr)

    def unlock_attribute(self, attr):
        if attr not in self._locked_attributes: return
        self._locked_attributes.remove(attr)

    def save_data(self):
        self._assert_valid_data()
        self._valid = True

    def get_data_property(self, key, default=None):
        if isinstance(key, str): key = [key]
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
        update_attribute = key and key[0]
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
        dictionary_utils.delete_keys(update_obj, list(self._locked_attributes))
        for key in list(update_obj.keys()):
            self.set_data_property([key], update_obj[key])

    def copy_from(self, other):
        self._set_data(other.get_data_copy())

    def is_valid(self):
        return self._valid

    def delete(self):
        return

    def _set_data(self, new_data):
        self.__data = dictionary_utils.deep_copy(new_data)

    def _get_data(self):
        return dictionary_utils.deep_copy(self.__data)

    def _assert_valid_data(self):
        pass

    def _set_attribute_updated(self, attr):
        self._updated_attributes.add(attr)
