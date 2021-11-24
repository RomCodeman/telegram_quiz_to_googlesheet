from django.core.management.base import BaseCommand

from bot_app.logger import logger
from config import bot


class Command(BaseCommand):
    help = 'Starts telegram bot'

    def __init__(self):
        super().__init__()

    def handle(self, *args, **options):

        # Launches a Bot on polling
        def main():
            try:
                bot.remove_webhook()
                logger.info(f"Webhook was removed.")
                logger.info(f"Bot has been launched.")
                bot.infinity_polling()
            except Exception as e:
                logger.error(f"Exception is: {e}")

        main()
