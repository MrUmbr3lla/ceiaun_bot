import re

STATE_HOME, STATE_REQUEST_COURSE, STATE_CONVERT_COURSE = range(3)
STATE_ADMIN, STATE_ADMIN_GET_FILE, STATE_ADMIN_FILE_ID = range(3, 6)

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
)
COURSE_NAME_EXCLUDE_REGEX = re.compile(f".*({'|'.join(COURSE_NAME_EXCLUDE)}).*")
