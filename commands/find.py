from telegram import Update
from telegram.ext import ContextTypes

from log import logger
import crawling


async def find(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"UserID: {chat_id} - find")
    # 입력 메시지에서 '/find'를 제외한 텍스트 추출
    search_value = update.message.text.replace('/find', '').replace('@black_tuesday_bot', '').strip()
    if search_value == "":
        await context.bot.send_message(
            chat_id=chat_id,
            text="Please enter your search value.\n"
                 "e.g.)\t/find Apple"
        )
    else:
        await process_find_value(chat_id, context, search_value)


async def f(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"UserID: {chat_id} - f")
    # 입력 메시지에서 '/f'를 제외한 텍스트 추출
    search_value = update.message.text.replace('/f', '').replace('@black_tuesday_bot', '').strip()
    if search_value == "":
        await context.bot.send_message(
            chat_id=chat_id,
            text="Please enter your search value.\n"
                 "e.g.)\t/f Apple"
        )
    else:
        await process_find_value(chat_id, context, search_value)


async def process_find_value(chat_id: int, context: ContextTypes.DEFAULT_TYPE, find_value: str):
    code, name, type_market = crawling.find_crawling(find_value)
    type = ""
    market = ""

    if type_market:
        # type_market의 첫 번째 값에서 " - "를 기준으로 type과 market 구분
        split_values = type_market[0].split(" - ")
        if len(split_values) == 2:
            type = split_values[0].strip()
            market = split_values[1].strip()

    if not code:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Can't find any result."
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"{name[0]} ({code[0]})\n{market} - {type}"
        )
