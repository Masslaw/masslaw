import json
from datetime import datetime
from decimal import Decimal
from typing import Union


def ensure_dict(d):
    d = isinstance(d, dict) and d or isinstance(d, str) and try_loads(str(d)) or d
    if isinstance(d, dict):
        for key in list(d.keys()):
            d[key] = ensure_dict(d[key])
    return d


def try_loads(d):
    try:
        return json.loads(d)
    except:
        return None


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
    if len(path) < 1:
        d = element
        return d
    if not isinstance(d, dict):
        d = isinstance(d, str) and try_loads(d) or {}
    d[path[0]] = len(path) > 1 and set_at(d.get(path[0], {}), path[1:], element) or element
    return d


def select_keys(d: dict, keys):
    new_dict = {}
    for key in keys:
        if isinstance(key, str): key = [key]
        val = get_from(d, key)
        if val: set_at(new_dict, key, val)
    return new_dict


def remove_not_provided(d: dict):
    new_dict = {}
    for key, value in d.items():
        if isinstance(value, dict):
            new_dict[key] = remove_not_provided(value)
        elif (value is not None) and (not value == ''):
            new_dict[key] = value
    return new_dict


def ensure_flat(d: dict):
    new_dict = {}
    for key, value in d.items():
        if isinstance(value, dict):
            new_dict[key] = json.dumps(value)
        elif isinstance(value, list):
            new_dict[key] = [isinstance(v, dict) and json.dumps(v) or v for v in value]
        else:
            new_dict[key] = value
    return new_dict


def ensure_serializable(val):
    if isinstance(val, dict):
        new_dict = {}
        for key, value in val.items():
            new_dict[key] = ensure_serializable(value)
        return new_dict
    elif isinstance(val, (list, tuple)):
        return [isinstance(v, dict) and ensure_serializable(v) or v for v in val]
    elif isinstance(val, Decimal):
        return float(val)
    elif isinstance(val, datetime):
        return val.isoformat()
    else:
        return val


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
    new_dict = d.copy()
    for key in keys:
        if isinstance(key, str): key = [key]
        new_dict = delete_at(d, key)
    return new_dict


def delete_at(d: dict, path: list):
    parent_path = path[:-1]
    parent_value = get_from(d, parent_path)
    if not parent_value:
        return d
    if not isinstance(parent_value, dict):
        return d
    if path[-1] not in parent_value:
        return d
    del parent_value[path[-1]]
    return set_at(d, parent_path, parent_value)


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
        if not any(isinstance(dict_value, t) for t in validation_value):
            return False
    return True
