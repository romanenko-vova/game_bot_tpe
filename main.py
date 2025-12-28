import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler,
)
from config.config import TELEGRAM_TOKEN
from handlers.biba_handlers import biba, say_boba, say_biba
from handlers.talk_handlers import talk_start, talk, say_contact
from handlers.guess_number_handlers import guess_number_start, guess_number
from handlers.tictactoe_handlers import tictactoe_start, tictactoe
from handlers.start_handler import start
from config.states import MAINMENU, TALK, BIBA, GUESS_NUMBER, TICTACTOE

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
                CallbackQueryHandler(biba, pattern="biba"),
                CallbackQueryHandler(talk_start, pattern="talk"),
                CallbackQueryHandler(
                    guess_number_start, pattern="guess_number"
                ),
                CallbackQueryHandler(tictactoe_start, pattern="tictactoe"),
            ],
            TALK: [MessageHandler(filters.TEXT & ~filters.COMMAND, talk)],
            BIBA: [
                MessageHandler(filters.Regex("^биба$"), say_boba),
                MessageHandler(filters.Regex("^боба$"), say_biba),
                MessageHandler(filters.CONTACT, say_contact),
            ],
            GUESS_NUMBER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, guess_number)
            ],
            TICTACTOE: [
                CallbackQueryHandler(tictactoe, pattern="^[0-8]$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    # & - и
    # | - или
    # ~ - не

    application.run_polling()
