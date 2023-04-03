import logging

from asgiref.sync import async_to_sync

from app.bot.inline_keyboards.user_buttons import send_habit_checker_to_client
from app.models import Client
from config.celery import app

logger = logging.getLogger(__name__)


@app.task
def habits_notification():
    clients = Client.objects.all()
    for client in clients:
        async_to_sync(send_habit_checker_to_client)(client.user_id, client.habit.all())
        logger.info(
            f"Received habits_notification with parameter client.user_id: {client.user_id}"
        )
