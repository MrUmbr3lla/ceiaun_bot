# Home
from telegram import KeyboardButton, ReplyKeyboardMarkup

HOME_COURSE_REQUEST = "درخواست افزایش ظرفیت"
HOME_CONVERT_NAME = "ابزار تبدیل متن"
HOME_CHART = "چارت دروس"

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
