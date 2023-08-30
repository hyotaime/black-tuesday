from telegram import Update
from telegram.ext import ContextTypes

from log import logger

import crawling
import re
import random
import string
import scheduler
import database


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    weather_alarm_time = update.message.text.replace('/weather', '').replace('@black_tuesday_bot', '').strip()

    if weather_alarm_time == "":
        logger.info(f"ChatID: {chat_id} - weather")
        await process_weather(chat_id, context)
    else:
        logger.info(f"ChatID: {chat_id} - weather {weather_alarm_time}")
        time_pattern = r"\b\d{1,2}:\d{2}\b"
        if re.match(time_pattern, weather_alarm_time):
            try:
                await process_weather_notification(chat_id, context, weather_alarm_time)
            except ValueError:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="Please enter a valid time.\n"
                         "00:00 ~ 23:59"
                )
        elif ":" in weather_alarm_time:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Check the time format.\n"
                     "Correct Form: 9:30, 22:10\n"
            )


async def weather_set_loc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    weather_location = update.message.text.replace('/setloc', '').replace('@black_tuesday_bot', '').strip()
    if weather_location == "":
        nx, ny = database.get_weather_location(chat_id)
        await context.bot.send_message(
            chat_id=chat_id,
            text="Set or Change your location.\n"
                 "e.g.) /setloc 12 345\n"
                 f"Your current key is ({nx, ny})"
        )
    else:
        nx = weather_location.split(' ')[0]
        ny = weather_location.split(' ')[1]
        database.set_weather_location(chat_id, nx, ny)
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Your location is set to {nx, ny}."
        )


async def process_weather(chat_id, context: ContextTypes.DEFAULT_TYPE):
    nx, ny = database.get_weather_location(chat_id)
    if nx is None or ny is None:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Please set your location.\n"
                 "e.g.) /setloc 12 345"
        )
        return
    today, weather_datas = crawling.weather_crawling(nx, ny)
    message = ""
    now_weather = weather_datas[0]
    if now_weather[3] != '0':
        message += (f"{today.month}월 {today.day}일 {today.hour}시 {today.minute}분 날씨입니다.\n"
                    f"{now_weather[3]}\n"
                    f"🌧강수량: {now_weather[4]}\n"
                    f"🌡기온: {now_weather[0]}°C\n"
                    f"💧습도: {now_weather[5]}%\n"
                    f"💨바람: {now_weather[7]}({now_weather[6]}°)방향으로 {now_weather[8]}m/s\n"
                    f"날씨예보\n")
    else:
        message += (f"{today.month}월 {today.day}일 {today.hour}시 {today.minute}분 날씨입니다.\n"
                    f"{now_weather[1]}{now_weather[2]}\n"
                    f"🌡기온: {now_weather[0]}°C\n"
                    f"💧습도: {now_weather[5]}%\n"
                    f"💨바람: {now_weather[7]}({now_weather[6]}°)방향으로 {now_weather[8]}m/s\n"
                    f"날씨예보\n")
    for weather_data in weather_datas[1:]:
        if weather_data[3] != '0':
            message += f"{weather_data[9]}시: ☔{weather_data[0]}°C, 💧{weather_data[5]}%\n"
        else:
            message += f"{weather_data[9]}시: {weather_data[1]}{weather_data[0]}°C, 💧{weather_data[5]}%\n"
    message += "기상청 초단기예보 조회 서비스 오픈 API를 이용한 것으로, 실제 기상상황과 차이가 있을 수 있습니다."

    await context.bot.send_message(
        chat_id=chat_id,
        text=message
    )


async def process_weather_notification(chat_id, context: ContextTypes.DEFAULT_TYPE, alarm_time: str):
    weather_noti_time = database.get_weather_noti_time(chat_id)
    if weather_noti_time != alarm_time or weather_noti_time is None:
        database.set_weather_noti_time(chat_id, alarm_time)

    target_hour, target_minute = map(int, alarm_time.split(':'))
    weather_job_id = database.get_weather_job_id(chat_id)

    if weather_job_id is None:
        rand_str = ""
        for i in range(34):
            rand_str += str(random.choice(string.ascii_uppercase + string.digits))
        weather_job_id = "W" + rand_str
    job = scheduler.scheduler.get_job(weather_job_id)
    if job is not None:
        job.remove()
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Weather Notification Time is changed to {alarm_time}."
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Weather Notification is set to " + alarm_time + ".\n"
        )
    scheduler.scheduler.add_job(process_weather, 'cron', hour=target_hour, minute=target_minute, args=(chat_id, context), id=weather_job_id)
    database.set_weather_job_id(chat_id, weather_job_id)


def process_set_weather_location(chat_id, nx, ny):
    database.set_weather_location(chat_id, nx, ny)
