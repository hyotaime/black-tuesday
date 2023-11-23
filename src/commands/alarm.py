from telegram import Update
from telegram.ext import ContextTypes
from src.log import logger
from src import database
import datetime
import re


async def alarm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - alarm")

    # 입력 메시지에서 '/alarm'를 제외한 텍스트 추출
    alarm_time = update.message.text.replace('/alarm', '').replace('@black_tuesday_bot', '').strip()
    # 정규식을 사용하여 알람 시간 형식이 "09:30"과 같은지 확인
    time_pattern = r"\d{2}:\d{2}\b"

    if alarm_time == "":
        alarms = database.get_alarm(chat_id)
        if alarms:
            alarm_list = "\n".join([f"{i + 1}. {alarm['atime']}\n"
                                    f"ID: {alarm['id']}\n"
                                    f""
                                    for i, alarm in enumerate(alarms)])
            await context.bot.send_message(
                chat_id=chat_id,
                text="Alarm List:\n" + alarm_list
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text="There are no scheduled alarms.\n"
                     "Please enter your alarm time(00:00~23:59).\n"
                     "e.g.) /alarm 09:30"
            )
    elif alarm_time == "all":
        await remove_all_alarms(chat_id, context)
    elif re.match(time_pattern, alarm_time):
        try:
            database.set_alarm(chat_id, alarm_time)
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"Alarm set for {alarm_time}."
            )
        except ValueError:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Please enter a valid time.\n"
                     "00:00 ~ 23:59"
            )

    elif ":" in alarm_time:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Check the time format.\n"
                 "Correct Form: 09:30, 22:10\n"
        )
    else:
        alarm_identifier = alarm_time
        await remove_alarm(chat_id, context, alarm_identifier)


async def print_notification(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=chat_id,
        text="Alarm: The specified time!"
    )


async def remove_alarm(chat_id: int, context: ContextTypes.DEFAULT_TYPE, alarm_identifier: str):
    alarm_list = database.get_alarm(chat_id)
    if alarm_identifier.isdigit():  # 입력 값이 숫자일 경우 index로 처리
        logger.info(f"ChatID: {chat_id} - remove_alarm_by_index")
        try:
            if alarm_list:
                try:
                    index = int(alarm_identifier) - 1
                    selected_alarm = alarm_list[index]
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=f"Alarm No.{alarm_identifier} has been removed.\n"
                             f"{selected_alarm['atime']}\n"
                             f"(ID: {selected_alarm['id']})"
                    )
                    database.remove_alarm(selected_alarm['id'])
                except IndexError as e:
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text="An error occurred while removing alarm by index.\n" + str(e)
                    )
            else:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"Alarm No.{alarm_identifier} does not exist.\n"
                         f"Please check the scheduled alarm list again."
                )
        except ValueError:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Please enter a valid number. 예) /alarm remove 1"
            )
    else:  # 입력 값이 숫자가 아니면 ID로 처리
        await remove_alarm_by_id(chat_id, context, alarm_identifier)


async def remove_alarm_by_id(chat_id: int, context: ContextTypes.DEFAULT_TYPE, alarm_identifier: str):
    logger.info(f"ChatID: {chat_id} - remove_alarm_by_id")
    alarm_list = database.get_alarm(chat_id)
    try:
        alarm_id = alarm_identifier
        alarm_time = ""
        alarm_exists = False
        for alarm in alarm_list:
            if alarm['id'] == alarm_id:
                alarm_time += alarm['atime']
                database.remove_alarm(alarm_id)
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"{alarm_time} Alarm has been cleared.\n"
                         f"(ID: {alarm_id})"
                )
                alarm_exists = True
                break
        if not alarm_exists:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"Alarm(ID: {alarm_id}) not found."
            )
    except ValueError:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Please enter a valid or ID."
        )


async def remove_all_alarms(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"ChatID: {chat_id} - remove_all_alarms")
    database.remove_all_alarm(chat_id)
    await context.bot.send_message(
        chat_id=chat_id,
        text="All alarms have been cleared."
    )


async def process_alarm_notification(context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"alarm notification")
    current_time = datetime.datetime.now().strftime("%H:%M")
    chatids = database.get_alarm_by_time(current_time)
    for chatid in chatids:
        await print_notification(chatid['chatid'], context)
