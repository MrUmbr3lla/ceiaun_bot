from telegram import KeyboardButton, ReplyKeyboardMarkup

# Home
HOME_COURSE_REQUEST = "درخواست افزایش ظرفیت 📮"
HOME_SUMMER_REQUEST = "درخواست دروس تابستان 🏖"
HOME_CONVERT_NAME = "ابزار تبدیل متن 🔃"
HOME_CHART = "چارت دروس 📚"

HOME_KEYBOARD = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(HOME_COURSE_REQUEST),
        ],
        [
            KeyboardButton(HOME_SUMMER_REQUEST),
        ],
        [
            KeyboardButton(HOME_CONVERT_NAME),
            KeyboardButton(HOME_CHART),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

# Back
BACK = "برگشت 🔙"

BACK_KEYBOARD = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(BACK),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
)

# Admin
ADMIN_STAT = "آمار 📝"
ADMIN_GET_FILE_ID = "دریافت آیدی فایل"
ADMIN_GET_FILE = "دریافت فایل اکسل 📤"
ADMIN_CLEAN_REQUEST_LIST = "پاکسازی لیست درخواست ها"
ADMIN_GET_SUMMER_REQUESTS = "دریافت درخواست های تابستان"
ADMIN_CLEAN_SUMMER_REQUESTS = "پاکسازی لیست درخواست های تابستان"
ADMIN_SEND_MESSAGE = "ارسال پیام به کاربر"
ADMIN_SEND_MESSAGE_TO_ALL = "ارسال پیام به همه"

ADMIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(ADMIN_STAT),
            KeyboardButton(ADMIN_GET_FILE_ID),
        ],
        [
            KeyboardButton(ADMIN_GET_FILE),
            KeyboardButton(ADMIN_CLEAN_REQUEST_LIST),
        ],
        [
            KeyboardButton(ADMIN_GET_SUMMER_REQUESTS),
            KeyboardButton(ADMIN_CLEAN_SUMMER_REQUESTS),
        ],
        [
            KeyboardButton(ADMIN_SEND_MESSAGE),
        ],
        [
            KeyboardButton(ADMIN_SEND_MESSAGE_TO_ALL),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
