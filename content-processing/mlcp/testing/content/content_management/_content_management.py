import os
import random


def get_content_folder(folder_local_path):
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'content_repository', folder_local_path)


def get_random_file(folder_local_path):
    parent_path = get_content_folder(folder_local_path)
    return os.path.join(parent_path, random.choice(os.listdir(parent_path)))


def get_all_files(folder_local_path):
    parent_path = get_content_folder(folder_local_path)
    return [os.path.join(parent_path, f) for f in os.listdir(parent_path)]


def get_file_path(folder_local_path, file_name):
    return os.path.join(get_content_folder(folder_local_path), file_name)
