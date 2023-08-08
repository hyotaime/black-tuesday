from telegram import Update
from telegram.ext import ContextTypes

from log import logger
import database


async def gpt_key_set(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"UserID: {chat_id} - gptkeyset")
    # 입력 메시지에서 '/gpt'를 제외한 텍스트 추출
    key_value = update.message.text.replace('/gptkeyset', '').strip()
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
