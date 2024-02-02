import logging
import os.path

from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler,
    PersistenceInput, PicklePersistence, filters
)

import settings
from bot import conversations, keyboards, states
from utils import create_new_sheet

logger = logging.getLogger(__name__)


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

    # Conversations
    all_keyboards = (
        f"^({keyboards.HOME_COURSE_REQUEST}|{keyboards.HOME_CONVERT_NAME}|{keyboards.HOME_CHART}|{keyboards.BACK})$"
    )
    main_conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", conversations.start_handler),
            MessageHandler(
                filters.TEXT & filters.Regex(all_keyboards),
                conversations.start_handler
            )
        ],
        states={
            states.HOME: [
                MessageHandler(filters.TEXT, conversations.home_handler)
            ],
            states.REQUEST_COURSE: [
                MessageHandler(filters.TEXT & ~filters.Regex(f"^{keyboards.BACK}$"),
                               conversations.request_course_handler)
            ],
            states.CONVERT_COURSE: [
                MessageHandler(filters.TEXT & ~filters.Regex(f"^{keyboards.BACK}$"),
                               conversations.convert_course_handler)
            ],
        },
        fallbacks=[
            MessageHandler(filters.TEXT, conversations.start_handler),
        ],
        name="main_conv",
        persistent=True
    )

    app.add_handlers([
        CommandHandler("start", conversations.start_handler),
        main_conv,
    ])

    # Errors
    app.add_error_handler(error)

    app.run_polling()


if __name__ == "__main__":
    # TODO: Delete this
    if not os.path.exists(settings.EXCEL_TEMP_FILE):
        create_new_sheet("temp")

    run()
