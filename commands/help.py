from telegram import Update
from telegram.ext import ContextTypes

from log import logger


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("help")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Command List\n"
             "/help - Show command list\n"
             "/find - Search stock information at investing.com\n"
             "/now - Show real time price of the stock\n"
             "/alarm - Set NASDAQ, KOSPI, NIKKEI price alarm\n"
             "/search - Search anything you want at google.com\n"
             "/gpt - Ask anything to chatGPT"
    )