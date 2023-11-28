import json


def get_from(d: dict, path: list, default=None):
    v = d.copy()
    for key in path:
        if not isinstance(v, dict):
            return default
        v = v.get(key)
        if v is None:
            return default
    return v


def set_at(d: dict, path: list, element):
    if not path:
        return
    if len(path) == 1:
        d[path[0]] = element
        return
    sub_value = d.get(path[0], {})
    if not isinstance(sub_value, dict):
        sub_value = {}
    set_at(sub_value, path[1:], element)
    d[path[0]] = sub_value


def select_keys(d: dict, keys):
    new_dict = {}
    for key in keys:
        if isinstance(key, str): key = [key]
        val = get_from(d, key)
        if val: set_at(new_dict, key, val)
    return new_dict


def remove_not_provided(d: dict):
    keys_to_remove = []
    for key, value in d.items():
        if isinstance(value, dict):
            remove_not_provided(value)
            if not value:
                keys_to_remove.append(key)
        elif value is None or value == '':
            keys_to_remove.append(key)
    for key in keys_to_remove:
        d.pop(key)


def ensure_flat(d: dict):
    for key, value in d.items():
        if isinstance(value, dict):
            d[key] = json.dumps(value)
        elif isinstance(value, list):
            d[key] = [isinstance(v, dict) and json.dumps(v) or v for v in value]
        else:
            d[key] = value


def delete_nested_keys(d: dict, k: str):
    if isinstance(d, dict):
        for key in list(d.keys()):
            if key == k:
                del d[key]
            else:
                delete_nested_keys(d[key], k)
    elif isinstance(d, list):
        for item in d:
            delete_nested_keys(item, k)


def delete_keys(d: dict, keys: list):
    for key in keys:
        if isinstance(key, str): key = [key]
        delete_at(d, key)


def delete_at(d: dict, path: list):
    if not path or len(path) == 0:
        return
    if len(path) == 1:
        if path[0] in d:
            del d[path[0]]
        return
    parent_path = path[:-1]
    parent_value = get_from(d, parent_path)
    if not parent_value or not isinstance(parent_value, dict):
        return
    last_key = path[-1]
    if last_key in parent_value:
        del parent_value[last_key]


def check_structure(d: dict, validation: dict):
    for key in list(validation.keys()):
        validation_value = validation[key]
        dict_value = d.get(key)

        if isinstance(validation_value, dict):
            if not check_structure(dict_value or {}, validation_value):
                return False
            continue

        if not isinstance(validation_value, list):
            validation_value = [validation_value]
        if dict_value is None:
            return None in validation_value
        if not any(isinstance(dict_value, t) for t in validation_value if t is not None):
            return False
    return True


def invert_dict(d: dict):
    return {v: k for k, v in d.items()}
