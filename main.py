import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler,
    PicklePersistence,
)

from config.config import TELEGRAM_TOKEN
from handlers.biba_handlers import biba, say_boba, say_biba
from handlers.talk_handlers import talk_start, talk, say_contact
from handlers.guess_number_handlers import guess_number_start, guess_number
from handlers.tictactoe_handlers import tictactoe_start, tictactoe
from handlers.tictactoe_online import tictactoe_online_start
from handlers.start_handler import start, get_age
from config.states import (
    MAINMENU,
    TALK,
    BIBA,
    GUESS_NUMBER,
    TICTACTOE,
    GET_AGE,
    TICTACTOE_ONLINE,
)
from db.database import create_tables
from handlers.tictactoe_online import tictactoe_online

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


if __name__ == "__main__":
    persistence = PicklePersistence("bot_cache")
    application = (
        ApplicationBuilder()
        .post_init(create_tables)
        .token(TELEGRAM_TOKEN)
        .persistence(persistence)
        .build()
    )

    # handler - обработчик
    # CommandHandler - обработчик команд
    # MessageHandler - обработчик сообщений

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            GET_AGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)
            ],
            MAINMENU: [
                CallbackQueryHandler(biba, pattern="biba"),
                CallbackQueryHandler(talk_start, pattern="talk"),
                CallbackQueryHandler(
                    guess_number_start, pattern="guess_number"
                ),
                CallbackQueryHandler(tictactoe_start, pattern="tictactoe"),
                CallbackQueryHandler(
                    tictactoe_online_start, pattern="online_tictactoe"
                ),
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
            TICTACTOE_ONLINE: [
                CallbackQueryHandler(tictactoe_online, pattern="^[0-8]$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
        persistent=True,
        name="conv_handler",
    )

    application.add_handler(conv_handler)

    # & - и
    # | - или
    # ~ - не
    application.bot_data["queue"] = []
    application.bot_data["games"] = {}
    application.bot_data["last_game_id"] = 0

    application.run_polling()
