import logging

import environ
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from ..services.users_service import get_user_habits

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

env = environ.Env()


def get_main_menu_buttons():
    button1 = InlineKeyboardButton(
        "Мои привычки 🚀", callback_data="user/profile/send_user_habits"
    )
    button2 = InlineKeyboardButton(
        "Мой прогресс 📈", callback_data="user/profile/send_user_stats"
    )
    button4 = InlineKeyboardButton("Войти в чат 💬", callback_data="user/chat/join_chat")
    button5 = InlineKeyboardButton(
        "Задать вопрос 🙋🏻", callback_data="user/qa/send_ask_question_info"
    )

    # Create an InlineKeyboardMarkup object with the buttons
    keyboard = [[button1], [button2], [button4], [button5]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    return reply_markup


async def send_user_habits(update, context):
    user_id = update.message.chat_id
    habits = await get_user_habits(user_id=user_id)
    habit_score_list = ""
    for habit in habits:
        habit_score_list += f"\n{habit.habit_score if habit.habit_score else 0} points: {habit.habit_title}"

    reply_text = f"""
Ваши привычки:
{habit_score_list}
    """

    await update.edit_message_text(
        text=reply_text, reply_markup=get_main_menu_buttons()
    )


async def send_user_stats(update, context):
    reply_text = "Скоро будет 🥹"
    await update.edit_message_text(
        text=reply_text, reply_markup=get_main_menu_buttons()
    )


async def send_habit_accepted(update, context):
    reply_text = "✨"

    await update.edit_message_text(
        text=reply_text, reply_markup=get_main_menu_buttons()
    )


async def send_message_to_client(user_id, text, reply_markup=None):
    bot = telegram.Bot(token=env.str("TELEGRAM_BOT_TOKEN", ""))
    await bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)


async def send_habit_checker_to_client(user_id: int, habits):
    bot = telegram.Bot(token=env.str("TELEGRAM_BOT_TOKEN", ""))
    logger.info(
        f"Received send_habit_checker_to_client with parameter user_id: {user_id}"
    )

    for habit in habits:
        button1 = InlineKeyboardButton(
            "1️⃣", callback_data=f"user/set_habit_score/1-{habit.id}"
        )
        button2 = InlineKeyboardButton(
            "2️⃣", callback_data=f"user/set_habit_score/2-{habit.id}"
        )
        button3 = InlineKeyboardButton(
            "3️⃣", callback_data=f"user/set_habit_score/3-{habit.id}"
        )
        button4 = InlineKeyboardButton(
            "4️⃣", callback_data=f"user/set_habit_score/4-{habit.id}"
        )
        button5 = InlineKeyboardButton(
            "5️⃣", callback_data=f"user/set_habit_score/5-{habit.id}"
        )

        keyboard = [[button1], [button2], [button3], [button4], [button5]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        text = f"Оцените привычку: \n{habit.habit_title}"
        await bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
