import logging

from telegram import InputMediaDocument, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import settings
from bot import keyboards, messages, states
from bot.database import save_course_request, save_user
from utils import process_course_request

logger = logging.getLogger(__name__)


async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(context, update.effective_user)

    await update.message.reply_document(
        quote=True,
        document=settings.FILE_HOME_IMAGE,
        reply_markup=keyboards.HOME_KEYBOARD,
        caption=messages.START_COMMAND,
    )

    context.user_data["state"] = states.HOME


async def back_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=messages.HOME_SHORT,
        quote=True,
        reply_markup=keyboards.HOME_KEYBOARD,
    )

    return states.HOME


async def home_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

        return states.HOME

    # converting courses name
    if text == keyboards.HOME_CONVERT_NAME:
        await update.message.reply_document(
            document=settings.FILE_CONVERT_NAME,
            caption=messages.CONVERT_NAME_COMMAND,
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True
        )

        return states.CONVERT_COURSE

    # students requests
    if text == keyboards.HOME_COURSE_REQUEST:
        await update.message.reply_document(
            document=settings.FILE_COURSE_REQUEST,
            caption=messages.REQUEST_COMMAND,
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True
        )

        return states.REQUEST_COURSE

    return states.HOME


async def convert_course_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    REPLACE = (
        (" ", "%"),
        ("ی", "%"),
        ("ک", "%"),
        ("ي", "%"),
        ("ك", "%"),
    )

    text = update.message.text

    if text == keyboards.BACK:
        return await back_home(update, context)

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


async def request_course_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == keyboards.BACK:
        return await back_home(update, context)

    try:
        request_list = process_course_request(text)
    except ValueError as e:
        await update.message.reply_text(
            text=str(e),
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True
        )
        return None

    user_id = update.effective_user.id
    username = update.effective_user.username
    logger.info(f"user {user_id} with username @{username} has request: {request_list}")

    save_course_request(context, request_list)
    logger.info(f"bot data: {context.bot_data}")

    await update.message.reply_text(
        text=messages.REQUEST_RECEIVED_REQUEST,
        reply_markup=keyboards.BACK_KEYBOARD,
        quote=True
    )
