import logging

from telegram import Update

import settings
from bot import consts, keyboards, messages
from bot.context import CustomContext
from utils import write_data_to_sheet

logger = logging.getLogger(__name__)


async def admin_start_command_handler(update: Update, context: CustomContext):
    await update.message.reply_text(
        text=messages.ADMIN_HOME,
        reply_markup=keyboards.ADMIN_KEYBOARD,
        quote=True,
    )

    context.user_data["state"] = consts.STATE_ADMIN


async def back_admin(update: Update, context: CustomContext):
    await update.message.reply_text(
        text=messages.ADMIN_HOME,
        quote=True,
        reply_markup=keyboards.ADMIN_KEYBOARD,
    )

    return consts.STATE_ADMIN


async def admin_panel_handler(update: Update, context: CustomContext):
    if update.effective_user.id not in settings.ADMIN_IDS:
        return consts.STATE_HOME

    text = update.message.text

    if text == keyboards.ADMIN_STAT:
        await update.message.reply_text(
            text=messages.ADMIN_STAT.format(
                request_count=len(context.request_list),
                users_count=len(context.bot_user_ids)
            ),
            reply_markup=keyboards.ADMIN_KEYBOARD,
            quote=True,
        )

        return consts.STATE_ADMIN

    if text == keyboards.ADMIN_GET_FILE:
        if len(context.request_list) == 0:
            await update.message.reply_text(
                text=messages.ADMIN_GET_FILE_NONE,
                reply_markup=keyboards.ADMIN_KEYBOARD,
                quote=True
            )
            return None

        await update.message.reply_text(
            text=messages.ADMIN_GET_FILE_TITLE,
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True
        )

        return consts.STATE_ADMIN_GET_FILE

    if text == keyboards.ADMIN_GET_FILE_ID:
        await update.message.reply_text(
            text=messages.ADMIN_GET_FILE_ID,
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True
        )

        return consts.STATE_ADMIN_FILE_ID

    if text == keyboards.ADMIN_CLEAN_REQUEST_LIST:
        await update.message.reply_text(
            text=messages.ADMIN_CLEAN_REQ_LIST,
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True
        )

        return consts.STATE_ADMIN_CLEAN_REQ


async def admin_send_file_handler(update: Update, context: CustomContext):
    if update.effective_user.id not in settings.ADMIN_IDS:
        return consts.STATE_HOME

    text = update.message.text
    if text == keyboards.BACK:
        return await back_admin(update, context)

    first_index = context.file_last_index
    course_requests = context.request_list
    file_path = write_data_to_sheet(
        f"{text} ({first_index + 1}-{len(course_requests)})",
        text,
        course_requests[first_index:],
        ["A", "B", "C", "D"]
    )
    context.file_last_index = len(course_requests)

    await update.message.reply_document(
        document=file_path,
        reply_markup=keyboards.ADMIN_KEYBOARD,
        quote=True,
    )

    return consts.STATE_ADMIN


async def admin_send_file_id_handler(update: Update, context: CustomContext):
    if update.effective_user.id not in settings.ADMIN_IDS:
        return consts.STATE_HOME

    text = update.message.text
    if text and text == keyboards.BACK:
        return await back_admin(update, context)

    result = await context.bot.send_document(
        chat_id=settings.BACKUP_CH_ID,
        document=update.message.document.file_id
    )

    await update.message.reply_text(
        text=result.document.file_id,
        reply_markup=keyboards.ADMIN_KEYBOARD,
        quote=True,
    )

    return consts.STATE_ADMIN


async def admin_clean_request_list_handler(update: Update, context: CustomContext):
    if update.effective_user.id not in settings.ADMIN_IDS:
        return consts.STATE_HOME

    text = update.message.text
    if text == keyboards.BACK:
        return await back_admin(update, context)

    course_requests = context.request_list
    file_path = write_data_to_sheet(
        f"{text} (1-{len(course_requests)})",
        text,
        course_requests,
        ["A", "B", "C", "D"]
    )
    # Clean list
    context.request_list = []
    context.file_last_index = 0

    await update.message.reply_document(
        document=file_path,
    )

    await update.message.reply_text(
        text=messages.ADMIN_HOME,
        reply_markup=keyboards.ADMIN_KEYBOARD,
        quote=True,
    )

    return consts.STATE_ADMIN
