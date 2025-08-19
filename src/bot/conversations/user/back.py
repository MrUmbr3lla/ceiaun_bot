from telegram import Update

from bot import consts, keyboards, messages
from bot.context import CustomContext


async def back_home_handler(update: Update, context: CustomContext):
    await update.message.reply_text(
        text=messages.HOME_SHORT,
        do_quote=True,
        reply_markup=keyboards.HOME_KEYBOARD,
    )

    return consts.STATE_HOME
