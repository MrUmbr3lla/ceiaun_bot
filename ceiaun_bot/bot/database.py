import logging

from telegram import User
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


def save_user(context: ContextTypes.DEFAULT_TYPE, effective_user: User) -> None:
    user_id = effective_user.id
    username = effective_user.username
    user_full_name = effective_user.full_name

    user_list = context.bot_data.get("user_list", set())
    if user_id not in user_list:
        logger.info(f"New user: {user_id} / username: @{username} / full name: {user_full_name}")
        user_list.add(user_id)
        context.bot_data["user_list"] = user_list


def get_user_count(context: ContextTypes.DEFAULT_TYPE) -> int:
    return len(context.bot_data.get("user_list", set()))


def get_course_request(context: ContextTypes.DEFAULT_TYPE) -> list:
    return context.bot_data.get("request_list", [])


def save_course_request(context: ContextTypes.DEFAULT_TYPE, request: list) -> None:
    request_list = context.bot_data.get("request_list", [])
    request_list.append(request)
    context.bot_data["request_list"] = request_list


def get_file_last_index(context: ContextTypes.DEFAULT_TYPE) -> int:
    return context.bot_data.get("file_last_index", 0)


def save_file_last_index(context: ContextTypes.DEFAULT_TYPE, last_index: int) -> None:
    context.bot_data["file_last_index"] = last_index
