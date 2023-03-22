import logging

import telegram
from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def send_about_service_info(query: CallbackQuery, reply_markup):
    await query.edit_message_text(
        """
Бот "Ramadan Tracker" - ваш надежный помощник во время месяца Рамадан.
Пользуйтесь им и сделайте свой Рамадан более осознанным и продуктивным.
        """,
        reply_markup=reply_markup,
    )


async def send_bootcamp_rules_info(query: CallbackQuery, reply_markup):
    await query.edit_message_text(
        """
Формат забега:

1. Участник выбирает 2-3 **привычки** из предоставленного списка.

2. Каждый **вечер** берется отчет о прогрессе дня.

3. Каждую **неделю** же проводятся прямые эфиры, где мы делимся результатами за 7 дней. Таких будет 4 прямых эфира.
 Где вы услышите опыт других участников, зарядитесь мотивацией и взгляните на свои действия под другим углом.

4. Помимо этого в течение дня вас будут радовать **полезными напоминаниями и мотивациями** из хадисов, аятов Корана и
 не только.

5. И конечно же **сообщество** участников, где будет много обсуждений, быстрые вопросы-ответы и многое другое
 полезное для вашей духовности, ин ша Аллах.
""",
        parse_mode=telegram.constants.ParseMode.MARKDOWN,
        reply_markup=reply_markup,
    )


async def send_price_info(query: CallbackQuery, reply_markup):
    await query.edit_message_text(
        """
Тариф "Стандарт".
Стоимость участия - 10 тысяч тенге.

Тариф "Премиум".
Стоимость участия - 30 тысяч тенге.

Он включает в себя все функции тарифа "Стандарт" + 2 индивидуальные онлайн консультации с Чингисом в течение забега.
        """,
        reply_markup=reply_markup,
    )


async def send_ask_question_info(query: CallbackQuery, reply_markup):
    await query.edit_message_text(
        """
Вы можете задать вопрос Чингису напрямую @sadu_chingis
        """,
        reply_markup=reply_markup,
    )


async def send_register_habits_info(
    query: CallbackQuery, context: ContextTypes.DEFAULT_TYPE
):
    button1 = InlineKeyboardButton(
        "Назад 🔙", callback_data="guest/register/get_back_main_menu"
    )

    # Create an InlineKeyboardMarkup object with the buttons
    keyboard = [[button1]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        """""",
        parse_mode=telegram.constants.ParseMode.MARKDOWN,
        reply_markup=reply_markup,
    )

    context.user_data["last_query"] = query
