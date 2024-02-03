import logging

from telegram import Update
from telegram.ext import ContextTypes

import settings
from bot import keyboards, messages, states
from bot.database import get_course_request, get_file_last_index, get_user_count, save_file_last_index
from utils import write_data_to_sheet

logger = logging.getLogger(__name__)


async def admin_start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=messages.ADMIN_HOME,
        reply_markup=keyboards.ADMIN_KEYBOARD,
        quote=True,
    )

    context.user_data["state"] = states.ADMIN


async def back_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        text=messages.ADMIN_HOME,
        quote=True,
        reply_markup=keyboards.ADMIN_KEYBOARD,
    )

    return states.ADMIN


async def admin_panel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in settings.ADMIN_IDS:
        return states.HOME

    text = update.message.text

    if text == keyboards.ADMIN_STAT:
        await update.message.reply_text(
            text=messages.ADMIN_STAT.format(users_count=get_user_count(context)),
            reply_markup=keyboards.ADMIN_KEYBOARD,
            quote=True,
        )

        return states.ADMIN

    if text == keyboards.ADMIN_GET_FILE:
        await update.message.reply_text(
            text=messages.ADMIN_GET_FILE_TITLE,
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True
        )

        return states.ADMIN_GET_FILE

    return states.ADMIN


async def admin_send_file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in settings.ADMIN_IDS:
        return states.HOME

    text = update.message.text
    if text == keyboards.BACK:
        return await back_admin(update, context)

    first_index = get_file_last_index(context)
    course_requests = get_course_request(context)
    file_path = write_data_to_sheet(
        f"{text} ({first_index + 1}-{len(course_requests)})",
        course_requests[first_index:],
        ["A", "B", "C", "D"]
    )
    save_file_last_index(context, len(course_requests))

    await update.message.reply_document(
        document=file_path,
        reply_markup=keyboards.ADMIN_KEYBOARD,
        quote=True,
    )

    return states.ADMIN
