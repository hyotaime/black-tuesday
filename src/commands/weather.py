from telegram import Update
from telegram.ext import ContextTypes
from src.log import logger
from src import crawling, database
import re
import datetime


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    weather_alarm_time = update.message.text.replace('/weather', '').replace('@black_tuesday_bot', '').strip()

    if weather_alarm_time == "":
        logger.info(f"ChatID: {chat_id} - weather")
        await process_weather(chat_id, context)
    elif weather_alarm_time == "off":
        logger.info(f"ChatID: {chat_id} - weather notification off")
        database.set_weather_noti_time(chat_id, None)
        await context.bot.send_message(
            chat_id=chat_id,
            text="Weather Notification is turned off."
        )
    else:
        logger.info(f"ChatID: {chat_id} - weather {weather_alarm_time}")
        time_pattern = r"\d{2}:\d{2}\b"
        if re.match(time_pattern, weather_alarm_time):
            try:
                await process_set_weather_notification(chat_id, context, weather_alarm_time)
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
                     "Correct Form: 09:30, 22:10\n"
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
        nx_str, ny_str = weather_location.split(' ')
        try:
            if len(nx_str) > 3 or len(ny_str) > 3:
                raise ValueError
            nx, ny = int(nx_str), int(ny_str)
            database.set_weather_location(chat_id, nx, ny)
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"Your location is set to {nx, ny}."
            )
        except ValueError:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Please enter a valid location.\n"
                     "e.g.) /setloc 12 345"
            )


async def process_weather(chat_id, context: ContextTypes.DEFAULT_TYPE):
    try:
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
    except Exception:
        await context.bot.send_message(
            chat_id=chat_id,
            text="날씨를 불러오는 중 문제가 발생했습니다."
        )


async def process_weather_notification(context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"weather notification")
    current_time = datetime.datetime.now().strftime("%H:%M")
    chatids = database.get_weather_noti_id(current_time)
    for chatid in chatids:
        await process_weather(chatid['id'], context)


async def process_set_weather_notification(chat_id, context: ContextTypes.DEFAULT_TYPE, alarm_time: str):
    database.set_weather_noti_time(chat_id, alarm_time)
    await context.bot.send_message(
        chat_id=chat_id,
        text="Weather Notification is set to " + alarm_time + ".\n"
    )
