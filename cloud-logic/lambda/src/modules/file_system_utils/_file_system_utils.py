import os
import re
import shutil


def get_file_type(path: str) -> str:
    _, file_type = os.path.splitext(path)
    return file_type


def get_file_name(path: str, remove_extention: bool = False) -> str:
    file_name, _ = os.path.splitext(os.path.basename(path))
    if remove_extention: file_name = file_name.replace(get_file_type(path), '')
    return file_name


def get_local_directory() -> str:
    return os.getcwd()


def join_paths(*args, **kwargs) -> str:
    return os.path.join(*args, **kwargs)


def abs_path(path: str) -> str:
    return os.path.abspath(path)


def is_file(path: str) -> bool:
    return os.path.isfile(path)


def is_dir(path: str) -> bool:
    return os.path.isdir(path)


def list_dir(path: str) -> list:
    return os.listdir(path)


def make_dir(path: str, override: bool = True):
    if is_dir(path):
        if (override):
            remove_dir(path)
        else:
            return
    os.makedirs(path)


def remove_dir(path: str):
    if is_file(path):
        remove_file(path)
        return
    for file in list_dir(path):
        remove_dir(join_paths(path, file))
    os.rmdir(path)


def remove_file(path: str):
    os.remove(path)


def copy_file(src_path: str, dst_path: str):
    shutil.copy(src_path, dst_path)


def copy_files(src_path: str, dst_path: str):
    for file in list_dir(src_path):
        file_path = join_paths(src_path, file)
        output_path = join_paths(dst_path, file)
        copy_file(file_path, output_path)


def get_parent_dir(path: str) -> str:
    return os.path.dirname(path)


def split_path(path) -> list:
    dirs = []
    while True:
        path, directory = os.path.split(path)
        if directory:
            dirs.insert(0, directory)
        else:
            if path:
                dirs.insert(0, path)
            break
    return dirs


def get_size(path: str) -> int:
    return os.path.getsize(path)


def get_modified_time(path: str) -> float:
    return os.path.getmtime(path)


def get_accessed_time(path: str) -> float:
    return os.path.getatime(path)


def get_created_time(path: str) -> float:
    return os.path.getctime(path)


def read_file(path: str) -> str:
    with open(path, 'r') as f:
        return f.read()


def write_file(path: str, contents):
    with open(path, 'w') as f:
        f.write(contents)


def search_file(path: str, search_string: str) -> bool:
    with open(path, 'r') as f:
        contents = f.read()
        if re.search(search_string, contents):
            return True
        else:
            return False


def replace_in_file(path: str, search_string: str, replace_string: str):
    with open(path, 'r') as f:
        contents = f.read()
    with open(path, 'w') as f:
        f.write(re.sub(search_string, replace_string, contents))


def get_relative_path(path: str, base_path: str) -> str:
    return os.path.relpath(path, base_path)


def get_common_path(path_1: str, path_2: str) -> str:
    return os.path.commonpath([path_1, path_2])


def rename_file(src_path: str, dst_path: str):
    os.rename(src_path, dst_path)


def move_file(src_path: str, dst_path: str):
    shutil.move(src_path, dst_path)


def get_human_readable_size(size_in_bytes: float) -> str:
    for unit in ['bytes', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} TB"


def get_next(dir: str = "", pattern: str = "") -> str:
    c = 0
    while True:
        path = join_paths(dir, f"{(c := c + 1)}_{pattern}")
        if not is_file(path): break
    return path


def get_nested_files(directory, file_type) -> list:
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if get_file_type(filename).replace('.', '') == file_type.replace('.', ''):
                files.append(os.path.join(root, filename))
    return files


def get_parent_path(path, folder) -> str:
    new_path = ""
    for p in split_path(path):
        if p == folder:
            return new_path
        new_path = join_paths(new_path, p)
    raise ValueError(f"Folder '{folder}' not found in path '{path}'.")


def get_all_files_in_directory(dir_path) -> list:
    if not os.path.exists(dir_path):
        return []
    if os.path.isfile(dir_path):
        return [dir_path]
    file_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


def filter_directories_for_types(directories, file_types) -> list:
    file_types = [ft if ft.startswith('.') else '.' + ft for ft in file_types]
    return [file for file in directories if any(file.endswith(ft) for ft in file_types)]


def clear_directory(directory: str):
    if is_dir(directory):
        remove_dir(directory)
    make_dir(directory)
