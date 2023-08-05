from telegram import Update
from telegram.ext import ContextTypes

from log import logger

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

# 이전에 스케줄러를 시작했는지 여부를 나타내는 변수
scheduler_started = False


async def alarm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global scheduler_started

    logger.info("alarm")
    # 입력 메시지에서 '/alarm'를 제외한 텍스트 추출
    alarm_time = update.message.text.replace('/alarm', '').strip()
    if alarm_time == "":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please enter your alarm time.\n"
                 "e.g.)\t/alarm 9:30"
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"알림이 {alarm_time}에 설정되었습니다."
        )
        process_alarm(update, context, alarm_time)

        if not scheduler_started:
            scheduler.start()
            scheduler_started = True


async def print_notification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="알림: 지정한 시간입니다!"
    )


def process_alarm(update: Update, context: ContextTypes.DEFAULT_TYPE, alarm_time: str):
    target_hour, target_minute = map(int, alarm_time.split(':'))

    scheduler.add_job(print_notification, 'cron', hour=target_hour, minute=target_minute, args=(update, context))
