import logging

from channels.db import database_sync_to_async
from django.db import DatabaseError, IntegrityError

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


@database_sync_to_async
def get_user_habits(user_id):
    return Habit.objects.filter(user__user_id=user_id).all()


@database_sync_to_async
def set_habit_score(habit_id, habit_score):
    try:
        habit = Habit.objects.get(id=habit_id)
        habit.habit_score += int(habit_score)
        habit.save()
        return True

    except (IntegrityError, DatabaseError) as error:
        logger.info(f"Received set_habit_score with parameter error: {error}")
        return False


def get_my_stats(user_id):
    pass
