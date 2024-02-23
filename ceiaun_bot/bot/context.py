from telegram.ext import CallbackContext, ExtBot

from bot import consts


class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
    @property
    def bot_user_ids(self) -> set[int]:
        return self.bot_data.setdefault("user_ids", set())

    @property
    def request_list(self) -> list[list]:
        return self.bot_data.setdefault("request_list", [])

    @request_list.setter
    def request_list(self, value: list) -> None:
        self.bot_data["request_list"] = value

    @property
    def file_last_index(self) -> int:
        return self.bot_data.setdefault("file_last_index", 0)

    @file_last_index.setter
    def file_last_index(self, value: int) -> None:
        self.bot_data["file_last_index"] = value

    @property
    def user_state(self) -> int:
        return self.user_data.setdefault("state", consts.STATE_HOME)

    @user_state.setter
    def user_state(self, value: int) -> None:
        if value is not None:
            self.user_data["state"] = value
