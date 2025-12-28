from telegram import (
    Update,
    ReplyKeyboardMarkup,
)
from telegram.ext import ContextTypes
from config.states import GUESS_NUMBER


async def guess_number_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Я загадал число от 1 до 100. Попробуй угадать его.",
    )
    keyboard = [["больше"], ["меньше"], ["угадал"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="50?",
        reply_markup=markup,
    )
    # context.user_data — хранится информация отдельная для каждого пользователя
    # context.chat_data — хранится информация общая для всех пользователей в чате
    # context.bot_data — хранится информация общая для всех пользователей
    context.user_data["start"] = 1
    context.user_data["end"] = 128
    context.user_data["mid"] = (
        context.user_data["start"] + context.user_data["end"]
    ) // 2
    return GUESS_NUMBER


async def guess_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    keyboard = [["больше"], ["меньше"], ["угадал"]]
    markup = ReplyKeyboardMarkup(keyboard)
    if text == "больше":
        context.user_data["start"] = context.user_data["mid"]
        context.user_data["mid"] = (
            context.user_data["start"] + context.user_data["end"]
        ) // 2
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{context.user_data['mid']}?",
            reply_markup=markup,
        )
    elif text == "меньше":
        pass
    elif text == "угадал":
        pass
