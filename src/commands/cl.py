from telegram import Update
from telegram.ext import ContextTypes
from src.log import logger
from src import crawling


async def cl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - cl")
    data = crawling.cl_crawling()
    message = ""
    for match in data:
        status = match['statusInfo']
        if status == '경기전':
            home_team = match['homeTeamName']
            away_team = match['awayTeamName']
            kick_off_date = match['gameDateTime'].split('T')[0].split('-')[1:]
            kick_off_time = match['gameDateTime'].split('T')[1].split(':')[:-1]
            stadium = match['stadium']

            message += (f"{'-'.join(kick_off_date)} {':'.join(kick_off_time)} {status}\n"
                        f"{home_team} vs {away_team}\n"
                        f"{stadium}\n\n")
        else:
            home_team = match['homeTeamName']
            away_team = match['awayTeamName']
            home_score = match['homeTeamScore']
            away_score = match['awayTeamScore']
            kick_off_date = match['gameDateTime'].split('T')[0].split('-')[1:]
            kick_off_time = match['gameDateTime'].split('T')[1].split(':')[:-1]
            stadium = match['stadium']

            message += (f"{'-'.join(kick_off_date)} {':'.join(kick_off_time)} {status}\n"
                        f"{home_team} {home_score}:{away_score} {away_team}\n"
                        f"{stadium}\n\n")
    if message == "":
        await context.bot.send_message(
            chat_id=chat_id,
            text="이번 주 예정된 챔피언스리그 경기가 없습니다."
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=message
        )
