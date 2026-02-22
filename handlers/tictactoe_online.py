from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config.states import TICTACTOE_ONLINE


async def tictactoe_online_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    print("tictactoe_online_start")
    query = update.callback_query
    await query.answer()

    queue = context.bot_data["queue"]
    if len(queue) == 0:
        queue.append(update.effective_user.id)
        game_id = context.bot_data["last_game_id"] + 1
        context.user_data["game_id"] = game_id
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text="Ты добавлен в очередь. Жди пока кто-то зайдет в игру.",
        )
    elif len(queue) >= 1:
        first_user = queue.pop()
        second_user = update.effective_user.id
        game_id = context.bot_data["last_game_id"] + 1
        context.user_data["game_id"] = game_id
        context.bot_data["games"][game_id] = {
            "krestik": first_user,
            "nolik": second_user,
            "board": [
                "⬜️",
                "⬜️",
                "⬜️",
                "⬜️",
                "⬜️",
                "⬜️",
                "⬜️",
                "⬜️",
                "⬜️",
            ],
            "hod": 1,
        }
        keyboard = [
            [
                InlineKeyboardButton("⬜️", callback_data="0"),
                InlineKeyboardButton("⬜️", callback_data="1"),
                InlineKeyboardButton("⬜️", callback_data="2"),
            ],
            [
                InlineKeyboardButton("⬜️", callback_data="3"),
                InlineKeyboardButton("⬜️", callback_data="4"),
                InlineKeyboardButton("⬜️", callback_data="5"),
            ],
            [
                InlineKeyboardButton("⬜️", callback_data="6"),
                InlineKeyboardButton("⬜️", callback_data="7"),
                InlineKeyboardButton("⬜️", callback_data="8"),
            ],
        ]
        markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(
            chat_id=first_user,
            text="Йоу мы нашли тебе бедолагу!",
            reply_markup=markup,
        )
        await context.bot.send_message(
            chat_id=second_user,
            text="Ты оказался бедолагой!",
            reply_markup=markup,
        )
    return TICTACTOE_ONLINE


async def tictactoe_online(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    game_id = context.user_data["game_id"]
    game = context.bot_data["games"][game_id]
    print("Информация о вашей игре", game)
    if game["hod"] % 2 != 0:
        if game['krestik'] != update.effective_user.id:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Сейчас не твой ход!",
            )
            return TICTACTOE_ONLINE
        # что произойдет, если ход крестика и вы сейчас в крестике
        
        