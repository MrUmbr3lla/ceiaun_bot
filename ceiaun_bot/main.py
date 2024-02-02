import logging
import os.path

from telegram import InputMediaDocument, Update, User
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler,
    PersistenceInput, PicklePersistence, filters
)

import settings
from bot import keyboards, messages
from utils import create_new_sheet, process_course_request

logger = logging.getLogger(__name__)

# States
HOME, REQUEST_COURSE, GET_CHARTS, CONVERT_COURSE = map(chr, range(4))
END = ConversationHandler.END


def save_user(context: ContextTypes.DEFAULT_TYPE, effective_user: User) -> None:
    user_id = effective_user.id
    username = effective_user.username
    user_full_name = effective_user.full_name

    user_list = context.bot_data.get("user_list", set())
    if user_id not in user_list:
        logger.info(f"New user: {user_id} / username: @{username} / full name: {user_full_name}")
        user_list.add(user_id)
        context.bot_data["user_list"] = user_list


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(context, update.effective_user)
    logger.info(context.user_data)

    await update.message.reply_document(
        quote=True,
        document=settings.FILE_HOME_IMAGE,
        reply_markup=keyboards.HOME_KEYBOARD,
        caption=messages.START_COMMAND,
    )

    return HOME


async def back_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_document(
        quote=True,
        document=settings.FILE_HOME_IMAGE,
        reply_markup=keyboards.HOME_KEYBOARD,
        caption=messages.HOME_SHORT,
    )

    return HOME


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # sending courses_list
    if text == keyboards.HOME_CHART:
        # Send se chart
        await context.bot.send_media_group(
            chat_id=update.effective_chat.id,
            media=[
                InputMediaDocument(settings.FILE_SE_CHARTS[0]),
                InputMediaDocument(
                    settings.FILE_SE_CHARTS[1],
                    caption=messages.CHART_SE_CAPTION,
                    parse_mode=ParseMode.HTML
                )
            ],
        )
        # Send it charts
        await context.bot.send_media_group(
            chat_id=update.effective_chat.id,
            media=[
                InputMediaDocument(settings.FILE_IT_CHARTS[0]),
                InputMediaDocument(
                    settings.FILE_IT_CHARTS[1],
                    caption=messages.CHART_IT_CAPTION,
                    parse_mode=ParseMode.HTML,
                )
            ],
        )
        # Send orient help
        await update.message.reply_text(
            quote=True,
            text=messages.CHART_SELECT_ORIENT,
            parse_mode=ParseMode.HTML,
            reply_markup=keyboards.HOME_KEYBOARD
        )

        return HOME

    # converting courses name
    if text == keyboards.HOME_CONVERT_NAME:
        await update.message.reply_document(
            document=settings.FILE_CONVERT_NAME,
            caption=messages.CONVERT_NAME_COMMAND,
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True
        )

        return CONVERT_COURSE

    # students requests
    if text == keyboards.HOME_COURSE_REQUEST:
        await update.message.reply_document(
            document=settings.FILE_COURSE_REQUEST,
            caption=messages.REQUEST_COMMAND,
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True
        )

        return REQUEST_COURSE


async def handle_convert_course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    REPLACE = (
        (" ", "%"),
        ("ی", "%"),
        ("ک", "%"),
        ("ي", "%"),
        ("ك", "%"),
    )

    text = update.message.text

    converted_name = text
    for r in REPLACE:
        converted_name = converted_name.replace(*r)

    result = ""
    for name in converted_name.split("\n"):
        result += f"<code>%{name}%</code>\n"

    await update.message.reply_text(
        text=messages.CONVERT_NAME_RESULT.format(result=result),
        parse_mode=ParseMode.HTML,
        quote=True,
        reply_markup=keyboards.BACK_KEYBOARD
    )


async def handle_request_course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    result = process_course_request(text)

    await update.message.reply_text(
        text=result,
        reply_markup=keyboards.BACK_KEYBOARD,
        quote=True
    )


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.warning(f"Error for update {update} caused error {context.error}")


if __name__ == "__main__":
    if not os.path.exists(settings.EXCEL_TEMP_FILE):
        create_new_sheet("temp")

    persistence = PicklePersistence(
        filepath=settings.BOT_DATABASE_DIR / "bot",
        store_data=PersistenceInput(chat_data=False, callback_data=False),
        single_file=False,
        update_interval=settings.BOT_DATABASE_UPDATE_INTERVAL
    )
    app = Application.builder().token(settings.BOT_TOKEN).persistence(persistence).build()

    all_keyboards = (
        f"^({keyboards.HOME_COURSE_REQUEST}|{keyboards.HOME_CONVERT_NAME}|{keyboards.HOME_CHART}|{keyboards.BACK})$"
    )
    main_conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", start_command),
            MessageHandler(
                filters.TEXT & filters.Regex(all_keyboards),
                start_command
            )
        ],
        states={
            HOME: [
                MessageHandler(filters.TEXT, handle_messages)
            ],
            REQUEST_COURSE: [
                MessageHandler(filters.TEXT & ~filters.Regex(f"^{keyboards.BACK}$"), handle_request_course)
            ],
            CONVERT_COURSE: [
                MessageHandler(filters.TEXT & ~filters.Regex(f"^{keyboards.BACK}$"), handle_convert_course)
            ],
        },
        fallbacks=[
            MessageHandler(filters.TEXT, start_command),
        ],
        name="main_conv",
        persistent=True
    )

    app.add_handlers([
        main_conv,
    ])

    # Errors
    app.add_error_handler(error)

    app.run_polling()
