from telegram import Update
from telegram.ext import ContextTypes

from log import logger
import crawling


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 입력 메시지에서 '/search'를 제외한 텍스트 추출
    search_value = update.message.text.replace('/search', '').strip()
    logger.info("search : " + "\"" + search_value + "\"")
    search_value = search_value.replace(' ', '+').strip()
    if search_value == "":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please enter your search value.\n"
                 "e.g.)\t/search banana"
        )
    else:
        await process_search_value(update, context, search_value)


async def process_search_value(update: Update, context: ContextTypes.DEFAULT_TYPE, search_value: str):
    message = crawling.search_crawling(search_value)

    if not message:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Can't find any result."
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message
        )
