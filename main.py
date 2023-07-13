import telegram as tel
from telegram.ext import CommandHandler, ApplicationBuilder

from commands import start, help, find, now, gpt, alarm, search

# 토큰 읽기
with open("./token.txt") as f:
    lines = f.readlines()
    token = lines[0].strip()

with open("./chat_id.txt") as f:
    lines = f.readlines()
    chat_id = lines[0].strip()

bot = tel.Bot(token=token)

# 메인 함수
if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler('start', start.start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help.help)
    application.add_handler(help_handler)

    find_handler = CommandHandler('find', find.find)
    application.add_handler(find_handler)
    f_handler = CommandHandler('f', find.f)
    application.add_handler(f_handler)

    now_handler = CommandHandler('now', now.now)
    application.add_handler(now_handler)
    n_handler = CommandHandler('n', now.n)
    application.add_handler(n_handler)

    alarm_handler = CommandHandler('alarm', alarm.alarm)
    application.add_handler(alarm_handler)

    search_handler = CommandHandler('search', search.search)
    application.add_handler(search_handler)

    gpt_handler = CommandHandler('gpt', gpt.gpt)
    application.add_handler(gpt_handler)

    application.run_polling()
