from telegram import Update
from telegram.ext import ContextTypes
from src.log import logger
from src import crawling
import json
from pandas import json_normalize


async def kbo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - kbo")
    await process_kbo(chat_id, context)


async def kbonow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - kbonow")
    await process_kbo_now(chat_id, context)


async def process_kbo(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    team_data_list = crawling.kbo_crawling()
    team_data_json = json.dumps(team_data_list, ensure_ascii=False)
    team_data_json = json.loads(team_data_json)
    df = json_normalize(team_data_json)
    message = "순위 팀명  경기   승   패   무  게임차 연속\n"
    message += df.to_string(index=False, header=False, justify='center', col_space=5)

    await context.bot.send_message(
        chat_id=chat_id,
        text=message
    )


async def process_kbo_now(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    games = crawling.kbo_now_crawling()
    message = ""
    if not games:
        message += "프로야구 경기가 없습니다."
    else:
        for game in games:
            if game['status_code'] == 'BEFORE':
                message += (f"{game['time']} {game['status_info']}\n"
                            f"{game['away']}({game['away_starter']}) vs {game['home']}({game['home_starter']})\n"
                            f"{game['stadium']} {game['broadcast']}\n\n")
            else:
                message += (f"{game['time']} {game['status_info']}\n"
                            f"{game['away']} {game['away_score']} : {game['home_score']} {game['home']}\n"
                            f"{game['stadium']} {game['broadcast']}\n\n")

    await context.bot.send_message(
        chat_id=chat_id,
        text=message
    )
