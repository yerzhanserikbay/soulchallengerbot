import logging
import re

import environ
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from .commands.help_command import help_command
from .commands.start_command import start_command
from .inline_keyboards.guest_buttons import habit_message_handler, invoice_image_handler
from .services.inline_keyboard_service import inline_keyboard_buttons_handler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

env = environ.Env()


def start_telegram_bot() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(env.str("TELEGRAM_BOT_TOKEN", "")).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    # application.add_handler(conversation_handler)
    application.add_handler(MessageHandler(filters.PHOTO, invoice_image_handler))
    application.add_handler(
        MessageHandler(
            filters.Regex(re.compile(r"^Мои привычки$", re.MULTILINE)),
            habit_message_handler,
        )
    )

    # Add a callback query handler for button clicks
    application.add_handler(CallbackQueryHandler(inline_keyboard_buttons_handler))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()
