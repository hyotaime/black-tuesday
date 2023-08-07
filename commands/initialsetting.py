from telegram import Update
from telegram.ext import ContextTypes

from log import logger

_api_key = {}


async def gpt_key_set(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"UserID: {chat_id} - gptkeyset")
    # 입력 메시지에서 '/gpt'를 제외한 텍스트 추출
    key_value = update.message.text.replace('/gptkeyset', '').strip()
    if key_value == "":
        await context.bot.send_message(
            chat_id=chat_id,
            text="Please set your Openai API key.\n"
                 "e.g.) /gptkeyset 1q2w3e4r5t"
        )
    else:
        logger.info(f"UserID: {chat_id} - gptkeyset")
        set_api_key(chat_id, key_value)
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Your ChatGPT API key is set to \"{key_value}\""
        )


def set_api_key(chat_id, key):
    _api_key[chat_id] = key


def get_api_key_all():
    return _api_key


def get_api_key(chat_id):
    return _api_key[chat_id]