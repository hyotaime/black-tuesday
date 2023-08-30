from telegram import Update
from telegram.ext import ContextTypes
from log import logger
import database, scheduler
import re


async def alarm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    weather_alarm_job = database.get_weather_job_id(chat_id)
    logger.info(f"ChatID: {chat_id} - alarm")

    # 입력 메시지에서 '/alarm'를 제외한 텍스트 추출
    alarm_time = update.message.text.replace('/alarm', '').replace('@black_tuesday_bot', '').strip()
    # 정규식을 사용하여 알람 시간 형식이 "9:30"과 같은지 확인
    time_pattern = r"\b\d{1,2}:\d{2}\b"

    if alarm_time == "":
        jobs = scheduler.scheduler.get_jobs()
        matching_jobs = [job for job in jobs if job.args and len(job.args) > 0 \
                         and job.args[0] == chat_id and job.id != weather_alarm_job]
        if matching_jobs:
            alarm_list = "\n".join([f"{i + 1}. {job.next_run_time.time()}\n"
                                    f"ID: {job.id}\n"
                                    f""
                                    for i, job in enumerate(matching_jobs)])
            await context.bot.send_message(
                chat_id=chat_id,
                text="Alarm List:\n" + alarm_list
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text="There are no scheduled alarms.\n"
                     "Please enter your alarm time(00:00~23:59).\n"
                     "e.g.)\t/alarm 9:30"
            )
    elif alarm_time == "all":
        await remove_all_alarms(chat_id, context, weather_alarm_job)
    elif re.match(time_pattern, alarm_time):
        try:
            process_alarm(chat_id, context, alarm_time)
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
                 "Correct Form: 9:30, 22:10\n"
        )
    else:
        alarm_identifier = alarm_time
        await remove_alarm(chat_id, context, alarm_identifier, weather_alarm_job)


async def print_notification(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=chat_id,
        text="Alarm: The specified time!"
    )


def process_alarm(chat_id, context: ContextTypes.DEFAULT_TYPE, alarm_time: str):
    target_hour, target_minute = map(int, alarm_time.split(':'))

    scheduler.scheduler.add_job(print_notification, 'cron', hour=target_hour, minute=target_minute,
                                args=(chat_id, context))


async def remove_alarm(chat_id: int, context: ContextTypes.DEFAULT_TYPE, alarm_identifier: str, weather_alarm_job: str):
    jobs = scheduler.scheduler.get_jobs()
    matching_jobs = [job for job in jobs if job.args and len(job.args) > 0 \
                     and job.args[0] == chat_id and job.id != weather_alarm_job]
    if alarm_identifier.isdigit():  # 입력 값이 숫자일 경우 index로 처리
        logger.info(f"ChatID: {chat_id} - remove_alarm_by_index")
        try:
            if matching_jobs:
                try:
                    index = int(alarm_identifier) - 1
                    selected_alarm = matching_jobs[index]
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=f"Alarm No.{alarm_identifier} has been removed.\n"
                             f"{selected_alarm.next_run_time.time()}\n"
                             f"(ID: {selected_alarm.id})"
                    )
                    selected_alarm.remove()
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


async def remove_alarm_by_id(chat_id: int, context: ContextTypes.DEFAULT_TYPE, alarm_id: str, weather_alarm_job: str):
    logger.info(f"ChatID: {chat_id} - remove_alarm_by_id")
    try:
        job_id = alarm_id
        job = scheduler.scheduler.get_job(job_id)
        if job.args[0] == chat_id and job.id != weather_alarm_job:
            alarm_time = job.next_run_time.time()
            job.remove()
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"{alarm_time} Alarm has been cleared.\n"
                     f"(ID: {job_id})"
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"Alarm(ID: {job_id}) not found."
            )
    except ValueError:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Please enter a valid number or ID."
        )


async def remove_all_alarms(chat_id: int, context: ContextTypes.DEFAULT_TYPE, weather_alarm_job: str):
    logger.info(f"ChatID: {chat_id} - remove_all_alarms")
    jobs = scheduler.scheduler.get_jobs()
    for job in jobs:
        if chat_id == job.args[0] and job.id != weather_alarm_job:
            job.remove()

    await context.bot.send_message(
        chat_id=chat_id,
        text="All alarms have been cleared."
    )
