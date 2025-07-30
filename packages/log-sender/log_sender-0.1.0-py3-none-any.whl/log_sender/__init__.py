import click
from .senders.telegram_bot_sender import TelegramSender


@click.group()
def send_with(): ...


@send_with.command("telegram")
@click.argument("chat_id", type=click.STRING)
@click.argument("file", type=click.Path(exists=True, dir_okay=False, readable=True))
@click.option("--caption", type=click.STRING, default="")
def main(chat_id: str, file: str, caption: str):
    TelegramSender().send(chat_id, file, caption)
