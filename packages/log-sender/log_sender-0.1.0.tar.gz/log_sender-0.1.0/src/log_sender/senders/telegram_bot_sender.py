import os
import niquests
from .exceptions import MissingEnvironmentVariable, BadResponseFromTelegramAPI


class TelegramSender:
    def __init__(self) -> None:
        required_env_vars = ["TELEGRAM_BOT_TOKEN"]
        for var in required_env_vars:
            value = os.environ.get("TELEGRAM_BOT_TOKEN")
            if not value:
                raise MissingEnvironmentVariable(var)

    def send(self, chat_id: str, file_path: str, caption: str) -> None:
        res = niquests.post(
            f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendDocument",
            files={"document": open(file_path, "rb")},
            data={"caption": caption, "chat_id": chat_id},
            stream=True,
        )

        if res.status_code != 200:
            raise BadResponseFromTelegramAPI(res.text)
