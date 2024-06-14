import logging

from telegram import InputMediaDocument, Update

import settings
from bot import consts, inline_keyboards, keyboards, messages
from bot.consts import SUMMER_REQUEST_COURSES
from bot.context import CustomContext
from utils import process_course_request
from utils.course_request import generate_summer_request_response, process_summer_course_request

logger = logging.getLogger(__name__)
request_logger = logging.getLogger("request_log")
bad_request_logger = logging.getLogger("bad_request_log")


async def start_command_handler(update: Update, context: CustomContext):
    await update.message.reply_document(
        quote=True,
        document=settings.FILE_HOME_IMAGE,
        reply_markup=keyboards.HOME_KEYBOARD,
        caption=messages.START_COMMAND,
    )

    context.user_state = consts.STATE_HOME


async def back_home(update: Update, context: CustomContext):
    await update.message.reply_text(
        text=messages.HOME_SHORT,
        quote=True,
        reply_markup=keyboards.HOME_KEYBOARD,
    )

    return consts.STATE_HOME


async def home_handler(update: Update, context: CustomContext):
    text = update.message.text

    if text == keyboards.HOME_CHART:
        # Send SE chart
        await context.bot.send_media_group(
            chat_id=update.effective_chat.id,
            media=[
                InputMediaDocument(settings.FILE_SE_CHARTS[0]),
                InputMediaDocument(
                    settings.FILE_SE_CHARTS[1],
                    caption=messages.CHART_SE_CAPTION,
                ),
            ],
        )
        # Send IT charts
        await context.bot.send_media_group(
            chat_id=update.effective_chat.id,
            media=[
                InputMediaDocument(settings.FILE_IT_CHARTS[0]),
                InputMediaDocument(
                    settings.FILE_IT_CHARTS[1],
                    caption=messages.CHART_IT_CAPTION,
                ),
            ],
        )
        # Send orient help
        await update.message.reply_text(
            quote=True,
            text=messages.CHART_SELECT_ORIENT,
            reply_markup=keyboards.HOME_KEYBOARD,
        )

        return consts.STATE_HOME

    # converting courses name
    if text == keyboards.HOME_CONVERT_NAME:
        await update.message.reply_document(
            document=settings.FILE_CONVERT_NAME,
            caption=messages.CONVERT_NAME_COMMAND,
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True,
        )

        return consts.STATE_CONVERT_COURSE

    # students requests
    if text == keyboards.HOME_COURSE_REQUEST:
        await update.message.reply_document(
            document=settings.FILE_COURSE_REQUEST,
            caption=messages.REQ_COMMAND,
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True,
        )

        return consts.STATE_REQUEST_COURSE

    if text == keyboards.HOME_SUMMER_REQUEST:
        context.user_summer_course_status = {course.id: False for course in SUMMER_REQUEST_COURSES}

        await update.message.reply_text(
            text=generate_summer_request_response(context.user_summer_course_status),
            reply_markup=inline_keyboards.generate_summer_request_inline_keyboard(context.user_summer_course_status),
            quote=True,
        )

        return consts.STATE_SUMMER_REQUEST


async def convert_course_handler(update: Update, context: CustomContext):
    text = update.message.text

    if text == keyboards.BACK:
        return await back_home(update, context)

    converted_name = text
    for r in consts.PERCENT_REPLACE:
        converted_name = converted_name.replace(*r)

    result = ""
    for name in converted_name.split("\n"):
        result += f"<code>%{name}%</code>\n"

    await update.message.reply_text(
        text=messages.CONVERT_NAME_RESULT.format(result=result),
        quote=True,
        reply_markup=keyboards.BACK_KEYBOARD,
    )


async def request_course_handler(update: Update, context: CustomContext):
    text = update.message.text
    user_id = update.effective_user.id
    username = update.effective_user.username

    if text == keyboards.BACK:
        return await back_home(update, context)

    try:
        request_list = process_course_request(text)
    except ValueError as e:
        await update.message.reply_text(
            text=e.args[0],
            reply_markup=keyboards.BACK_KEYBOARD,
            quote=True,
        )
        bad_request_logger.info(f"user {user_id} with username @{username} has bad request with id {e.args[1]}: {text}")
        return None

    request_logger.info(f"user {user_id} with username @{username} has request: {','.join(request_list)}")
    context.request_list.append(request_list)

    await update.message.reply_text(
        text=messages.REQ_RECEIVED_REQ,
        reply_markup=keyboards.BACK_KEYBOARD,
        quote=True,
    )


async def summer_request_handler(update: Update, context: CustomContext):
    query = update.callback_query

    if query.data.startswith("course"):
        course_id = int(query.data.replace("course-", ""))
        course_status = context.user_summer_course_status
        course_status[course_id] = not course_status[course_id]

        await query.answer()
        await query.edit_message_text(
            text=generate_summer_request_response(course_status),
            reply_markup=inline_keyboards.generate_summer_request_inline_keyboard(course_status),
        )

        return consts.STATE_SUMMER_REQUEST

    if query.data == inline_keyboards.SUMMER_REQUEST_ACCEPT_QUERY:
        if not any(value for value in context.user_summer_course_status.values()):
            await query.answer(
                text="حداقل یکی از دروس را انتخاب کنید!",
                show_alert=True,
            )

            return consts.STATE_SUMMER_REQUEST

        await query.answer()
        await query.edit_message_text(
            text="نام و نام خانوادگی خود را به همراه شماره دانشجویی به فرمت زیر ارسال کنید:",
            reply_markup=inline_keyboards.SUMMER_REQUEST_GET_NAME_KEYBOARD,
        )

        return consts.STATE_SUMMER_REQUEST_GET_NAME

    if query.data == inline_keyboards.SUMMER_REQUEST_BACK_QUERY:
        await query.answer()
        await query.edit_message_text(text="درخواست لفو شد.")
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text=messages.HOME_SHORT,
            reply_markup=keyboards.HOME_KEYBOARD,
        )

        return consts.STATE_HOME


async def summer_request_get_name_handler(update: Update, context: CustomContext):
    query = update.callback_query
    if query and query.data == inline_keyboards.SUMMER_REQUEST_BACK_QUERY:
        await query.answer()
        await query.edit_message_text(
            text=generate_summer_request_response(context.user_summer_course_status),
            reply_markup=inline_keyboards.generate_summer_request_inline_keyboard(context.user_summer_course_status),
        )

        return consts.STATE_SUMMER_REQUEST

    if not update.message:
        return None

    text = update.message.text
    user_id = update.effective_user.id
    username = update.effective_user.username
    try:
        student_info = process_summer_course_request(text)
    except ValueError as e:
        await update.message.reply_text(
            text=e.args[0],
            reply_markup=inline_keyboards.SUMMER_REQUEST_GET_NAME_KEYBOARD,
            quote=True,
        )
        bad_request_logger.info(
            f"user {user_id} with username @{username} has bad summer request with id {e.args[1]}: {text}"
        )

        return consts.STATE_SUMMER_REQUEST_GET_NAME

    for course in SUMMER_REQUEST_COURSES:
        if not context.user_summer_course_status[course.id]:
            continue

        request_list = [*student_info, course.name]
        request_logger.info(f"user {user_id} with username @{username} has summer request: {','.join(request_list)}")
        context.summer_request_list.append(request_list)

    await update.message.reply_text(
        text="درخواست دریافت شد. توجه کنید که درخواست های تکراری حذف خواهند شد.",
        reply_markup=keyboards.HOME_KEYBOARD,
        quote=True,
    )

    return consts.STATE_HOME
