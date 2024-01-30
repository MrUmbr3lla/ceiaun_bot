from unidecode import unidecode

import settings
from messages import messages
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


def process_course_request(text: str) -> str:
    user_text = text.split("+")
    if len(user_text) != 4:
        return messages.REQUEST_INCORRECT_LENGTH

    student_name = user_text[0].strip()
    student_id = str(unidecode(user_text[1].strip()))
    student_course = user_text[2].strip()
    student_course_id = str(unidecode(user_text[3].strip()))

    if student_name.isnumeric():
        return messages.REQUEST_INCORRECT_USERNAME

    if (not student_id.isnumeric()) or (len(student_id) not in [8, 11, 14]):
        return messages.REQUEST_INCORRECT_STUDENT_ID

    if student_course.isnumeric():
        return messages.REQUEST_INCORRECT_COURSE

    if not student_course_id.isnumeric():
        return messages.REQUEST_INCORRECT_COURSE_ID

    # adding data to excel file
    write_data_to_sheet(
        settings.EXCEL_TEMP_FILE,
        [student_name, student_id, student_course, student_course_id],
        ["A", "B", "C", "D"],
        start_row_number=3
    )

    return messages.REQUEST_RECEIVED_REQUEST
