import logging

from telegram import Update

from bot import keyboards, messages
from bot.context import CustomContext
from utils import process_course_request

from .back import back_home_handler

request_logger = logging.getLogger("request_log")
bad_request_logger = logging.getLogger("bad_request_log")


async def request_course_handler(update: Update, context: CustomContext):
    text = update.message.text
    user_id = update.effective_user.id
    username = update.effective_user.username

    if text == keyboards.BACK or not context.flags["REQUEST_OPEN"]:
        return await back_home_handler(update, context)

    try:
        request_list = process_course_request(text)
    except ValueError as e:
        await update.message.reply_text(
            text=e.args[0],
            reply_markup=keyboards.BACK_KEYBOARD,
            do_quote=True,
        )
        bad_request_logger.info(f"user {user_id} with username @{username} has bad request with id {e.args[1]}: {text}")
        return None

    request_logger.info(f"user {user_id} with username @{username} has request: {','.join(request_list)}")
    context.request_list.append(request_list)

    await update.message.reply_text(
        text=messages.REQ_RECEIVED_REQ,
        reply_markup=keyboards.BACK_KEYBOARD,
        do_quote=True,
    )
