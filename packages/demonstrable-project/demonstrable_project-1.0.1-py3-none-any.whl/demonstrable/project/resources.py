import importlib.resources
import shutil
from importlib.abc import Traversable

from demonstrable.exception import ConfigurationError

import demonstrable.project
from demonstrable.project.templating import update_pyproject_fields, update_readme_fields


def recursive_traversal(directory: Traversable):
    """Recursively traverse a Traversable directory and yield all files."""
    for item in directory.iterdir():
        if item.is_dir():
            yield from recursive_traversal(item)
        elif item.is_file():
            yield item


def emplace_project(project_directory, name, description):
    package_data_dirpath = importlib.resources.files(demonstrable.project.package_data)
    project_template_dirpath = package_data_dirpath / "new_project"
    # Check that none of the files that will be copied already exist
    # Use recent Python 3.12 import resources API to recursively find all
    # files in the package_data_dirpath/new_project directory and check
    # if they exist in the project_directory
    existing_files = []
    for filepath in recursive_traversal(project_template_dirpath):
        relative_path = filepath.relative_to(project_template_dirpath)
        target_filepath = project_directory / relative_path
        if target_filepath.exists():
            existing_files.append(target_filepath)
    if existing_files:
        message_lines = [
            f"The following file(s) already exist in the project directory and would be overwritten:\n\n"]
        for filepath in existing_files:
            message_lines.append(f"  {filepath}\n")
        message_lines.append("\nPlease remove them or choose a different project directory.")
        raise ConfigurationError("".join(message_lines))
    shutil.copytree(project_template_dirpath, project_directory)
    update_pyproject_fields(project_directory, name, description)
    update_readme_fields(project_directory, name, description)
