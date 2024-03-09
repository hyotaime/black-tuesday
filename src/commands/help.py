from telegram import Update
from telegram.ext import ContextTypes
from src.log import logger


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - help")
    await context.bot.send_message(
        chat_id=chat_id,
        text="Command List\n"
             "/help - Show command list\n"
             "/alarm - Set an alarm\n"
             "/search - Search anything you want at google.com\n"
             "/weather - Show weather information\n"
             "/setloc - Set location for weather command\n"
             "/pl - Show Premier League table\n"
             "/plnow - Show today's Premier League schedule\n"
             "/plnext - Show tomorrow's Premier League schedule\n"
             "/cl - Show this week's UEFA Champions League schedule\n"
             "/kbo - Show KBO league table\n"
             "/kbonow - Show today's KBO game schedule\n"
             "/npb - Show NPB league table\n"
             "/npbnow - Show today's NPB game schedule\n"
             "/gpt - Ask anything to chatGPT\n"
             "/gptkeyset - Set your chatGPT API key\n"
             "/find - Search stock ticker with company name\n"
             "/now - Show real time price of the stock\n"
             "/boj - BOJ(Solved.ac) streak reminder\n"
    )
