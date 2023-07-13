from telegram import Update
from telegram.ext import ContextTypes

from log import logger


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("search")
    # 입력 메시지에서 '/search'를 제외한 텍스트 추출
    search_value = update.message.text.replace('/search', '').strip()
    if search_value == "":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please enter your search value.\n"
                 "e.g.)\t/search banana"
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=search_value + "\nsearch test"
        )