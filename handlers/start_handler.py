from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes
)
from config.states import MAINMENU
from db.user_crud import add_user, get_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update - полная информация о том, что произошло
    # update.effective_chat - вся инфа о чате
    # update.effective_user - вся инфа о пользователе
    # update.effective_message - вся инфа о сообщении
    # update.effective_message.text - текст сообщения
    
    user = await get_user(update.effective_user.id)
    print(user)
    print(user['id'], user['tg_id'], user['name'])
    if not user:
        await add_user(update.effective_user.id)
    
    keyboard = [
        [InlineKeyboardButton("Режим разговора", callback_data="talk")],
        [InlineKeyboardButton("Режим бибы", callback_data="biba")],
        [InlineKeyboardButton("Игра 'Бот угадывает число'", callback_data="guess_number")],
        [InlineKeyboardButton("Игра 'Крестики-нолики'", callback_data="tictactoe")],
        [InlineKeyboardButton("Крестики Нолики по сети", callback_data="online_tictactoe")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    context.user_data['previous_messages'] = []
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Привет {update.effective_user.first_name}!\n\nНапиши команду:\n /talk чтобы поговорить со мной.\n /biba чтобы получить бобу.",
        reply_markup=markup
    )
    return MAINMENU