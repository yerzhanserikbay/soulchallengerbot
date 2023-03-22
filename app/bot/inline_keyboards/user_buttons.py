import logging

import environ
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

env = environ.Env()


def get_main_menu_buttons():
    # button1 = InlineKeyboardButton(
    #     "Мои привычки 🚀", callback_data="user/profile/send_my_habits"
    # )
    # button2 = InlineKeyboardButton(
    #     "Мой прогресс 📈", callback_data="user/profile/send_my_stats"
    # )
    button4 = InlineKeyboardButton("Войти в чат 💬", callback_data="user/chat/join_chat")
    button5 = InlineKeyboardButton(
        "Задать вопрос 🙋🏻", callback_data="user/qa/send_ask_question_info"
    )

    # Create an InlineKeyboardMarkup object with the buttons
    # keyboard = [[button1], [button2], [button4], [button5]]
    keyboard = [[button4], [button5]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    return reply_markup


async def send_message_to_client(user_id):
    bot = telegram.Bot(token=env.str("TELEGRAM_BOT_TOKEN", ""))

    await bot.send_message(
        chat_id=user_id, text="Ваша заявка одобрена, для старта нишите команду /start"
    )
