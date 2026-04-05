from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes, ConversationHandler
from config.states import MAINMENU, GET_AGE
from db.user_crud import add_user, get_user, update_age


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update - полная информация о том, что произошло
    # update.effective_chat - вся инфа о чате
    # update.effective_user - вся инфа о пользователе
    # update.effective_message - вся инфа о сообщении
    # update.effective_message.text - текст сообщения

    user = await get_user(update.effective_user.id)
    print(user)
    # guard statement - если пользователь не найден, то запрашиваем возраст
    if not user:
        user = await add_user(update.effective_user.id, update.effective_user.first_name)
    if not user["age"]:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Привет! Сколько тебе лет?"
        )
        return GET_AGE
    
    if user["age"] > 15:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Атстань, Скуф!"
        )
        return ConversationHandler.END

    keyboard = [
        [InlineKeyboardButton("Режим разговора", callback_data="talk")],
        [InlineKeyboardButton("Режим бибы", callback_data="biba")],
        [
            InlineKeyboardButton(
                "Игра 'Бот угадывает число'", callback_data="guess_number"
            )
        ],
        [
            InlineKeyboardButton(
                "Игра 'Крестики-нолики'", callback_data="tictactoe"
            )
        ],
        [
            InlineKeyboardButton(
                "Крестики Нолики по сети", callback_data="online_tictactoe"
            )
        ],
        [InlineKeyboardButton("Топ игроков", callback_data="top_players")],
        [InlineKeyboardButton('кнопка webapp', web_app=WebAppInfo('https://e5f5-2405-4802-e686-4e00-d87e-dc0c-b954-9dfa.ngrok-free.app'))]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    context.user_data["previous_messages"] = []
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Привет {update.effective_user.first_name}!\n\nНапиши команду:\n /talk чтобы поговорить со мной.\n /biba чтобы получить бобу.",
        reply_markup=markup,
    )
    
    context.user_data["page"] = 1
    return MAINMENU


async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    age = update.effective_message.text
    # написать здесь проверку на дурака
    age = int(age)
    user = await update_age(update.effective_user.id, age)
    return await start(update, context)
