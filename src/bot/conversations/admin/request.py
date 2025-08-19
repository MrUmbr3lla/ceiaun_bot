from telegram import Update

import settings
from bot import consts, keyboards
from bot.context import CustomContext
from utils import remove_duplicate_request, write_data_to_sheet

from .back import admin_back_handler


async def get_requests_file_handler(update: Update, context: CustomContext):
    if update.effective_user.id not in settings.ADMIN_IDS:
        return consts.STATE_HOME

    text = update.message.text
    if text == keyboards.BACK:
        return await admin_back_handler(update, context)

    first_index = context.file_last_index
    course_requests = context.request_list
    file_path = write_data_to_sheet(
        settings.EXCEL_BASE_TEMPLATE,
        f"{text} ({first_index + 1}-{len(course_requests)})",
        text,
        remove_duplicate_request(course_requests[first_index:]),
        ["A", "B", "C", "D"],
    )
    context.file_last_index = len(course_requests)

    await update.message.reply_document(
        document=file_path,
        reply_markup=keyboards.ADMIN_KEYBOARD,
        do_quote=True,
    )

    return consts.STATE_ADMIN


async def clean_request_list_handler(update: Update, context: CustomContext):
    if update.effective_user.id not in settings.ADMIN_IDS:
        return consts.STATE_HOME

    text = update.message.text
    if text == keyboards.BACK:
        return await admin_back_handler(update, context)

    course_requests = context.request_list
    file_path = write_data_to_sheet(
        settings.EXCEL_BASE_TEMPLATE,
        f"{text} (1-{len(course_requests)})",
        text,
        remove_duplicate_request(course_requests),
        ["A", "B", "C", "D"],
    )

    # Clean list
    context.request_list = []
    context.file_last_index = 0

    await update.message.reply_document(
        document=file_path,
        reply_markup=keyboards.ADMIN_KEYBOARD,
        do_quote=True,
    )

    return consts.STATE_ADMIN
