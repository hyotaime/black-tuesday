from telegram import Update
from telegram.ext import ContextTypes

import database
from log import logger
import openai


_gpt_chat = {}
openai.api_key = None


async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - gpt")
    openai.api_key = database.get_key(chat_id)
    # 입력 메시지에서 '/gpt'를 제외한 텍스트 추출
    ask_value = update.message.text.replace('/gpt', '').replace('@black_tuesday_bot', '').strip()
    try:
        if openai.api_key is None:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Please set your Openai API key.\n"
                     "e.g.) /gptkeyset 1q2w3e4r5t"
            )
        elif ask_value == "":
            await context.bot.send_message(
                chat_id=chat_id,
                text="Please enter your qusetion.\n"
                     "e.g.) \"/gpt Are you human?\"\n"
                     "Use \"/gpt clear\" to clear the chat history."
            )
        elif ask_value == "clear":
            logger.info(f"ChatID: {chat_id} - gpt clear")
            _gpt_chat[chat_id].clear()
            await context.bot.send_message(
                chat_id=chat_id,
                text="Chat history with ChatGPT is cleared."
            )
        else:
            await process_gpt(chat_id, context, ask_value)
    except openai.error.OpenAIError as e:
        await context.bot.send_message(
            chat_id=chat_id,
            text="An error occurred while using the OpenAI API: " + str(e)
        )


async def gpt_key_set(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - gptkeyset")
    # 입력 메시지에서 '/gpt'를 제외한 텍스트 추출
    key_value = update.message.text.replace('/gptkeyset', '').replace('@black_tuesday_bot', '').strip()
    if key_value == "":
        key_value = database.get_key(chat_id)
        await context.bot.send_message(
            chat_id=chat_id,
            text="Set or Change your Openai API key.\n"
                 "e.g.) /gptkeyset 1q2w3e4r5t\n"
                 f"Your current key is \"{key_value}\""
        )
    else:
        database.set_key(chat_id, key_value)
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Your ChatGPT API key is set to \"{key_value}\""
        )


async def process_gpt(chat_id: int, context: ContextTypes.DEFAULT_TYPE, ask_value: str):
    content = ask_value

    if chat_id not in _gpt_chat:
        _gpt_chat[chat_id] = []  # 새로운 chat_id에 해당하는 딕셔너리 생성

    _gpt_chat[chat_id].append({"role": "user", "content": content})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=_gpt_chat[chat_id]
    )

    chat_response = completion.choices[0].message.content.strip()
    await context.bot.send_message(
        chat_id=chat_id,
        text=f'ChatGPT: {chat_response}'
    )
    _gpt_chat[chat_id].append({"role": "assistant", "content": chat_response})
