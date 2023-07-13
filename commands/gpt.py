from telegram import Update
from telegram.ext import ContextTypes

from log import logger


async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("gpt")
    # 입력 메시지에서 '/gpt'를 제외한 텍스트 추출
    ask_value = update.message.text.replace('/gpt', '').strip()
    if ask_value == "":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please enter your qusetion.\n"
                 "e.g.)\t/gpt Are you a human?"
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ask_value + "\ngpt test"
        )
