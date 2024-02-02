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
