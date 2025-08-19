from telegram import Update

import settings
from bot import consts, keyboards
from bot.context import CustomContext
from utils import write_data_to_sheet
from utils.course_request import remove_duplicate_summer_request

from .back import admin_back_handler


async def get_summer_requests_file_handler(update: Update, context: CustomContext):
    if update.effective_user.id not in settings.ADMIN_IDS:
        return consts.STATE_HOME

    text = update.message.text
    if text == keyboards.BACK:
        return await admin_back_handler(update, context)

    file_path = write_data_to_sheet(
        settings.EXCEL_BASE_SUMMER_TEMPLATE,
        text,
        text,
        remove_duplicate_summer_request(context.summer_request_list),
        ["A", "B", "C"],
    )

    await update.message.reply_document(
        document=file_path,
        reply_markup=keyboards.ADMIN_KEYBOARD,
        do_quote=True,
    )

    return consts.STATE_ADMIN


async def clean_summer_request_list_handler(update: Update, context: CustomContext):
    if update.effective_user.id not in settings.ADMIN_IDS:
        return consts.STATE_HOME

    text = update.message.text
    if text == keyboards.BACK:
        return await admin_back_handler(update, context)

    file_path = write_data_to_sheet(
        settings.EXCEL_BASE_SUMMER_TEMPLATE,
        text,
        text,
        remove_duplicate_summer_request(context.summer_request_list),
        ["A", "B", "C"],
    )

    # Clean list
    context.summer_request_list = []

    await update.message.reply_document(
        document=file_path,
        reply_markup=keyboards.ADMIN_KEYBOARD,
        do_quote=True,
    )

    return consts.STATE_ADMIN
