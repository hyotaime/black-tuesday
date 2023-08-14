import datetime

from telegram import Update
from telegram.ext import ContextTypes

from log import logger
import crawling


async def kbo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"UserID: {chat_id} - kbo")
    await process_kbo(chat_id, context)


async def kbonow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"UserID: {chat_id} - kbonow")
    await process_kbo_now(chat_id, context)


async def process_kbo_now(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    games = crawling.kbo_now_crawling()
    # today = datetime.datetime.now().strftime("%-m.%d")
    today = "8.02"
    message = ""
    for game in games:
        if game['date'].startswith(today):
            if game['time'] == "-":
                message = "프로야구 경기가 없습니다."
            else:
                message += f"{game['time']} {game['home']} {game['home_score']} : {game['away_score']} {game['away']}\n{game['stadium']} {game['broadcast']}\n\n"

    await context.bot.send_message(
        chat_id=chat_id,
        text=message
    )


async def process_kbo(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    team_data_list = crawling.kbo_crawling()

    message = "순위 팀명 경기 승  패  무  게임차 연속\n"
    for team_data in team_data_list:
        rank = "%-5s" % (team_data['Rank'] + "위")
        name = "%-5s" % team_data['Team Name']
        games_played = "%-5s" % team_data['Games Played']
        wins = "%-3s" % team_data['Wins']
        losses = "%-3s" % team_data['Losses']
        draws = "%-3s" % team_data['Draws']
        win_streak = "%-7s" % team_data['Win Streak']
        recent_wins = "%-3s" % team_data['Recent Wins']
        message += f"{rank} {name} {games_played} {wins} {losses} {draws} {win_streak} {recent_wins}\n"

    await context.bot.send_message(
        chat_id=chat_id,
        text=message
    )
