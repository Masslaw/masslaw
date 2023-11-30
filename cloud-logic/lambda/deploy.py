import ast
import os
import re
import shutil
from _ast import Module
from typing import Set


def run_build(handler_implementations_dir: str, target_build_dir: str, source_parent: str, base_yaml_file: str):
    build_lambda_handlers(handler_implementations_dir, target_build_dir, source_parent)
    generate_serverless_deployment_yaml(base_yaml_file, target_build_dir)


def build_lambda_handlers(handler_implementations_dir: str, target_build_dir: str, source_parent: str):
    handler_implementations_dir_absolute = os.path.abspath(handler_implementations_dir)
    target_build_dir_absolute = os.path.abspath(target_build_dir)
    source_parent_absolute = os.path.abspath(source_parent)
    source_parent_as_module = format_source_parent(source_parent)
    clear_directory(target_build_dir_absolute)
    init_files = collect_init_files(handler_implementations_dir_absolute)
    print(f"Collected {len(init_files)} handlers.")
    for index, init_file in enumerate(init_files):
        process_handler(init_file, target_build_dir_absolute, source_parent_absolute, source_parent_as_module, index, len(init_files))
    update_progress_bar(len(init_files), len(init_files), "Complete")


def generate_serverless_deployment_yaml(base_yaml_file: str, target_build_dir: str):
    generated_yaml_content = ''
    with open(base_yaml_file, 'r') as f:
        generated_yaml_content += f.read()
    generated_yaml_content += "\n\nfunctions:"
    for handler_package in os.listdir(target_build_dir):
        handler_package_path = os.path.join(target_build_dir, handler_package)
        if not os.path.isdir(handler_package_path): continue
        handler_package_serverless_file = os.path.join(handler_package_path, 'serverless.yml')
        if not os.path.exists(handler_package_serverless_file): continue
        formatted_handler_name = re.sub(r'(?<!^)(?=[A-Z])|_| ', '-', handler_package).lower()
        generated_yaml_content += f"\n  {formatted_handler_name}:\n    handler: {handler_package}.handler\n    package:\n      patterns:\n        - {handler_package}/**"
        with open(handler_package_serverless_file, 'r') as f:
            handler_package_serverless_yaml_content = f.read()
            generated_yaml_content += "\n    " + handler_package_serverless_yaml_content.replace("\n", "\n    ")
    generated_yaml_file = os.path.abspath(os.path.join(target_build_dir, "serverless.yml"))
    with open(generated_yaml_file, 'w+') as f:
        f.write(generated_yaml_content)


def format_source_parent(source_parent: str) -> str:
    return source_parent.strip("./").replace("/", ".")


def clear_directory(directory: str):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


def collect_init_files(directory: str) -> list:
    return [os.path.join(subdir, file) for subdir, _, files in os.walk(directory) for file in files if file == '__init__.py']


def process_handler(init_file: str, target_build_dir: str, source_parent: str, source_parent_as_module: str, index: int, total: int):
    parent_dir_path = os.path.dirname(init_file)
    parent_dir_name = os.path.basename(parent_dir_path)
    update_progress_bar(index, total, parent_dir_name)

    dependencies = collect_script_module_dependencies(init_file)
    handler_build_dir = os.path.join(target_build_dir, parent_dir_name)
    shutil.copytree(parent_dir_path, handler_build_dir, dirs_exist_ok=True)

    copy_dependencies(dependencies, handler_build_dir, source_parent, parent_dir_name)
    update_import_statements(handler_build_dir, source_parent_as_module, parent_dir_name)
    update_progress_bar(index + 1, total, parent_dir_name)


def copy_dependencies(dependencies: Set[str], handler_build_dir: str, source_parent: str, parent_dir_name: str):
    for dep in dependencies:
        rel_path = os.path.relpath(dep, source_parent)
        dest_path = os.path.join(handler_build_dir, rel_path)
        if not os.path.exists(os.path.dirname(dest_path)):
            os.makedirs(os.path.dirname(dest_path))
        if os.path.isdir(dep):
            shutil.copytree(dep, dest_path, dirs_exist_ok=True)
        else:
            shutil.copy(dep, dest_path)


