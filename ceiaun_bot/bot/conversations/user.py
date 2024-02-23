import logging

from telegram import InputMediaDocument, Update

import settings
from bot import consts, keyboards, messages
from bot.context import CustomContext
from utils import process_course_request

logger = logging.getLogger(__name__)
request_logger = logging.getLogger("request_log")
bad_request_logger = logging.getLogger("bad_request_log")


async def start_command_handler(update: Update, context: CustomContext):
    await update.message.reply_document(
        quote=True,
        document=settings.FILE_HOME_IMAGE,
        reply_markup=keyboards.HOME_KEYBOARD,
        caption=messages.START_COMMAND,
    )

    context.user_state = consts.STATE_HOME


async def back_home(update: Update, context: CustomContext):
    await update.message.reply_text(
        text=messages.HOME_SHORT,
        quote=True,
        reply_markup=keyboards.HOME_KEYBOARD,
    )

    return consts.STATE_HOME


async def home_handler(update: Update, context: CustomContext):
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
                    caption=messages.CHART_SE_CAPTION
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
                    caption=messages.CHART_IT_CAPTION
                )
            ],
        )
        # Send orient help
        await update.message.reply_text(
            quote=True,
            text=messages.CHART_SELECT_ORIENT,
            reply_markup=keyboards.HOME_KEYBOARD
        )

        return consts.STATE_HOME

    # converting courses name
    if text == keyboards.HOME_CONVERT_NAME:
        await update.message.reply_document(
            document=settings.FILE_CONVERT_NAME,
            caption=messages.CONVERT_NAME_COMMAND,
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True
        )

        return consts.STATE_CONVERT_COURSE

    # students requests
    if text == keyboards.HOME_COURSE_REQUEST:
        await update.message.reply_document(
            document=settings.FILE_COURSE_REQUEST,
            caption=messages.REQ_COMMAND,
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True
        )

        return consts.STATE_REQUEST_COURSE


async def convert_course_handler(update: Update, context: CustomContext):
    text = update.message.text

    if text == keyboards.BACK:
        return await back_home(update, context)

    converted_name = text
    for r in consts.PERCENT_REPLACE:
        converted_name = converted_name.replace(*r)

    result = ""
    for name in converted_name.split("\n"):
        result += f"<code>%{name}%</code>\n"

    await update.message.reply_text(
        text=messages.CONVERT_NAME_RESULT.format(result=result),
        quote=True,
        reply_markup=keyboards.BACK_KEYBOARD
    )


async def request_course_handler(update: Update, context: CustomContext):
    text = update.message.text
    user_id = update.effective_user.id
    username = update.effective_user.username

    if text == keyboards.BACK:
        return await back_home(update, context)

    try:
        request_list = process_course_request(text)
    except ValueError as e:
        await update.message.reply_text(
            text=e.args[0],
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True
        )
        bad_request_logger.info(f"user {user_id} with username @{username} has bad request with id {e.args[1]}: {text}")
        return None

    request_logger.info(f"user {user_id} with username @{username} has request: {','.join(request_list)}")
    context.request_list.append(request_list)

    await update.message.reply_text(
        text=messages.REQ_RECEIVED_REQ,
        reply_markup=keyboards.BACK_KEYBOARD,
        quote=True
    )
