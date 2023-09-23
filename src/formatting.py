import ast
from typing import Any, List
import unidecode


def clean_accents(text: str) -> str:
    """
    Clean accents from string.
    :param text: text to clean
    :return: clean text
    """
    return unidecode.unidecode(text).strip()


def convert_special_char(text: str) -> str:
    """
    Convert special characters fromt text.
    :param text: text to clean
    :return: clean text
    """
    return (
        text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    )


def string_to_list_dict(text: str) -> List[Any] | ast.Dict[str, Any]:
    """
    Convert string version of list or dict to objects.
    :param text: list or dict as a string
    :return: list or dict
    """
    return ast.literal_eval(text)
