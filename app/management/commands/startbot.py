from django.core.management.base import BaseCommand

from app.bot.start_bot import start_telegram_bot


class Command(BaseCommand):
    help = "Displays stats related to Article and Comment models"

    def handle(self, *args, **kwargs):
        start_telegram_bot()
