import re
from typing import Optional


def camel_case(s):
    """Convert a string to camelCase.

    Args:
        s (str): The input string, typically with underscores or spaces.

    Returns:
        str: The camelCase version of the input string.

    Example:
        >>> camel_case("hello_world")
        'helloWorld'
    """
    words = s.replace("_", " ").split()
    return words[0].lower() + "".join(w.capitalize() for w in words[1:])


def normalize_package(name: str) -> str:
    """Creates a normalized package name used for installable packages

    Args:
        name (str): The name of the package

    Returns:
        str: Normalized package name
    """
    return re.sub(r"[-_.]+", "-", name).lower()


def truncate(text: str, max_length: int, ellipsis: str = "...") -> Optional[str]:
    """Truncate a string to a maximum length, appending an ellipsis if truncated.

    Args:
        text (str): The input string to truncate.
        max_length (int): The maximum length of the output string (including ellipsis).
        ellipsis (str, optional): The string to append if truncated. Defaults to "...".

    Returns:
        Optional[str]: The truncated string, or None if input is invalid.

    Examples:
        >>> truncate("Hello, World!", 8)
        'Hello...'
        >>> truncate("Short", 10)
        'Short'
        >>> truncate("", 5)
        None
    """
    if not text or not isinstance(text, str) or max_length < len(ellipsis):
        return None

    if len(text) <= max_length:
        return text

    return text[: max_length - len(ellipsis)] + ellipsis


def to_snake_case(text: str) -> Optional[str]:
    """
    Convert a string to snake_case (lowercase with underscores).

    Args:
        text (str): The input string to convert.

    Returns:
        Optional[str]: The snake_case string, or None if input is invalid.

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("My Package Name")
        'my_package_name'
        >>> to_snake_case("")
        None
    """
    if not text or not isinstance(text, str):
        return None

    # Replace non-alphanumeric with underscore, split camelCase
    normalized = re.sub(r"([A-Z])([a-z0-9])", r"\1_\2", text)
    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", normalized).lower()
    normalized = re.sub(r"_+", "_", normalized).strip("_")

    return normalized if normalized else None


def clean_string(text: str, allow_spaces: bool = False) -> Optional[str]:
    """
    Clean a string by removing extra whitespace and special characters.

    Args:
        text (str): The input string to clean.
        allow_spaces (bool, optional): If True, preserve single spaces between words.
                                      If False, replace spaces with empty string.
                                      Defaults to False.

    Returns:
        Optional[str]: The cleaned string, or None if input is invalid.

    Examples:
        >>> clean_string("  Hello  @World!  ")
        'HelloWorld'
        >>> clean_string("  Hello  World!  ", allow_spaces=True)
        'Hello World'
        >>> clean_string("")
        None
    """
    if not text or not isinstance(text, str):
        return None

    if allow_spaces:
        # Replace multiple spaces with single space, remove special characters
        cleaned = re.sub(r"[^a-zA-Z0-9\s]", "", text)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
    else:
        # Remove all whitespace and special characters
        cleaned = re.sub(r"[^a-zA-Z0-9]", "", text)

    return cleaned if cleaned else None
