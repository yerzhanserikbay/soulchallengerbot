import logging

from telegram import CallbackQuery, Update
from telegram.ext import ContextTypes

from ..inline_keyboards import guest_buttons, user_buttons
from .info_service import (
    send_about_service_info,
    send_ask_question_info,
    send_bootcamp_rules_info,
    send_price_info,
    send_register_habits_info,
)
from .users_service import check_user_exists

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def inline_keyboards_buttons_switcher(
    directory, query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE
):
    logger.info(
        f"Received inline_keyboards_buttons_switcher with parameter directory: {directory}"
    )

    directories = directory.split("/")

    client_path = directories[0]
    type_path = directories[1]
    action_path = directories[2]

    if client_path == "guest":
        if type_path == "register":
            match action_path:
                case "send_register_habits":
                    await send_register_habits_info(query, context)
                case "send_payment":
                    if await check_user_exists(query.from_user.id):
                        text = "Вы уже есть в базе. Ожидайте нашего ответа 🙂"
                        await query.edit_message_text(
                            text=text,
                            reply_markup=guest_buttons.get_main_menu_buttons(),
                        )
                    else:
                        await guest_buttons.send_payment(query, context)
                case "get_back_main_menu":
                    text = (
                        "\nДобро пожаловать в Ramadan Tracker. "
                        "\nПожалуйста, пройдите регистрацию."
                    )
                    await query.edit_message_text(
                        text=text, reply_markup=guest_buttons.get_main_menu_buttons()
                    )
        if type_path == "payment":
            match action_path:
                case "send_payment":
                    await guest_buttons.send_payment(query, context)
                case "check_invoice":
                    pass
        elif type_path == "register_habits":
            match action_path:
                case "check_payment":
                    await guest_buttons.check_payment(query, context)
                case "send_success":
                    await guest_buttons.send_success_registration(query, context)
                case "send_payment":
                    await guest_buttons.send_payment(query, context)
                case "send_change_habits":
                    # clean user_habits
                    context.user_data["user_habits"] = []
                    await send_register_habits_info(query, context)
        elif type_path == "info":
            match action_path:
                case "send_about_service_info":
                    await send_about_service_info(
                        query, guest_buttons.get_main_menu_buttons()
                    )
                case "send_bootcamp_rules_info":
                    await send_bootcamp_rules_info(
                        query, guest_buttons.get_main_menu_buttons()
                    )
                case "send_price_info":
                    await send_price_info(query, guest_buttons.get_main_menu_buttons())
                case "send_ask_question_info":
                    await send_ask_question_info(
                        query, guest_buttons.get_main_menu_buttons()
                    )

    elif client_path == "user":
        if type_path == "qa":
            match action_path:
                case "send_ask_question_info":
                    await send_ask_question_info(
                        query, user_buttons.get_main_menu_buttons()
                    )
        elif type_path == "chat":
            match action_path:
                case "join_chat":
                    text = "Пройдите по ссылке 🙂\nhttps://t.me/+qlrYuSIWX59lZWVi"
                    await query.edit_message_text(
                        text=text, reply_markup=user_buttons.get_main_menu_buttons()
                    )


# Define a function to handle button clicks
async def inline_keyboard_buttons_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()
    await inline_keyboards_buttons_switcher(query.data, query, context)
