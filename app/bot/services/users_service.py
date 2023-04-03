import logging

from channels.db import database_sync_to_async
from django.db import IntegrityError

from app.models import Client, Habit

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def create_user(
    user_id: str,
    full_name: str,
    login: str,
    payment_status: bool,
    habits: list[str],
):
    try:
        user = Client.objects.create(
            user_id=user_id,
            full_name=full_name,
            login=login,
            paid=payment_status,
        )

        user.invoice_image = f"documents/invoices/{user_id}.jpg"
        user.save()
        for habit in habits:
            Habit.objects.create(habit_title=habit, user=user)
        logger.info(
            f"Received create_user with parameter user, full_name: {user} {full_name}"
        )
    except IntegrityError as error:
        logger.info(f"Received create_user with parameter IntegrityError: {error}")


@database_sync_to_async
def check_user_exists(user_id):
    return Client.objects.filter(user_id=user_id).exists()