def update_import_statements(handler_build_dir: str, source_parent_as_module: str, parent_dir_name: str):
    for subdir, _, files in os.walk(handler_build_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                content = re.sub(rf"from\s+{re.escape(source_parent_as_module)}", f"from {parent_dir_name}", content)
                with open(file_path, 'w') as f:
                    f.write(content)


def update_progress_bar(progress, total, current_build_name):
    bar_length = 20
    percent = float(progress) / total
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    print(f"\rProgress: [{arrow + spaces}] {int(round(percent * 100))}% Building {current_build_name}", end='', flush=True)


def collect_script_module_dependencies(script_path: str) -> Set[str]:
    script_module_dependencies = set()
    visited_scripts = set()
    iter_stack = [{script_path}]
    while len(iter_stack):
        current_script_set = iter_stack[-1]
        if len(current_script_set) == 0:
            iter_stack.pop()
            continue
        current_script = current_script_set.pop()
        current_script_script_dependencies = collect_script_script_dependencies(current_script)
        current_script_script_dependencies = current_script_script_dependencies - visited_scripts
        iter_stack.append(current_script_script_dependencies)
        script_module = get_module_containing_script(current_script)
        script_module_dependencies.add(script_module)
        visited_scripts.add(current_script)
    return script_module_dependencies


def collect_script_script_dependencies(script_path: str) -> Set[str]:
    with open(script_path, 'r') as file:
        module: Module = ast.parse(file.read())
    imported_scrips = []
    for node in ast.iter_child_nodes(module):
        if isinstance(node, ast.Import):
            imported_scrips.extend(n.name for n in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported_scrips.append(node.module)
    imported_scripts_paths = set()
    for imported_script in imported_scrips:
        if not imported_script: continue
        full_script_path = find_relatively_imported_script_path(script_path, imported_script)
        if not full_script_path: continue
        imported_scripts_paths.add(full_script_path)
    return imported_scripts_paths


def find_relatively_imported_script_path(original_script_path: str, target_module_import_path: str) -> str:
    target_module_import_path = target_module_import_path.replace('.', os.sep)
    target_script_path_as_script = target_module_import_path + '.py'
    target_script_path_as_init = os.path.join(target_module_import_path, '__init__.py')
    original_script_path_parent = os.path.dirname(original_script_path)
    original_script_path_parent_parts = original_script_path_parent.split(os.sep)
    for count in range(len(original_script_path_parent_parts), 0, -1):
        path = "/" + os.path.join(*original_script_path_parent_parts[:count], target_script_path_as_script)
        if os.path.exists(path):
            return path
        path = "/" + os.path.join(*original_script_path_parent_parts[:count], target_script_path_as_init)
        if os.path.exists(path):
            return path


def find_artifact_declaration(artifact_name: str, search_directory: str) -> str:
    for subdir, dirs, files in os.walk(search_directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    if f"class {artifact_name}(" in content or f"def {artifact_name}(" in content:
                        return file_path
    return "Not found"


def get_module_containing_script(script_path: str) -> str:
    directory = os.path.dirname(script_path)
    while directory:
        if os.path.exists(os.path.join(directory, '__init__.py')): return directory
        parent_dir = os.path.dirname(directory)
        if parent_dir == directory: break
        directory = parent_dir
    return None


if __name__ == "__main__":
    handler_implementations_parent_dir = './src/handlers'
    target_build_directory = './build'
    source_parent = './src'
    base_yaml_file = './serverless-base.yml'
    stage = input('stage: ')
    run_build(handler_implementations_parent_dir, target_build_directory, source_parent, base_yaml_file)
    os.system(f"cd build; serverless deploy --stage {stage}")
    shutil.rmtree(target_build_directory)
