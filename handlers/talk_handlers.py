from telegram import (
    Update,
)
from telegram.ext import ContextTypes
from config.states import TALK
from openai import OpenAI


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
        if len(context.user_data["previous_messages"]) > 6:
            context.user_data["previous_messages"].pop(0)
            context.user_data["previous_messages"].pop(0)
        client = OpenAI()
        response = client.responses.create(
            model="gpt-5-mini",
            reasoning={"effort": "low"},
            input=[
                {
                    "role": "developer",
                    "content": 'Ты - бот, который общается с пользователем в Telegram. Человек тебе пишет сообщение, а ты поддерживай диалог. Пиши только на русском языке. Говори с человеком будто он на твоем уроке на экране рисовал письки"',
                },
            ]
            + context.user_data["previous_messages"]
            + [
                {
                    "role": "user",
                    "content": text,
                }
            ],
        )
        response_text = response.output_text
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response_text,
        )
        context.user_data["previous_messages"].append({"role": "user", "content": text})
        context.user_data["previous_messages"].append(
            {"role": "assistant", "content": response_text}
        )


async def say_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_number = update.effective_message.contact.phone_number
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Ваш номер: {phone_number}"
    )
