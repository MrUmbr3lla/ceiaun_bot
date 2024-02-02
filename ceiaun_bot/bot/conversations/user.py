import logging

from telegram import InputMediaDocument, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import settings
from bot import keyboards, messages, states
from bot.database import save_user
from utils import process_course_request

logger = logging.getLogger(__name__)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(context, update.effective_user)
    logger.info(context.user_data)

    await update.message.reply_document(
        quote=True,
        document=settings.FILE_HOME_IMAGE,
        reply_markup=keyboards.HOME_KEYBOARD,
        caption=messages.START_COMMAND,
    )

    return states.HOME


async def back_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_document(
        quote=True,
        document=settings.FILE_HOME_IMAGE,
        reply_markup=keyboards.HOME_KEYBOARD,
        caption=messages.HOME_SHORT,
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


async def convert_course_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
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


async def request_course_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    result = process_course_request(text)

    await update.message.reply_text(
        text=result,
        reply_markup=keyboards.BACK_KEYBOARD,
        quote=True
    )
