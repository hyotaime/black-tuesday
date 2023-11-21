from telegram import Update
from telegram.ext import ContextTypes
from log import logger
import crawling


async def find(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - find")
    # 입력 메시지에서 '/find'를 제외한 텍스트 추출
    search_value = update.message.text.replace('/find', '').replace('@black_tuesday_bot', '').strip()
    if search_value == "":
        await context.bot.send_message(
            chat_id=chat_id,
            text="Please enter your search value.\n"
                 "e.g.) /find Apple"
        )
    else:
        await process_find_value(chat_id, context, search_value)


async def f(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - f")
    # 입력 메시지에서 '/f'를 제외한 텍스트 추출
    search_value = update.message.text.replace('/f', '').replace('@black_tuesday_bot', '').strip()
    if search_value == "":
        await context.bot.send_message(
            chat_id=chat_id,
            text="Please enter your search value.\n"
                 "e.g.) /f Apple"
        )
    else:
        await process_find_value(chat_id, context, search_value)


async def process_find_value(chat_id: int, context: ContextTypes.DEFAULT_TYPE, find_value: str):
    result = crawling.find_crawling(find_value)

    if not result:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Can't find any result."
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=result
        )
