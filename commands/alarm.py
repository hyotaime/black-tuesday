from telegram import Update
from telegram.ext import ContextTypes

from log import logger


async def alarm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("alarm")
    # 입력 메시지에서 '/alarm'를 제외한 텍스트 추출
    time = update.message.text.replace('/alarm', '').strip()
    if time == "":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please enter your alarm time.\n"
                 "e.g.)\t/alarm 9"
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=time + "\nalarm test"
        )
