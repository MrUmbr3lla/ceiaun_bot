from telegram import Update

import settings
from bot import consts, keyboards, messages
from bot.context import CustomContext


async def start_command_handler(update: Update, context: CustomContext):
    await update.message.reply_document(
        do_quote=True,
        document=settings.FILE_HOME_IMAGE,
        reply_markup=keyboards.HOME_KEYBOARD,
        caption=messages.START_COMMAND,
    )

    context.user_state = consts.STATE_HOME
