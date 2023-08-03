from telegram import Update
from telegram.ext import ContextTypes

from log import logger
import openai

with open("./hiddenValues/gptapi_key.txt") as f:
    lines = f.readlines()
    openai.api_key = lines[0].strip()

messages = []


async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("gpt")
    # 입력 메시지에서 '/gpt'를 제외한 텍스트 추출
    ask_value = update.message.text.replace('/gpt', '').strip()
    if ask_value == "":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please enter your qusetion.\n"
                 "e.g.) \"/gpt Are you human?\"\n"
                 "Use \"/gpt clear\" to clear the chat history."
        )
    elif ask_value == "clear":
        logger.info("gpt clear")
        messages.clear()
        print(messages)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Chat history with ChatGPT is cleared."
        )
    else:
        await process_gpt(update, context, ask_value)


async def process_gpt(update: Update, context: ContextTypes.DEFAULT_TYPE, ask_value: str):
    content = ask_value

    messages.append({"role": "user", "content": content})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    chat_response = completion.choices[0].message.content.strip()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'ChatGPT: {chat_response}'
    )
    messages.append({"role": "assistant", "content": chat_response})
    print(messages)
