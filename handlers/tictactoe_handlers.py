from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config.states import TICTACTOE


async def tictactoe_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Йоу"""
    query = update.callback_query  # Полная информация о нажатой кнопке
    await query.answer()  # отвечаем на запрос
    context.user_data["lst"] = [
        "⬜",
        "⬜️",
        "⬜️",
        "⬜️",
        "⬜️",
        "⬜️",
        "⬜️",
        "⬜️",
        "⬜️",
    ]
    lst = context.user_data["lst"]  # Получаем список из user_data
    keyboard = [
        [
            InlineKeyboardButton(lst[0], callback_data="0"),
            InlineKeyboardButton(lst[1], callback_data="1"),
            InlineKeyboardButton(lst[2], callback_data="2"),
        ],
        [
            InlineKeyboardButton(lst[3], callback_data="3"),
            InlineKeyboardButton(lst[4], callback_data="4"),
            InlineKeyboardButton(lst[5], callback_data="5"),
        ],
        [
            InlineKeyboardButton(lst[6], callback_data="6"),
            InlineKeyboardButton(lst[7], callback_data="7"),
            InlineKeyboardButton(lst[8], callback_data="8"),
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Игра Крестики-нолики. Ты играешь за крестики, я за нолики. Нажми на кнопку, чтобы начать игру.",
        reply_markup=markup,
    )
    return TICTACTOE


async def tictactoe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Йоу"""
    query = update.callback_query
    await query.answer()

    nomer_knopki = int(query.data)
    lst = context.user_data["lst"]
    lst[nomer_knopki] = "❌"
    # победа
    if lst[0] == lst[1] == lst[2]:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Ты победил!",
        )
    # игра продолжается
    keyboard = [
        [
            InlineKeyboardButton(lst[0], callback_data="0"),
            InlineKeyboardButton(lst[1], callback_data="1"),
            InlineKeyboardButton(lst[2], callback_data="2"),
        ],
        [
            InlineKeyboardButton(lst[3], callback_data="3"),
            InlineKeyboardButton(lst[4], callback_data="4"),
            InlineKeyboardButton(lst[5], callback_data="5"),
        ],
        [
            InlineKeyboardButton(lst[6], callback_data="6"),
            InlineKeyboardButton(lst[7], callback_data="7"),
            InlineKeyboardButton(lst[8], callback_data="8"),
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Ход ноликов.",
        reply_markup=markup,
    )
