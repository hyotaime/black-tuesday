from telegram import Update
from telegram.ext import ContextTypes

from log import logger

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import re

scheduler = AsyncIOScheduler()

# 이전에 스케줄러를 시작했는지 여부를 나타내는 변수
scheduler_started = False


async def alarm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global scheduler_started

    logger.info("alarm")
    # 입력 메시지에서 '/alarm'를 제외한 텍스트 추출
    alarm_time = update.message.text.replace('/alarm', '').strip()
    # 정규식을 사용하여 알람 시간 형식이 "9:30"과 같은지 확인
    time_pattern = r"\b\d{1,2}:\d{2}\b"

    if alarm_time == "":
        jobs = scheduler.get_jobs()
        if jobs:
            alarm_list = "\n".join([f"{i + 1}. {job.next_run_time.time()}\n"
                                    f"ID: {job.id}\n"
                                    for i, job in enumerate(jobs)])
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="예정된 알람 리스트:\n" + alarm_list
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="예정된 알람이 없습니다.\n"
                     "Please enter your alarm time.\n"
                     "e.g.)\t/alarm 9:30"
            )
    elif re.match(time_pattern, alarm_time):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"알림이 {alarm_time}에 설정되었습니다."
        )
        process_alarm(update, context, alarm_time)

        if not scheduler_started:
            scheduler.start()
            scheduler_started = True
    elif ":" in alarm_time:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="시간 형식을 확인하세요.\n"
                 "올바른 형식: 9:30, 22:10\n"
        )
    else:
        alarm_identifier = alarm_time
        await remove_alarm(update, context, alarm_identifier)


async def print_notification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="알림: 지정한 시간입니다!"
    )


def process_alarm(update: Update, context: ContextTypes.DEFAULT_TYPE, alarm_time: str):
    target_hour, target_minute = map(int, alarm_time.split(':'))

    scheduler.add_job(print_notification, 'cron', hour=target_hour, minute=target_minute, args=(update, context))


async def remove_alarm(update: Update, context: ContextTypes.DEFAULT_TYPE, alarm_identifier: str):
    jobs = scheduler.get_jobs()
    if alarm_identifier.isdigit():  # 입력 값이 숫자일 경우 index로 처리
        try:
            index = int(alarm_identifier) - 1
            if 0 <= index < len(jobs):
                job = jobs[index]
                job_id = job.id
                alarm_time = job.next_run_time.time()
                job.remove()
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"{alarm_identifier}번째 알람이 삭제되었습니다.\n"
                         f"{alarm_time}\n"
                         f"(ID: {job_id})"
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"{alarm_identifier}번째 알람이 존재하지 않습니다.\n"
                         f"예정된 알람 리스트를 다시 확인해주세요."
                )
        except ValueError:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="올바른 번호를 입력하세요. 예) /alarm remove 1"
            )
    else:  # 입력 값이 숫자가 아니면 ID로 처리
        try:
            job_id = alarm_identifier
            job = scheduler.get_job(job_id)
            if job:
                alarm_time = job.next_run_time.time()
                job.remove()
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"{alarm_time} 알람이 삭제되었습니다.\n"
                         f"(ID: {job_id})"
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"알람(ID: {job_id})을 찾을 수 없습니다."
                )
        except ValueError:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="올바른 번호 또는 ID를 입력하세요."
            )
