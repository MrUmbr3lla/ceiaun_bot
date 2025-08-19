from telegram import Update

from bot import consts, keyboards, messages
from bot.context import CustomContext


async def start_command_handler(update: Update, context: CustomContext):
    await update.message.reply_text(
        text=messages.ADMIN_HOME,
        reply_markup=keyboards.ADMIN_KEYBOARD,
        do_quote=True,
    )

    context.user_data["state"] = consts.STATE_ADMIN
