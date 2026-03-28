from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import ContextTypes

text_pages = {
    1: "топ игроков крестиков-ноликов",
    2: "Сообщение 2",
    3: "Сообщение 3",
}

async def top_players(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # query - запрос
    query = update.callback_query
    await query.answer()
    
    page = context.user_data["page"]
    
    keyboard = [
        [InlineKeyboardButton("<", callback_data="<")],
        [InlineKeyboardButton(">", callback_data=">")],
    ]
    lst = ['Леха', 'Петя', 'Вася']
    markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=text_pages[page], reply_markup=markup
    )
