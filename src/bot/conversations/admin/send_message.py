import logging

from telegram import Update

import settings
from bot import consts, keyboards, messages
from bot.context import CustomContext

from .back import admin_back_handler

logger = logging.getLogger(__name__)


async def send_message_to_user_handler(update: Update, context: CustomContext):
    if update.effective_user.id not in settings.ADMIN_IDS:
        return consts.STATE_HOME

    text = update.message.text
    if text == keyboards.BACK:
        return await admin_back_handler(update, context)

    try:
        text_split = text.split("\n")
        for_user_id = int(text_split[0])
        for_user_message = "\n".join(text_split[1:])

        result = await context.bot.send_message(
            chat_id=for_user_id,
            text=messages.ADMIN_SEND_MSG_TEMPLATE.format(message=for_user_message),
        )
        result_message = messages.ADMIN_SEND_MSG_SUCCESS.format(
            user=f"<a href='tg://user?id={for_user_id}'>{for_user_id}</a>",
            message_id=result.id,
            name=result.chat.full_name,
            username=result.chat.username,
        )
    except Exception as e:
        result_message = str(e)

    await update.message.reply_text(
        text=result_message,
        reply_markup=keyboards.ADMIN_KEYBOARD,
        do_quote=True,
    )

    return consts.STATE_ADMIN


async def send_message_to_all_handler(update: Update, context: CustomContext):
    if update.effective_user.id not in settings.ADMIN_IDS:
        return consts.STATE_HOME

    text = update.message.text
    if text == keyboards.BACK:
        return await admin_back_handler(update, context)

    for chat_id in context.bot_user_ids:
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=text,
            )
        except Exception as e:
            logger.error(f"send to all error for user {chat_id}: {e}")

    await update.message.reply_text(
        text=messages.ADMIN_HOME,
        do_quote=True,
        reply_markup=keyboards.ADMIN_KEYBOARD,
    )

    return consts.STATE_ADMIN
