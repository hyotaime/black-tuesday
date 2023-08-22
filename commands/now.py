from telegram import Update
from telegram.ext import ContextTypes

from log import logger
import yfinance as yf
import time


async def now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"UserID: {chat_id} - now")
    # 입력 메시지에서 '/now'를 제외한 텍스트 추출
    ticker = update.message.text.replace('/now', '').replace('@black_tuesday_bot', '').strip()
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
    ticker = update.message.text.replace('/n', '').replace('@black_tuesday_bot', '').strip()
    if ticker == "":
        await context.bot.send_message(
            chat_id=chat_id,
            text="Please enter the ticker.\ne.g.)\t/n AAPL"
        )
    else:
        await process_now_value(chat_id, context, ticker)


async def process_now_value(chat_id: int, context: ContextTypes.DEFAULT_TYPE, ticker: str):
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    try:
        # Use yfinance
        info = yf.Ticker(ticker).info
        try:
            rst = yf.download(ticker, start=today, end=today)
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"{info['longName']}({info['symbol']})\n"
                     f"Current Price: {info['currency']}{info['currentPrice']}\n"
                     f"Open: {rst['Open'][0]:.2f}\n"
                     f"High: {rst['High'][0]:.2f}\n"
                     f"Low: {rst['Low'][0]:.2f}\n"
                     f"Close: {rst['Close'][0]:.2f}\n"
                     f"Adj CLose: {rst['Adj Close'][0]:.2f}\n"
                     f"Volume: {rst['Volume'][0]}\n"
            )
        except Exception:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"{info['longName']}({info['symbol']})\n"
                     f"Current Price: {info['currency']}{info['currentPrice']}\n"
            )
    except Exception:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Can't find any result."
        )
