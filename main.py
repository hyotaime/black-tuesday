import telegram as tel
from telegram.ext import CommandHandler, ApplicationBuilder

import database
from commands import start, help, find, now, gpt, alarm, search, kbo

# 토큰 읽기
with open("./hiddenValues/token_test.txt") as f:
    lines = f.readlines()
    token = lines[0].strip()

bot = tel.Bot(token=token)

# 메인 함수
if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    database.db_connection_test()

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

    application.run_polling()
