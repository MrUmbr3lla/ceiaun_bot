import logging
import os.path

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import settings
from messages import messages
from utils import create_new_sheet

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keys = [[KeyboardButton("درخواست افزایش ظرفیت")],
            [KeyboardButton("ابزار تبدیل متن"), KeyboardButton("چارت دروس")]]
    key_markup = ReplyKeyboardMarkup(keys, resize_keyboard=True, one_time_keyboard=True)
    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document='BQACAgQAAx0Edz5chAADCWW340mbGOmLl-WAtkCOFxEm1L5kAAIPEAACi4zBUS36-Kc0q-JeNAQ',
        reply_markup=key_markup,
        caption=messages.START_COMMAND,
        read_timeout=20)


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    users_id = update.message.from_user.username

    # sending courses_list (done)
    if "چارت دروس" in text:

        for file_id in settings.FILE_SE_CHARTS + settings.FILE_IT_CHARTS:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file_id,
                read_timeout=20
            )

    # converting courses name (unfinished)
    if "ابزار تبدیل متن" in text:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document="BQACAgQAAx0Edz5chAADCmW3440_ebd_3XPYwfxkoCpz8TYnAAIQEAACi4zBUfXtf4Z0LyMsNAQ",
            caption=messages.CONVERT_NAME_COMMAND,
            read_timeout=20)

        # باید با استیت هندل بشه ############################

        # chars = list(text)
        # course_name = chars[5:]
        # if course_name[-1] != " ":
        #     course_name.append(" ")
        # modified_name = "".join([sub
        #                         .replace(" ", "%")
        #                         .replace("ی", "%")
        #                         .replace("ک", "%")
        #                         .replace("ي", "%")
        #                         .replace("ك", "%")
        #                          for sub in course_name])
        # return modified_name

    # students requests (unfinished)
    if "درخواست افزایش ظرفیت" in text:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document='BQACAgQAAx0Edz5chAADB2W34uUd86Q7EG8SNB8-jRtiPMZsAAINEAACi4zBURJXGMOkPaRENAQ',
            caption=messages.REQUEST_COMMAND,
            read_timeout=20)

    # باید با استیت هندل بشه ############################

    # user_text = text.split("+")
    # if len(user_text) != 4:
    #     return messages.INCORRECT_LENGTH

    # student_name = user_text[0].strip()
    # student_id = str(unidecode(user_text[1].strip()))
    # student_course = user_text[2].strip()
    # student_course_id = str(unidecode(user_text[3].strip()))

    # if student_name.isnumeric():
    #     return messages.INCORRECT_USERNAME

    # if (not student_id.isnumeric()) or (len(student_id) not in [8, 11, 14]):
    #     return messages.INCORRECT_STUDENT_ID

    # if student_course.isnumeric():
    #     return messages.INCORRECT_COURSE

    # if not student_course_id.isnumeric():
    #     return messages.INCORRECT_COURSE_ID

    # #adding data to excel file
    # write_data_to_sheet(
    #     settings.EXCEL_TEMP_FILE,
    #     [student_name, student_id, student_course, student_course_id],
    #     ["A", "B", "C", "D"],
    #     start_row_number=3)

    # return messages.RECEIVED_REQUEST
    ###

    logger.info(f"user id is = {users_id}")
    logger.info(f" user{update.message.chat.id} in {message_type}: {text}")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.warning(f"Error for update {update} caused error {context.error}")


if __name__ == "__main__":
    if not os.path.exists(settings.EXCEL_TEMP_FILE):
        create_new_sheet("temp")

    app = Application.builder().token(settings.BOT_TOKEN).build()

    app.add_handlers([
        # Commands
        CommandHandler("start", start_command),
        # Messages
        MessageHandler(filters.TEXT, handle_messages),
    ])

    # Errors
    app.add_error_handler(error)

    app.run_polling()
