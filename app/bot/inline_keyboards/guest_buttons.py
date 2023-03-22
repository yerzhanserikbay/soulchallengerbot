import logging

import telegram
from asgiref.sync import sync_to_async
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from ..services.users_service import create_user

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

INVOICE_IMAGE_HANDLER = False


def get_main_menu_buttons():
    button1 = InlineKeyboardButton(
        "Пройти регистрацию 🚀", callback_data="guest/register/send_payment"
    )
    button2 = InlineKeyboardButton(
        "О Ramadan Tracker? ⁉️", callback_data="guest/info/send_about_service_info"
    )
    button3 = InlineKeyboardButton(
        "Как проходит забег? 🏃🏻‍♀️", callback_data="guest/info/send_bootcamp_rules_info"
    )
    button4 = InlineKeyboardButton(
        "Сколько стоит? 🤑", callback_data="guest/info/send_price_info"
    )
    button5 = InlineKeyboardButton(
        "Задать вопрос 🙋🏻", callback_data="guest/info/send_ask_question_info"
    )

    # Create an InlineKeyboardMarkup object with the buttons
    keyboard = [[button1], [button2], [button3], [button4], [button5]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    return reply_markup


async def send_payment(update, context: ContextTypes.DEFAULT_TYPE):
    text = """
Для оплаты:
1. Отправьте 7 000 тенге на KASPI по номеру +7 705 570 18 04 Чингис С.
\nЛибо по номеру карты 4400 4301 7722 9587 CHINGIS SADUYEV
\n2. Сохранив чек о переводе, отправьте его сюда в качестве фото.
    """

    button1 = InlineKeyboardButton(
        "Назад 🔙", callback_data="guest/register/get_back_main_menu"
    )

    keyboard = [[button1]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.user_data["last_query"] = update

    await update.edit_message_text(text=text, reply_markup=reply_markup)


# Define the callback functions for each state
async def habit_message_handler(update, context):
    message_text = update.message.text
    # Do something with the message text...
    context.user_data["message_text"] = message_text
    split_message_text = message_text.split("\n\n")

    if split_message_text[0].upper() != "МОИ ПРИВЫЧКИ":
        return await update.message.reply_text(
            "Простите, попробуйте еще раз написать по формату выше."
        )
    else:
        reply_text = f"""
Ваши привычки:
1. {split_message_text[1].replace("1 ", "")}
2. {split_message_text[2].replace("2 ", "")}
        """
        button1 = InlineKeyboardButton(
            "Верно", callback_data="guest/register_habits/send_success"
        )
        button2 = InlineKeyboardButton(
            "Хочу исправить", callback_data="guest/register_habits/send_change_habits"
        )
        button3 = InlineKeyboardButton(
            "Назад 🔙", callback_data="guest/register/get_back_main_menu"
        )

        keyboard = [[button1], [button2], [button3]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        last_query = context.user_data["last_query"]

        context.user_data["user_habits"] = [
            split_message_text[1].replace("1 ", ""),
            split_message_text[2].replace("2 ", ""),
        ]

        await last_query.edit_message_text(
            text=reply_text,
            parse_mode=telegram.constants.ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

        chat_id = update.message.chat_id
        message_id = update.message.message_id

        # Delete the user's last message
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)


async def invoice_image_handler(update, context):
    user = update.message.from_user
    chat_id = update.message.chat_id
    message_id = update.message.message_id

    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive(f"documents/invoices/{chat_id}.jpg")

    # Delete the user's last message
    await context.bot.delete_message(chat_id=chat_id, message_id=message_id)

    last_query = context.user_data["last_query"]
    reply_text = (
        "Поздравляем Вас 🥳"
        "\nПосле подтверждения оплаты, к вам придет сообщение с приглашением в канал забега."
    )

    button2 = InlineKeyboardButton(
        "О Ramadan Tracker? ⁉️", callback_data="guest/info/send_about_service_info"
    )
    button3 = InlineKeyboardButton(
        "Как проходит забег? 🏃🏻‍♀️", callback_data="guest/info/send_bootcamp_rules_info"
    )
    button4 = InlineKeyboardButton(
        "Сколько стоит? 🤑", callback_data="guest/info/send_price_info"
    )
    button5 = InlineKeyboardButton(
        "Задать вопрос 🙋🏻", callback_data="guest/info/send_ask_question_info"
    )

    # Create an InlineKeyboardMarkup object with the buttons
    keyboard = [[button2], [button3], [button4], [button5]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    user_fullname = f"{user.first_name} {user.last_name}"

    # user_habits = context.user_data["user_habits"]
    user_habits = []

    sync_to_async(
        await create_user(
            user_id=chat_id,
            full_name=user_fullname,
            login=user.username,
            payment_status=False,
            habits=user_habits,
        )
    )

    await last_query.edit_message_text(text=reply_text, reply_markup=reply_markup)
