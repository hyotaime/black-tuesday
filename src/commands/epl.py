from telegram import Update
from telegram.ext import ContextTypes
from src.log import logger
from src import crawling


async def epl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - epl")
    await process_epl(chat_id, context)


async def eplnow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - eplnow")
    await process_epl_now(chat_id, context)


async def eplnext(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - eplnext")
    await process_epl_next(chat_id, context)


async def process_epl(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    data = crawling.epl_crawling()
    message = ""
    for pl_team_info in data:
        message += (f"{pl_team_info['position']} {pl_team_info['team']['tla']} {pl_team_info['playedGames']}G "
                    f"{pl_team_info['points']}p {pl_team_info['won']}W {pl_team_info['draw']}D {pl_team_info['lost']}L "
                    f"{pl_team_info['goalsFor']}:{pl_team_info['goalsAgainst']} {pl_team_info['goalDifference']}GD\n")

    await context.bot.send_message(
        chat_id=chat_id,
        text=message
    )


async def process_epl_now(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    data1, data2, today = crawling.epl_now_crawling()
    message = ""
    for match in data1:
        if match['gameDateTime'].split('T')[0].split('-')[2] != today and int(
                match['gameDateTime'].split('T')[1].split(':')[0]) >= 12:
            status = match['statusInfo']
            if status == '경기전':
                home_team = match['homeTeamName']
                away_team = match['awayTeamName']
                kick_off_time = match['gameDateTime'].split('T')[1].split(':')[:-1]
                stadium = match['stadium']

                message += (f"{':'.join(kick_off_time)} {status}\n"
                            f"{home_team} vs {away_team}\n"
                            f"{stadium}\n\n")
            else:
                home_team = match['homeTeamName']
                away_team = match['awayTeamName']
                home_score = match['homeTeamScore']
                away_score = match['awayTeamScore']
                kick_off_time = match['gameDateTime'].split('T')[1].split(':')[:-1]
                stadium = match['stadium']

                message += (f"{':'.join(kick_off_time)} {status}\n"
                            f"{home_team} {home_score}:{away_score} {away_team}\n"
                            f"{stadium}\n\n")

    for match in data2:
        if match['gameDateTime'].split('T')[0].split('-')[2] != today and int(
                match['gameDateTime'].split('T')[1].split(':')[0]) < 12:
            status = match['statusInfo']
            if status == '경기전':
                home_team = match['homeTeamName']
                away_team = match['awayTeamName']
                kick_off_time = match['gameDateTime'].split('T')[1].split(':')[:-1]
                stadium = match['stadium']

                message += (f"{':'.join(kick_off_time)} {status}\n"
                            f"{home_team} vs {away_team}\n"
                            f"{stadium}\n\n")
            else:
                home_team = match['homeTeamName']
                away_team = match['awayTeamName']
                home_score = match['homeTeamScore']
                away_score = match['awayTeamScore']
                kick_off_time = match['gameDateTime'].split('T')[1].split(':')[:-1]
                stadium = match['stadium']

                message += (f"{':'.join(kick_off_time)} {status}\n"
                            f"{home_team} {home_score}:{away_score} {away_team}\n"
                            f"{stadium}\n\n")
    if message == "":
        await context.bot.send_message(
            chat_id=chat_id,
            text="오늘 밤 예정된 프리미어리그 경기가 없습니다."
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=message
        )


async def process_epl_next(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    data1, data2, tomorrow = crawling.epl_now_crawling()
    message = ""
    for match in data1:
        if match['gameDateTime'].split('T')[0].split('-')[2] != tomorrow and int(
                match['gameDateTime'].split('T')[1].split(':')[0]) >= 12:
            home_team = match['homeTeamName']
            away_team = match['awayTeamName']
            kick_off_date = match['gameDateTime'].split('T')[0].split('-')[1:]
            kick_off_time = match['gameDateTime'].split('T')[1].split(':')[:-1]
            stadium = match['stadium']

            message += (f"{'-'.join(kick_off_date)} {':'.join(kick_off_time)}\n"
                        f"{home_team} vs {away_team}\n"
                        f"{stadium}\n\n")

    for match in data2:
        if match['gameDateTime'].split('T')[0].split('-')[2] != tomorrow and int(
                match['gameDateTime'].split('T')[1].split(':')[0]) < 12:
            home_team = match['homeTeamName']
            away_team = match['awayTeamName']
            kick_off_date = match['gameDateTime'].split('T')[0].split('-')[1:]
            kick_off_time = match['gameDateTime'].split('T')[1].split(':')[:-1]
            stadium = match['stadium']

            message += (f"{'-'.join(kick_off_date)} {':'.join(kick_off_time)}\n"
                        f"{home_team} vs {away_team}\n"
                        f"{stadium}\n\n")

    if message == "":
        await context.bot.send_message(
            chat_id=chat_id,
            text="내일 밤 예정된 프리미어리그 경기가 없습니다."
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=message
        )
