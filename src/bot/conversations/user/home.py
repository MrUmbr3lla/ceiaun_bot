from telegram import Update

import settings
from bot import consts, inline_keyboards, keyboards, messages
from bot.consts import SUMMER_REQUEST_COURSES
from bot.context import CustomContext
from utils import generate_summer_request_response


async def home_handler(update: Update, context: CustomContext):
    text = update.message.text

    # if text == keyboards.HOME_CHART:
    #     # Send SE chart
    #     await context.bot.send_media_group(
    #         chat_id=update.effective_chat.id,
    #         media=[
    #             InputMediaDocument(settings.FILE_SE_CHARTS[0]),
    #             InputMediaDocument(
    #                 settings.FILE_SE_CHARTS[1],
    #                 caption=messages.CHART_SE_CAPTION,
    #             ),
    #         ],
    #     )
    #     # Send IT charts
    #     await context.bot.send_media_group(
    #         chat_id=update.effective_chat.id,
    #         media=[
    #             InputMediaDocument(settings.FILE_IT_CHARTS[0]),
    #             InputMediaDocument(
    #                 settings.FILE_IT_CHARTS[1],
    #                 caption=messages.CHART_IT_CAPTION,
    #             ),
    #         ],
    #     )
    #     # Send orient help
    #     await update.message.reply_text(
    #         do_quote=True,
    #         text=messages.CHART_SELECT_ORIENT,
    #         reply_markup=keyboards.HOME_KEYBOARD,
    #     )
    #
    #     return consts.STATE_HOME

    # converting courses name
    if text == keyboards.HOME_CONVERT_NAME:
        await update.message.reply_document(
            document=settings.FILE_CONVERT_NAME,
            caption=messages.CONVERT_NAME_COMMAND,
            reply_markup=keyboards.BACK_KEYBOARD,
            do_quote=True,
        )

        return consts.STATE_CONVERT_COURSE

    # students requests
    if text == keyboards.HOME_COURSE_REQUEST:
        if not context.flags["REQUEST_OPEN"]:
            await update.message.reply_text(
                text=messages.REQ_CLOSE,
                reply_markup=keyboards.HOME_KEYBOARD,
                do_quote=True,
            )

            return None

        await update.message.reply_document(
            document=settings.FILE_COURSE_REQUEST,
            caption=messages.REQ_COMMAND,
            reply_markup=keyboards.BACK_KEYBOARD,
            do_quote=True,
        )

        return consts.STATE_REQUEST_COURSE

    if text == keyboards.HOME_SUMMER_REQUEST:
        if not context.flags["REQUEST_SUMMER_OPEN"]:
            await update.message.reply_text(
                text=messages.SUMMER_REQ_CLOSED,
                reply_markup=keyboards.HOME_KEYBOARD,
                do_quote=True,
            )

            return None

        context.user_summer_course_status = {course.id: False for course in SUMMER_REQUEST_COURSES}

        result = await update.message.reply_text(
            text=generate_summer_request_response(context.user_summer_course_status),
            reply_markup=inline_keyboards.generate_summer_request_inline_keyboard(context.user_summer_course_status),
            do_quote=True,
        )
        context.user_last_inline_message = result.message_id

        return consts.STATE_SUMMER_REQUEST
