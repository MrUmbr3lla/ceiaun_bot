from unidecode import unidecode

from bot import messages
from .excel import write_data_to_sheet  # noqa


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


def process_course_request(text: str) -> list:
    user_text = text.split("+")
    if len(user_text) != 4:
        raise ValueError(messages.REQUEST_INCORRECT_LENGTH)

    student_name = user_text[0].strip()
    student_id = str(unidecode(user_text[1].strip()))
    student_course = user_text[2].strip()
    student_course_id = str(unidecode(user_text[3].strip()))

    if student_name.isnumeric():
        raise ValueError(messages.REQUEST_INCORRECT_USERNAME)

    if (not student_id.isnumeric()) or (len(student_id) not in [8, 11, 14]):
        raise ValueError(messages.REQUEST_INCORRECT_STUDENT_ID)

    if student_course.isnumeric():
        raise ValueError(messages.REQUEST_INCORRECT_COURSE)

    if not student_course_id.isnumeric():
        raise ValueError(messages.REQUEST_INCORRECT_COURSE_ID)

    return [student_name, student_id, student_course, student_course_id]
