from telegram import Update
from telegram.ext import ContextTypes
from log import logger
import crawling
import json
from pandas import json_normalize


async def npb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - npb")
    await process_npb(chat_id, context)


async def npbnow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    logger.info(f"ChatID: {chat_id} - npbnow")
    await process_npb_now(chat_id, context)


async def process_npb(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    table_central, table_pacific = crawling.npb_crawling()
    team_data_json_central = json.dumps(table_central, ensure_ascii=False)
    team_data_json_central = json.loads(team_data_json_central)
    df_central = json_normalize(team_data_json_central)
    message = "セ・リーグ\n"
    message += "順位  チーム名   試合   勝利   敗戦   引分  勝率  勝差\n"
    message += df_central.to_string(index=False, header=False, justify='center', col_space=5)
    message += "\n\n"
    team_data_json_pacific = json.dumps(table_pacific, ensure_ascii=False)
    team_data_json_pacific = json.loads(team_data_json_pacific)
    df_pacific = json_normalize(team_data_json_pacific)
    message += "パ・リーグ\n"
    message += "順位  チーム名   試合   勝利   敗戦   引分  勝率  勝差\n"
    message += df_pacific.to_string(index=False, header=False, justify='center', col_space=5)
    message += "\n"

    await context.bot.send_message(
        chat_id=chat_id,
        text=message
    )


async def process_npb_now(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    games = crawling.npb_now_crawling()
    message = ""
    for game in games:
        if games is None:
            message = "プロ野球の試合がありません。"
        elif game['status_info'] == '試合前':
            message += (f"{game['time']} {game['status_info']} {game['stadium']}\n"
                        f"{game['away']}({game['away_starter']}) vs {game['home']}({game['home_starter']})\n\n")
        elif game['status_info'] == '試合終了':
            if game['away_score'] > game['home_score']:
                message += (f"{game['status_info']} {game['stadium']}\n"
                            f"{game['away']} {game['away_score']} : {game['home_score']} {game['home']}\n"
                            f"(勝){game['winning_pitcher']}  (敗){game['losing_pitcher']}\n")
                if game['save_pitcher'] != '-':
                    message += (f"(S){game['save_pitcher']}\n\n")
                else:
                    message += "\n"
            elif game['away_score'] < game['home_score']:
                message += (f"{game['status_info']} {game['stadium']}\n"
                            f"{game['away']} {game['away_score']} : {game['home_score']} {game['home']}\n"
                            f"(敗){game['losing_pitcher']}\t\t(勝){game['winning_pitcher']}\n")
                if game['save_pitcher'] != '-':
                    message += (f"               (S){game['save_pitcher']}\n\n")
                else:
                    message += "\n"
            else:
                message += (f"{game['status_info']} {game['stadium']}\n"
                            f"{game['away']} {game['away_score']} : {game['home_score']} {game['home']}\n")
        else:
            message += (f"{game['away']} {game['away_score']} {game['status_info']} {game['home_score']} {game['home']}\n"
                        f"{game['stadium']}\n\n")

    await context.bot.send_message(
        chat_id=chat_id,
        text=message
    )
