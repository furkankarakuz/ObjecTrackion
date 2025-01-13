from dotenv import load_dotenv
from telegram import Bot
import os

load_dotenv()


class TelegramBot():
    def __init__(self, token: str, chat_id: str) -> None:
        """TelegramBot

        Initialize TelegramBot Class

        Args:
            token (str): TOKEN ID for TelegramBot
            chat_id (str): Message CHAT ID
        """
        self.token = token
        self.chat_id = chat_id
        self.bot = Bot(token=token)

    async def send_message(self, message: str, photo_path: str) -> None:
        """Send Message

        This method sends message(s) for notification

        Args:
            message (str): Message text
            photo_path (str): Photo path
        """
        await self.bot.send_message(chat_id=self.chat_id, text=message)
        await self.bot.send_photo(chat_id=self.chat_id, photo=open(photo_path, 'rb'))


bot = TelegramBot(os.getenv("TOKEN"), os.getenv("CHAT_ID"))
