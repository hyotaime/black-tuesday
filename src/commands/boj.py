from telegram import Update
from telegram.ext import ContextTypes
from src.log import logger
from src import crawling, database
import re
import datetime


async def boj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - boj")
    handle_or_alert_time = update.message.text.replace('/boj', '').replace('@black_tuesday_bot', '').strip()
    if handle_or_alert_time == "":
        handle = database.get_boj_handle(chat_id)
        noti_time = database.get_boj_noti_time(chat_id)
        if handle is None:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Please enter your BOJ handle.\n"
                     "e.g.) /boj handle"
            )
        elif noti_time is None:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"Your BOJ handle is \"{handle}\" and alarm time is \"{noti_time}\"\n"
                     f"e.g.) /boj handle\n"
                     f"e.g.) /boj 09:30\n"
            )
        else:
            await process_boj(chat_id, context)
    elif handle_or_alert_time == "off":
        logger.info(f"ChatID: {chat_id} - boj notification off")
        database.set_boj_noti_time(chat_id, None)
        await context.bot.send_message(
            chat_id=chat_id,
            text="BOJ Streak Reminder is turned off."
        )
    else:
        await process_boj_setting(chat_id, context, handle_or_alert_time)


async def process_boj(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    handle = database.get_boj_handle(chat_id)
    data = crawling.solved_crawling(handle)
    is_today_solved = False
    today_solved = 0
    for i in range(len(data)):
        if data[i]['date'] == datetime.datetime.now().strftime("%Y-%m-%d"):
            is_today_solved = True
            today_solved = data[i]['value']

    if is_today_solved:
        if today_solved == 1:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"You already solved {today_solved} problem today.\n"
                     f"https://solved.ac/profile/{handle}"
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"You already solved {today_solved} problems today.\n"
                     f"https://solved.ac/profile/{handle}"
            )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Not solved any problems today.\n"
                 f"https://solved.ac/"
        )


async def process_boj_setting(chat_id: int, context: ContextTypes.DEFAULT_TYPE, handle_or_alert_time: str):
    logger.info(f"ChatID: {chat_id} - boj {handle_or_alert_time}")
    time_pattern = r"\d{2}:\d{2}\b"
    if re.match(time_pattern, handle_or_alert_time):
        noti_time = handle_or_alert_time
        try:
            database.set_boj_noti_time(chat_id, noti_time)
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"BOJ Streak Reminder is set to \"{noti_time}\".\n"
            )
        except ValueError:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Please enter a valid time.\n"
                     "00:00 ~ 23:59"
            )
    elif ":" in handle_or_alert_time:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Check the time format.\n"
                 "Correct Form: 09:30, 22:10\n"
        )
    else:
        handle = handle_or_alert_time
        database.set_boj_handle(chat_id, handle)
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Your BOJ handle is set to \"{handle}\"."
        )


async def process_boj_notification(context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"BOJ Streak Reminder")
    current_time = datetime.datetime.now().strftime("%H:%M")
    chatids = database.get_boj_noti_id(current_time)
    if chatids is not None:
        for chatid in chatids:
            await process_boj(chatid['id'], context)
