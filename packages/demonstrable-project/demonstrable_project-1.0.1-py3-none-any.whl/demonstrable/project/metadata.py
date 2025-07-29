import re

from demonstrable.exception import DataError

_NAME_PATTERN = r"^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$"
_NAME_REGEX = re.compile(_NAME_PATTERN, re.IGNORECASE)


class InvalidNameError(DataError):
    """Exception raised when a project name is invalid."""


class InvalidDescriptionError(DataError):
    """Exception raised when a project description is invalid."""


def is_valid_name(name: str) -> bool:
    """
    Check if the given name is a valid project name.

    Valid names are defined here at,

     https://packaging.python.org/en/latest/specifications/name-normalization/#name-format

    """
    return _NAME_REGEX.match(name) is not None


def valid_name(name: str) -> str:
    """Ensure the given name is valid and return it.

    Args:
        name (str): The name to validate.

    Returns:
        str: The validated name.

    Raises:
        InvalidNameError: If the name is not valid.
    """
    if not is_valid_name(name):
        raise InvalidNameError(
            f"Project name '{name}' is not allowed. "
            f"A valid name consists only of the letters A-Z or a-z, and numbers, "
            f"period, underscore and hyphen. It must start and end with "
            f"a letter or number."
        )
    return name.strip()


def normalize_name(name: str) -> str:
    """
    Normalize the given name to a valid project name.

    Name normalization is defined at,

     https://packaging.python.org/en/latest/specifications/name-normalization/#name-format
    """
    if not is_valid_name(name):
        raise ValueError(f"Invalid project name: {name}")
    return re.sub(r"[-_.]+", "-", name).lower()


def is_valid_description(description: str):
    """Determine if the given description is valid."""
    return description.strip() != ""


def valid_description(description: str) -> str:
    """Ensure the given description is valid and return it.

    Args:
        description (str): The description to validate.

    Returns:
        str: The validated description.

    Raises:
        InvalidDescriptionError: If the description is not valid.
    """
    if not is_valid_description(description):
        raise InvalidDescriptionError(
            f"Project description '{description}' is not allowed. "
            f"A valid description cannot be blank or empty."
        )
    return description.strip()