import logging
import os.path

from telegram import Update
from telegram import KeyboardButton,ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from unidecode import unidecode

import settings
from messages import messages
from utils import create_new_sheet, write_data_to_sheet

logger = logging.getLogger(__name__)

keys = [[KeyboardButton("درخواست افزایش ظرفیت")],
         [KeyboardButton("ابزار تبدیل متن") , KeyboardButton("چارت دروس")]]
key_markup = ReplyKeyboardMarkup(keys , resize_keyboard=True , one_time_keyboard=True)

buttons = ["درخواست افزایش ظرفیت" , "چارت دروس" , "ابزار تبدیل متن"]

### sending document and images
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document='BQACAgQAAxkBAAERRedltOR9eHOnJlCGmNmKlKQpkrVDHwAC4RAAAkpOqFHnytMdXl323zQE',
        caption=messages.START_COMMAND,
        reply_markup=key_markup,
        read_timeout= 20)


async def courses_list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pdf_file_ids = ["BQACAgQAAxkDAAPkZbZ_YkGd_DXFw_wyDBjH6EZRBmcAAnYUAAIZD7FRxvHkRVIWpJY0BA" , #لیست نرم افزار
                     "BQACAgQAAxkDAAPrZbaBDjIFWbLpNHcCjo53B-FVK0cAAoUUAAIZD7FRA6rSpl77Sbc0BA" , # لیست دروس فناوری اطلاعات
                       "BQACAgQAAxkDAAPtZbaBeZfNBWuqrG5Lhg5CpQdZOsYAAocUAAIZD7FRk3YrvhJRQoE0BA" , # چارت پیشنهادی نرم افزار
                         "BQACAgQAAxkDAAPuZbaBsMeu0Rw1kCQG3F9f9RKYPBoAAokUAAIZD7FROhPmiPgnhh40BA"] # چارت پیشنهادی فناوری اطلاعات
    for file_id in pdf_file_ids:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=file_id,
            read_timeout= 20)


async def request_sample_image_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document='BQACAgQAAxkDAAPQZbTmuFiI9B_rxHw_rSZGGRZEpygAAukQAAJKTqhRlM4x2o8RDP00BA',
        caption=messages.REQUEST_COMMAND,
        read_timeout= 20)
    

async def convert_name_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document='BQACAgQAAxkDAAPTZbTnHtO7g4RSzZpjpVermVDiNxUAAuoQAAJKTqhRx4DZ0PaIqU00BA',
        caption=messages.CONVERT_NAME_COMMAND,
        read_timeout= 20)
###


def handle_responses(text: str) -> str:
    processed: str = text

    # convert course name for Amoozeshyar
    if "تبدیل" in processed:
        chars = list(processed)
        course_name = chars[5:]
        if course_name[-1] != " ":
            course_name.append(" ")
        modified_name = "".join([sub
                                .replace(" ", "%")
                                .replace("ی", "%")
                                .replace("ک", "%")
                                .replace("ي", "%")
                                .replace("ك", "%")
                                 for sub in course_name])
        return modified_name

    user_text = processed.split("+")

    if len(user_text) != 4:
        return messages.INCORRECT_LENGTH

    student_name = user_text[0].strip()
    student_id = str(unidecode(user_text[1].strip()))
    student_course = user_text[2].strip()
    student_course_id = str(unidecode(user_text[3].strip()))

    if student_name.isnumeric():
        return messages.INCORRECT_USERNAME

    if (not student_id.isnumeric()) or (len(student_id) not in [8, 11, 14]):
        return messages.INCORRECT_STUDENT_ID

    if student_course.isnumeric():
        return messages.INCORRECT_COURSE

    if not student_course_id.isnumeric():
        return messages.INCORRECT_COURSE_ID

    # adding data to excel file
    write_data_to_sheet(
        settings.EXCEL_TEMP_FILE,
        [student_name, student_id, student_course, student_course_id],
        ["A", "B", "C", "D"],
        start_row_number=3
    )

    return messages.RECEIVED_REQUEST


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    users_id = update.message.from_user.username

    logger.info(f"user id is = {users_id}")
    logger.info(f" user{update.message.chat.id} in {message_type}: {text}")

    response = handle_responses(text)

    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.warning(f"Error for update {update} caused error {context.error}")


if __name__ == "__main__":
    if not os.path.exists(settings.EXCEL_TEMP_FILE):
        create_new_sheet("temp")

    app = Application.builder().token(settings.BOT_TOKEN).build()

    app.add_handlers([
        # Commands
        CommandHandler("start", start_command),
        CommandHandler("chart_dorus" , courses_list_command),
        CommandHandler("request" , request_sample_image_command),
        CommandHandler("convert_name" , convert_name_command),

        # Messages
        MessageHandler(filters.TEXT, handle_messages),
    ])

    # Errors
    app.add_error_handler(error)

    app.run_polling()
