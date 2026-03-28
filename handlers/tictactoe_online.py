from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config.states import TICTACTOE_ONLINE
from utils.make_keyboard_ttt import make_keyboard_ttt
from db.user_crud import get_user


async def tictactoe_online_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("tictactoe_online_start")
    query = update.callback_query
    board = ["⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️", "⬜️"]
    await query.answer()
    print(context.bot_data)
    queue = context.bot_data.setdefault("queue", [])
    last_game_id = context.bot_data.setdefault("last_game_id", 0)
    if len(queue) == 0:
        queue.append(update.effective_user.id)
        game_id = last_game_id + 1
        context.user_data["game_id"] = game_id
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text="Ты добавлен в очередь. Жди пока кто-то зайдет в игру.",
        )
    elif len(queue) >= 1:
        first_user = queue.pop()
        second_user = update.effective_user.id
        game_id = last_game_id + 1
        context.user_data["game_id"] = game_id
        context.bot_data.setdefault("games", {})

        markup = make_keyboard_ttt(board)

        message_krestik = await context.bot.send_message(
            chat_id=first_user,
            text=f"Йоу мы нашли тебе бедолагу! Это {update.effective_user.first_name}",
            reply_markup=markup,
        )
        # получаем имя соперника
        user = await get_user(first_user)
        
        message_nolik = await context.bot.send_message(
            chat_id=second_user,
            text=f"Ты оказался бедолагой! Твой соперник — {user['name']}",
            reply_markup=markup,
        )
        context.bot_data["games"][game_id] = {
            "krestik": first_user,
            "message_krestik": message_krestik.id,
            "nolik": second_user,
            "message_nolik": message_nolik.id,
            "board": board,
            "hod": 1,
        }
    return TICTACTOE_ONLINE


async def tictactoe_online(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    game_id = context.user_data["game_id"]
    game = context.bot_data["games"][game_id]
    print("Информация о вашей игре", game)

    if game["hod"] % 2 != 0:
        if game["krestik"] != update.effective_user.id:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Сейчас не твой ход!",
            )
            return TICTACTOE_ONLINE
        else:
            n_kletki = int(query.data)
            game["board"][n_kletki] = "❌"
            markup = make_keyboard_ttt(game["board"])
            await query.edit_message_text(
                text="Ход ноликов.",
                reply_markup=markup,
            )
            print(context.bot_data["games"])
            await context.bot.edit_message_text(
                text="Твой напарник походил. Делай ход!",
                chat_id=game["nolik"],
                message_id=game["message_nolik"],
                reply_markup=markup,
            )
            context.bot_data["games"][game_id]['hod'] += 1
            return TICTACTOE_ONLINE
    if game["hod"] % 2 == 0:
        if game["nolik"] != update.effective_user.id:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Сейчас не твой ход!",
            )
            return TICTACTOE_ONLINE
        else:
            n_kletki = int(query.data)
            game["board"][n_kletki] = "⭕️"
            markup = make_keyboard_ttt(game["board"])
            await query.edit_message_text(
                text="Ход крестиков.",
                reply_markup=markup,
            )
            print(context.bot_data["games"])
            await context.bot.edit_message_text(
                text="Твой напарник походил. Делай ход!",
                chat_id=game["krestik"],
                message_id=game["message_krestik"],
                reply_markup=markup,
            )
            context.bot_data["games"][game_id]['hod'] += 1
            return TICTACTOE_ONLINE
