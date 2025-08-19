from telegram import Update

import settings
from bot import consts, keyboards
from bot.context import CustomContext

from .back import admin_back_handler


async def get_file_id_handler(update: Update, context: CustomContext):
    if update.effective_user.id not in settings.ADMIN_IDS:
        return consts.STATE_HOME

    text = update.message.text
    if text and text == keyboards.BACK:
        return await admin_back_handler(update, context)

    result = await context.bot.send_document(
        chat_id=settings.BACKUP_CH_ID,
        document=update.message.document.file_id,
    )

    await update.message.reply_text(
        text=result.document.file_id,
        reply_markup=keyboards.ADMIN_KEYBOARD,
        do_quote=True,
    )

    return consts.STATE_ADMIN
