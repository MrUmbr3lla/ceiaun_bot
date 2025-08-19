from telegram import Update

from bot import consts, keyboards, messages
from bot.context import CustomContext

from .back import back_home_handler


async def convert_course_handler(update: Update, context: CustomContext):
    text = update.message.text

    if text == keyboards.BACK:
        return await back_home_handler(update, context)

    converted_name = text
    for r in consts.PERCENT_REPLACE:
        converted_name = converted_name.replace(*r)

    result = ""
    for name in converted_name.split("\n"):
        result += f"<code>%{name}%</code>\n"

    await update.message.reply_text(
        text=messages.CONVERT_NAME_RESULT.format(result=result),
        do_quote=True,
        reply_markup=keyboards.BACK_KEYBOARD,
    )
