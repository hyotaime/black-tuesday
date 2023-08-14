from telegram import Update
from telegram.ext import ContextTypes

from log import logger


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"UserID: {chat_id} - help")
    await context.bot.send_message(
        chat_id=chat_id,
        text="Command List\n"
             "/help - Show command list\n"
             "/alarm - Set an alarm\n"
             "/search - Search anything you want at google.com\n"
             "/gpt - Ask anything to chatGPT\n"
             "/gptkeyset - Set your chatGPT API key\n"
             "/find - Search stock information at investing.com\n"
             "/now - Show real time price of the stock\n"
             "/kbo - Show KBO league table\n"
             "/kbonow - Show today's game schedule\n"
    )
