import logging

from telegram import Update
from telegram.ext import ContextTypes

from ..inline_keyboards import guest_buttons, user_buttons
from ..services.users_service import check_user_exists

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user

    if await check_user_exists(user.id):
        user = update.message.from_user
        text = (
            f"Салем, {user.first_name} {user.last_name}! "
            f"\nС возвращением в Ramadan Tracker."
        )
        await context.bot.send_message(
            chat_id=update.message.chat.id,
            text=text,
            reply_markup=user_buttons.get_main_menu_buttons(),
        )
    else:
        user = update.message.from_user
        text = (
            f"Салем, {user.first_name} {user.last_name}!"
            f"\nДобро пожаловать в Ramadan Tracker. "
            f"\nПожалуйста, пройдите регистрацию."
        )

        context.user_data["user_fullname"] = f"{user.first_name} {user.last_name}"
        context.user_data["user_login"] = user.username

        await context.bot.send_message(
            chat_id=update.message.chat.id,
            text=text,
            reply_markup=guest_buttons.get_main_menu_buttons(),
        )
