from typing import Iterable
from typing import List
from typing import Type


def force_element_in_index_path(lst: List, index_path: List[int], element: any, default: Type = None):
    if len(index_path) == 0: return
    if len(index_path) == 1:
        force_element_in_list_index(lst, index_path[0], element, default)
        return
    hierarchy_level = get_element_at(lst, index_path[0], [])
    if not isinstance(hierarchy_level, List): hierarchy_level = []
    force_element_in_index_path(hierarchy_level, index_path[1:], element, default)
    force_element_in_list_index(lst, index_path[0], hierarchy_level, default)


def force_element_in_list_index(lst: List, idx: int, e: any, default: Type = None):
    lst.extend([None if default is None else default() for _ in range(idx - len(lst) + 1)])
    lst[idx] = e


def set_list_length(lst: List, length: int, default: Type = None):
    lst = lst.copy()
    lst.extend([None if default is None else default() for _ in range(length - len(lst))])
    return lst[:length]


def get_element_at(lst: List, idx: int, default: any = None):
    if idx >= len(lst): return default
    return lst[idx]


def merge_mergeable(lst: List, mergeable: callable, merge: callable):
    i = 0
    while i < len(lst):
        for j in range(i + 1, len(lst)):
            if not mergeable(lst[i], lst[j]): continue
            lst[i] = merge(lst[i], lst[j])
            del lst[j]
            break
        else:
            i += 1
