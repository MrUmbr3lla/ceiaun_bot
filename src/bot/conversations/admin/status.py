from telegram import Update

import settings
from bot import consts, inline_keyboards, keyboards, messages
from bot.context import CustomContext


async def status_handler(update: Update, context: CustomContext):
    query = update.callback_query

    if update.effective_user.id not in settings.ADMIN_IDS:
        return consts.STATE_HOME

    if query.data == inline_keyboards.ADMIN_STATUS_BACK_QUERY:
        await query.answer()
        await query.edit_message_text(text=messages.ADMIN_STATUS_CLOSED)
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text=messages.ADMIN_HOME,
            reply_markup=keyboards.ADMIN_KEYBOARD,
        )

        return consts.STATE_ADMIN

    if query.data.startswith("ad-status-"):
        status_key = query.data.replace("ad-status-", "")
        context.set_flag(status_key, not context.flags[status_key])  # type: ignore

        await query.answer()
        await query.edit_message_reply_markup(
            reply_markup=inline_keyboards.generate_admin_status_inline_keyboard(context.flags),
        )

        return consts.STATE_ADMIN_STATUS
