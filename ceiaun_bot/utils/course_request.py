from unidecode import unidecode

from bot import consts, messages


def remove_special_characters(text: str) -> str:
    return "".join(e for e in text if e.isalnum())


def process_course_request(text: str) -> list:
    user_text = text.split("+")

    # Request must be 4 part (student name + student id + course name + course id)
    if len(user_text) != 4:
        raise ValueError(messages.REQ_ERROR_LENGTH, "REQ_ERROR_LENGTH")

    # Remove special chars and Convert persian number to english number
    student_name = user_text[0].strip()
    student_id = remove_special_characters(unidecode(user_text[1]))
    course_name = user_text[2].strip()
    course_id = remove_special_characters(unidecode(user_text[3].strip()))

    # Course name replace
    for words in consts.WORD_REPLACE:
        course_name = course_name.replace(*words)

    # Clean
    clean_student_name(student_name)
    clean_student_id(student_id)
    clean_course_name(course_name)
    clean_course_id(course_id)

    return [student_name, student_id, course_name, course_id]


def clean_student_name(name: str) -> None:
    if name == "":
        raise ValueError(messages.REQ_ERROR_USERNAME_NONE, "REQ_ERROR_USERNAME_NONE")

    if name.isnumeric():
        raise ValueError(messages.REQ_ERROR_USERNAME, "REQ_ERROR_USERNAME")


def clean_student_id(student_id):
    if student_id == "":
        raise ValueError(messages.REQ_ERROR_STUDENT_ID_NONE, "REQ_ERROR_STUDENT_ID_NONE")

    if not student_id.isnumeric():
        raise ValueError(messages.REQ_ERROR_STUDENT_ID, "REQ_ERROR_STUDENT_ID")

    if len(student_id) == 10:
        raise ValueError(messages.REQ_ERROR_STUDENT_ID_CODE_MELLI, "REQ_ERROR_STUDENT_ID_CODE_MELLI")

    if len(student_id) not in [8, 11, 14]:
        raise ValueError(messages.REQ_ERROR_STUDENT_ID, "REQ_ERROR_STUDENT_ID")


def clean_course_name(course_name):
    if course_name == "":
        raise ValueError(messages.REQ_ERROR_COURSE_NONE, "REQ_ERROR_COURSE_NONE")

    if course_name.isnumeric():
        raise ValueError(messages.REQ_ERROR_COURSE, "REQ_ERROR_COURSE")

    if consts.COURSE_NAME_EXCLUDE_REGEX.match(course_name):
        raise ValueError(messages.REQ_ERROR_COURSE_DEPARTMENT, "REQ_ERROR_COURSE_DEPARTMENT")


def clean_course_id(course_id):
    if course_id == "":
        raise ValueError(messages.REQ_ERROR_COURSE_ID_NONE, "REQ_ERROR_COURSE_ID_NONE")

    if not course_id.isnumeric():
        raise ValueError(messages.REQ_ERROR_COURSE_ID, "REQ_ERROR_COURSE_ID")

    if len(course_id) == 10:
        raise ValueError(messages.REQ_ERROR_COURSE_ID_INSTEAD, "REQ_ERROR_COURSE_ID_INSTEAD")


def remove_duplicate_request(request_list: list[list]) -> list[list]:
    requests = {}
    result = []
    for req in request_list:
        course_student = requests.setdefault(req[3], [])
        if req[1] not in course_student:
            course_student.append(req[1])
            result.append(req)

    return result
