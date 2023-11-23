import telegram as tel
from telegram.ext import CommandHandler, ApplicationBuilder
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from commands import start, help, find, now, gpt, alarm, search, kbo, weather, npb
from src import database, log

# 토큰 읽기
load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = tel.Bot(token=BOT_TOKEN)

# 메인 함수
if __name__ == '__main__':
    log.logger.addHandler(log.stream_handler)
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    database.db_connection_test()
    scheduler = AsyncIOScheduler()
    scheduler.start()
    scheduler.add_job(weather.process_weather_notification, 'cron', second=0, args=(application, ), id='wscheduler')
    scheduler.add_job(alarm.process_alarm_notification, 'cron', second=0, args=(application, ), id='ascheduler')

    start_handler = CommandHandler('start', start.start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help.help)
    application.add_handler(help_handler)

    alarm_handler = CommandHandler('alarm', alarm.alarm)
    application.add_handler(alarm_handler)

    search_handler = CommandHandler('search', search.search)
    application.add_handler(search_handler)

    gpt_handler = CommandHandler('gpt', gpt.gpt)
    application.add_handler(gpt_handler)
    gptkeyset_handler = CommandHandler('gptkeyset', gpt.gpt_key_set)
    application.add_handler(gptkeyset_handler)

    find_handler = CommandHandler('find', find.find)
    application.add_handler(find_handler)
    f_handler = CommandHandler('f', find.f)
    application.add_handler(f_handler)

    now_handler = CommandHandler('now', now.now)
    application.add_handler(now_handler)
    n_handler = CommandHandler('n', now.n)
    application.add_handler(n_handler)

    kbo_handler = CommandHandler('kbo', kbo.kbo)
    application.add_handler(kbo_handler)
    kbonow_handler = CommandHandler('kbonow', kbo.kbonow)
    application.add_handler(kbonow_handler)

    npb_handler = CommandHandler('npb', npb.npb)
    application.add_handler(npb_handler)
    npbnow_handler = CommandHandler('npbnow', npb.npbnow)
    application.add_handler(npbnow_handler)

    weather_handler = CommandHandler('weather', weather.weather)
    application.add_handler(weather_handler)
    setloc_handler = CommandHandler('setloc', weather.weather_set_loc)
    application.add_handler(setloc_handler)

    application.run_polling()
