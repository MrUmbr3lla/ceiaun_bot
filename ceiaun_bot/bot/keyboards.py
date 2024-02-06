from telegram import KeyboardButton, ReplyKeyboardMarkup

# Home
HOME_COURSE_REQUEST = "درخواست افزایش ظرفیت 📮"
HOME_CONVERT_NAME = "ابزار تبدیل متن 🔃"
HOME_CHART = "چارت دروس 📚"

HOME_KEYBOARD = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(HOME_COURSE_REQUEST)
        ],
        [
            KeyboardButton(HOME_CONVERT_NAME), KeyboardButton(HOME_CHART)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Back
BACK = "برگشت 🔙"

BACK_KEYBOARD = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(BACK)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

# Admin
ADMIN_STAT = "آمار کاربران 📝"
ADMIN_GET_FILE = "دریافت فایل اکسل 📤"
ADMIN_GET_FILE_ID = "دریافت آیدی فایل"

ADMIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(ADMIN_STAT), KeyboardButton(ADMIN_GET_FILE)
        ],
        [
            KeyboardButton(ADMIN_GET_FILE_ID)
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
