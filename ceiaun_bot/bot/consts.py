import re

STATE_HOME, STATE_REQUEST_COURSE, STATE_CONVERT_COURSE = range(3)
(
    STATE_ADMIN, STATE_ADMIN_GET_FILE, STATE_ADMIN_FILE_ID, STATE_ADMIN_CLEAN_REQ, STATE_ADMIN_SEND_MSG
) = range(3, 8)

PERCENT_REPLACE = (
    (" ", "%"),
    ("ی", "%"),
    ("ک", "%"),
    ("ي", "%"),
    ("ك", "%"),
)

WORD_REPLACE = (
    ("ي", "ی"),
    ("ك", "ک"),
)

COURSE_NAME_EXCLUDE = (
    "فیزیک",
    "انس ",
    "قرآن",
    "قران",
    "اندیشه",
    "اسلام",
    "ورزش",
    "تربیت",
    "آیین",
    "تفسیر",
    "انقلاب",
    "دانش خانواده",
    "تمدن",
    "فارسی",
    "وصایا",
    "دیفرانسیل",
)
COURSE_NAME_EXCLUDE_REGEX = re.compile(f".*({'|'.join(COURSE_NAME_EXCLUDE)}).*")
