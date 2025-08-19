from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.consts import ACCEPT_NOT_OK, ACCEPT_OK, SUMMER_REQUEST_COURSES
from bot.types import FlagDict

SUMMER_REQUEST_ACCEPT_QUERY = "accept"
SUMMER_REQUEST_BACK_QUERY = "back"
ADMIN_STATUS_BACK_QUERY = "back"

SUMMER_REQUEST_GET_NAME_KEYBOARD = InlineKeyboardMarkup(
    [[InlineKeyboardButton("برگشت 🔙", callback_data=SUMMER_REQUEST_BACK_QUERY)]]
)


def generate_summer_request_inline_keyboard(course_status: dict[int, bool]) -> InlineKeyboardMarkup:
    keyboards = []
    for summer_course in SUMMER_REQUEST_COURSES:
        accept_status = ACCEPT_OK if course_status[summer_course.id] else ACCEPT_NOT_OK
        keyboards.append(
            InlineKeyboardButton(
                f"{summer_course.name} {accept_status}",
                callback_data=f"course-{summer_course.id}",
            )
        )

    inline_keyboard = []
    for i in range(0, len(keyboards), 2):
        inline_keyboard.append(keyboards[i : i + 2])

    inline_keyboard.append([InlineKeyboardButton("ثبت درخواست 🎯", callback_data=SUMMER_REQUEST_ACCEPT_QUERY)])
    inline_keyboard.append([InlineKeyboardButton("برگشت 🔙", callback_data=SUMMER_REQUEST_BACK_QUERY)])

    return InlineKeyboardMarkup(inline_keyboard)


def generate_admin_status_inline_keyboard(flags: FlagDict) -> InlineKeyboardMarkup:
    keyboards = []
    for status_key, status_value in flags.items():
        status_icon = ACCEPT_OK if status_value else ACCEPT_NOT_OK
        keyboards.append(
            InlineKeyboardButton(
                f"{status_key} {status_icon}",
                callback_data=f"ad-status-{status_key}",
            )
        )

    inline_keyboard = []
    for i in range(0, len(keyboards), 2):
        inline_keyboard.append(keyboards[i : i + 2])

    inline_keyboard.append([InlineKeyboardButton("برگشت 🔙", callback_data=ADMIN_STATUS_BACK_QUERY)])

    return InlineKeyboardMarkup(inline_keyboard)
