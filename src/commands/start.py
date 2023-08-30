from telegram import Update
from telegram.ext import ContextTypes
from log import logger


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - start")
    await context.bot.send_message(
        chat_id=chat_id,
        text="I'm black-T.U.E.S.D.A.Y\n"
             "Telegram-bot Ultimately Essential Service Definitively Assist You.\n"
             "Use /help to check commands."
    )
