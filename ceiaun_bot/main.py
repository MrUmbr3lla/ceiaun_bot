import logging

from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes, MessageHandler,
    PersistenceInput, PicklePersistence, filters
)

import settings
from bot import conversations, states

logger = logging.getLogger(__name__)

CONVS = {
    # User
    states.HOME: conversations.home_handler,
    states.REQUEST_COURSE: conversations.request_course_handler,
    states.CONVERT_COURSE: conversations.convert_course_handler,

    # Admin
    states.ADMIN: conversations.admin_panel_handler,
    states.ADMIN_GET_FILE: conversations.admin_send_file_handler
}


async def state_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_state = context.user_data.get("state", states.HOME)
    logger.info(f"user {update.effective_user.id} state: {user_state}")
    result = await CONVS[user_state](update, context)
    context.user_data["state"] = result if result is not None else user_state
    logger.info(f"user {update.effective_user.id} after state: {result}")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.warning(f"Error for update {update} caused error {context.error}")


def run():
    # Persistent data
    persistence = PicklePersistence(
        filepath=settings.BOT_DATABASE_DIR / "bot",
        store_data=PersistenceInput(chat_data=False, callback_data=False),
        single_file=False,
        update_interval=settings.BOT_DATABASE_UPDATE_INTERVAL
    )

    app = Application.builder().token(settings.BOT_TOKEN).persistence(persistence).build()

    admin_filter = filters.User(user_id=int(settings.ADMIN_IDS[0]))

    app.add_handlers([
        CommandHandler("start", conversations.start_command_handler),
        CommandHandler("panel", conversations.admin_start_command_handler, filters=admin_filter),

        MessageHandler(filters.TEXT, state_handler)
    ])

    # Errors
    app.add_error_handler(error)

    app.run_polling()


if __name__ == "__main__":
    run()
