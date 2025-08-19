import logging

from telegram import Update

from bot import consts, inline_keyboards, keyboards, messages
from bot.consts import SUMMER_REQUEST_COURSES
from bot.context import CustomContext
from utils import generate_summer_request_response, process_summer_course_request

request_logger = logging.getLogger("request_log")
bad_request_logger = logging.getLogger("bad_request_log")


async def summer_request_handler(update: Update, context: CustomContext):
    query = update.callback_query

    if query.data == inline_keyboards.SUMMER_REQUEST_BACK_QUERY or not context.flags["REQUEST_SUMMER_OPEN"]:
        await query.answer()
        await query.edit_message_text(text=messages.SUMMER_REQ_CANCELED)
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text=messages.HOME_SHORT,
            reply_markup=keyboards.HOME_KEYBOARD,
        )

        return consts.STATE_HOME

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
                text=messages.SUMMER_REQ_ONE_SELECTED_AT_LEAST,
                show_alert=True,
            )

            return consts.STATE_SUMMER_REQUEST

        await query.answer()
        await query.edit_message_text(
            text=messages.SUMMER_REQ_GET_STUDENT_INFO,
            reply_markup=inline_keyboards.SUMMER_REQUEST_GET_NAME_KEYBOARD,
        )

        return consts.STATE_SUMMER_REQUEST_GET_NAME


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
        result = await update.message.reply_text(
            text=e.args[0],
            reply_markup=inline_keyboards.SUMMER_REQUEST_GET_NAME_KEYBOARD,
            do_quote=True,
        )
        context.user_last_inline_message = result.message_id

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
        text=messages.SUMMER_REQ_SUCCESS,
        reply_markup=keyboards.HOME_KEYBOARD,
        do_quote=True,
    )
    context.user_last_inline_message = None

    return consts.STATE_HOME
