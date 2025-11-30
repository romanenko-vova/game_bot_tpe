from telegram import (
    Update,
)
from telegram.ext import (
    ContextTypes
)
from config.states import TALK

async def talk_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Чтобы поговорить со мной, просто напиши любой текст.",
    )
    return TALK


async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    if "привет" in text.lower():
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Здарово, брат!",
        )
    # чтобы тут обрабатывались 5 рандомных фраз
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
        )

async def say_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_number = update.effective_message.contact.phone_number
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Ваш номер: {phone_number}"
    )