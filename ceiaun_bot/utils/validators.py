from bot import consts, messages


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
