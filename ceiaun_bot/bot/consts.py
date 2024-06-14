import re
from collections import namedtuple

STATE_HOME, STATE_REQUEST_COURSE, STATE_CONVERT_COURSE, STATE_SUMMER_REQUEST, STATE_SUMMER_REQUEST_GET_NAME = range(5)
(
    STATE_ADMIN,
    STATE_ADMIN_GET_FILE,
    STATE_ADMIN_FILE_ID,
    STATE_ADMIN_CLEAN_REQ,
    STATE_ADMIN_SEND_MSG,
    STATE_ADMIN_SUMMER_REQUEST,
    STATE_ADMIN_CLEAN_SUMMER_REQUEST,
) = range(100, 107)

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

SummerCourse = namedtuple("SummerCourse", ["id", "name"])
SUMMER_REQUEST_COURSES = [
    SummerCourse(1, "مبانی کامپیوتر"),
    SummerCourse(2, "برنامه سازی پیشرفته"),
    SummerCourse(3, "مدارهای منطقی"),
    SummerCourse(4, "ریاضیات گسسته"),
    SummerCourse(5, "کارگاه کامپیوتر"),
    SummerCourse(6, "مدار الکتریکی"),
]

ACCEPT_OK = "✅"
ACCEPT_NOT_OK = "❌"
