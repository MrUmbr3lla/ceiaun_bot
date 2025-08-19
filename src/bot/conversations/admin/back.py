from telegram import Update

from bot import consts, keyboards, messages
from bot.context import CustomContext


async def admin_back_handler(update: Update, context: CustomContext):
    await update.message.reply_text(
        text=messages.ADMIN_HOME,
        do_quote=True,
        reply_markup=keyboards.ADMIN_KEYBOARD,
    )

    return consts.STATE_ADMIN
