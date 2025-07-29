import string
from pathlib import Path

import tomli
import tomli_w

import demonstrable.project.metadata


def update_pyproject_fields(project_directory: Path, name: str | None, description: str | None):
    """Update the pyproject.toml file with the given name and description.

    Args:
        project_directory (Path): The path to the project directory.
        name (str | None): The name of the project.
        description (str | None): The description of the project.

    Raises:
        DataError: If the name or description is invalid.
    """
    if (name is not None) or (description is not None):
        pyproject_filepath = project_directory / "pyproject.toml"
        name = demonstrable.project.metadata.valid_name(name)
        description = demonstrable.project.metadata.valid_description(description)
        with open(pyproject_filepath, "rb") as f:
            pyproject = tomli.load(f)
            if name:
                pyproject["project"]["name"] = name
            if description:
                pyproject["project"]["description"] = description
        with open(pyproject_filepath, "wb") as f:
            tomli_w.dump(pyproject, f)


def update_readme_fields(project_directory: Path, name: str | None, description: str | None):
    """Update the README.md file with the given name and description.

    Args:
        project_directory (Path): The path to the project directory.
        name (str | None): The name of the project.
        description (str | None): The description of the project.

    Raises:
        DataError: If the name or description is invalid.
    """
    name = name or "<your-project-name>"
    description = description or "<your-project-description>"
    readme_filepath = project_directory / "README.md"
    # The default README.md file contains PEP 292 style placeholders
    readme_text = readme_filepath.read_text()
    readme_template = string.Template(readme_text)
    readme_text = readme_template.substitute(
        project_name=name,
        project_description=description,
        project_dirname=project_directory.resolve().name,
    )
    readme_filepath.write_text(readme_text)
