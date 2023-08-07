from telegram import Update
from telegram.ext import ContextTypes

from log import logger
import crawling


async def now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"UserID: {chat_id} - now")
    # 입력 메시지에서 '/now'를 제외한 텍스트 추출
    ticker = update.message.text.replace('/now', '').strip()
    if ticker == "":
        await context.bot.send_message(
            chat_id=chat_id,
            text="Please enter the ticker.\ne.g.)\t/now AAPL"
        )
    else:
        await process_now_value(chat_id, context, ticker)


async def n(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"UserID: {chat_id} - n")
    # 입력 메시지에서 '/n'를 제외한 텍스트 추출
    ticker = update.message.text.replace('/n', '').strip()
    if ticker == "":
        await context.bot.send_message(
            chat_id=chat_id,
            text="Please enter the ticker.\ne.g.)\t/n AAPL"
        )
    else:
        await process_now_value(chat_id, context, ticker)


async def process_now_value(chat_id: int, context: ContextTypes.DEFAULT_TYPE, ticker: str):
    name, market, price_now, price_change, price_change_percent = crawling.now_crawling(ticker)

    if not name:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Can't find any result."
        )
    else:
        if price_change[0] == "+":
            price_change = "⬆ " + price_change
        elif price_change[0] == "-":
            price_change = "⬇ " + price_change
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"{name} - {market}\n{price_now} {price_change} ({price_change_percent})"
        )
