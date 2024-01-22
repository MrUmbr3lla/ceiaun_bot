from unidecode import unidecode

from .excel import create_new_sheet, write_data_to_sheet  # noqa


def replace_persian_numbers(data: str) -> str:
    """
    Replace persian number with english number.
    """
    return unidecode(data)


def clean_data(data: str, has_number: list = None) -> list[str]:
    """
    Split and Clean data

    If each value of data has number, replace persian number with english number.
    """

    if has_number is None:
        has_number = []

    cleaned_data = []
    for i, value in enumerate(data.split("+")):
        if i in has_number:
            value = replace_persian_numbers(value)

        cleaned_data.append(value.strip())

    return cleaned_data
