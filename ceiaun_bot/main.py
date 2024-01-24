import logging
import os.path

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from unidecode import unidecode

import settings
from messages import messages
from utils import create_new_sheet, write_data_to_sheet

logger = logging.getLogger(__name__)

### sending document
async def chart_dorus_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document='BQACAgQAAxkBAAERPi1lsWN1VBB6czr0HQM5Q4J31AABCCIAAnsVAAL5hIhRWRHMoy7Si640BA',
        caption='test',
        read_timeout= 20)
    
async def chart_pishnahadi_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_document(
        chat_id=update.effective_chat.id,
        document='BQACAgQAAxkBAAERPitlsWIB7Lw7uhjcD3Okr-tupMXk8QACcxUAAvmEiFH7fwL8DbFr7zQE',
        caption='test',
        read_timeout= 20)
###

#start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=messages.START_COMMAND)

#help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text=messages.HELP_COMMAND)


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
        CommandHandler("help", help_command),
        CommandHandler("chart_dorus" , chart_dorus_command),
        CommandHandler("chart_pishnahadi" , chart_pishnahadi_command),

        # Messages
        MessageHandler(filters.TEXT, handle_messages),
    ])

    # Errors
    app.add_error_handler(error)

    app.run_polling()
