import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler
)
from config.config import TELEGRAM_TOKEN
from handlers.biba_handlers import biba, say_boba, say_biba
from handlers.talk_handlers import talk_start, talk, say_contact
from handlers.start_handler import start
from config.states import MAINMENU, TALK, BIBA

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # handler - обработчик
    # CommandHandler - обработчик команд
    # MessageHandler - обработчик сообщений

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAINMENU: [
                CommandHandler("talk", talk_start),
                CommandHandler("biba", biba),
                CallbackQueryHandler(biba, pattern="biba"),
                CallbackQueryHandler(talk_start, pattern="talk"),
            ],
            TALK: [MessageHandler(filters.TEXT & ~filters.COMMAND, talk)],
            BIBA: [
                MessageHandler(filters.Regex("^биба$"), say_boba),
                MessageHandler(filters.Regex("^боба$"), say_biba),
                MessageHandler(filters.CONTACT, say_contact),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    # & - и
    # | - или
    # ~ - не

    application.run_polling()
