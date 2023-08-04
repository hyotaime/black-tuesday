from telegram import Update
from telegram.ext import ContextTypes

from log import logger

from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()


async def alarm(update: Update, context: ContextTypes.DEFAULT_TYPE):
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


async def print_notification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="알림: 지정한 시간입니다!"
    )


def process_alarm(update: Update, context: ContextTypes.DEFAULT_TYPE, alarm_time: str):
    target_hour, target_minute = map(int, alarm_time.split(':'))

    scheduler.add_job(print_notification, 'cron', hour=target_hour, minute=target_minute, args=(update, context))
    scheduler.start()
