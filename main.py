import logging
import requests
from bs4 import BeautifulSoup
import telegram as tel
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, ApplicationBuilder

# 토큰 읽기
with open("./token.txt") as f:
    lines = f.readlines()
    token = lines[0].strip()

with open("./chat_id.txt") as f:
    lines = f.readlines()
    chat_id = lines[0].strip()

bot = tel.Bot(token=token)

# 로그 생성
logger = logging.getLogger()
# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)
# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
# 로그 끝

# 명령어
# start 명령어에 대한 응답
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("start")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="It's telegram bot.\nUse /help to check commands."
    )

# help 명령어에 대한 응답
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("help")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Command List\n/help - Show command list\n/find - Search stock information at investing.com\n/now - Show real time price of the stock\n"
    )

def searchCrawling(search_value):
    url = "https://investing.com/search/?q="
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    response = requests.get(url + search_value, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    second_elements = soup.select('.second')
    third_elements = soup.select('.third')
    fourth_elements = soup.select('.fourth')

    # 내부 값이 기호나 공백이 아닌 경우에만 추출하여 리스트에 저장
    second_values = [element.text.strip() for element in second_elements if element.text.strip() and not any(c in element.text for c in ('{', '}', '[', ']'))][:3]
    third_values = [element.text.strip() for element in third_elements if element.text.strip() and not any(c in element.text for c in ('{', '}', '[', ']'))][:3]
    fourth_values = [element.text.strip() for element in fourth_elements if element.text.strip() and not any(c in element.text for c in ('{', '}', '[', ']'))][:3]
    return second_values, third_values, fourth_values

def nowCrawling(code):
    url = "https://investing.com/search/?q="+code+"&tab=quotes"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    # 주어진 URL에 GET 요청 보내기
    response = requests.get(url, headers=headers)

    # 응답의 HTML 내용 추출
    html_content = response.content

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(html_content, 'html.parser')

    # 태그에서 필요한 값을 추출
    quote_row = soup.select('.js-inner-all-results-quote-item.row')
    new_url = "https://www.investing.com" + quote_row[0]['href'] if quote_row else None

    if not new_url:
        return None, None, None, None, None

    # 주어진 URL에 GET 요청 보내기
    response = requests.get(new_url, headers=headers)

    # 응답의 HTML 내용 추출
    html_content = response.content

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(html_content, 'html.parser')

    # 태그에서 필요한 값을 추출
    name = soup.find('h1', class_='text-xl text-left font-bold leading-7 md:text-3xl md:leading-8 mb-2.5 md:mb-2 text-[#232526] rtl:soft-ltr').text
    market = soup.find("span", class_ = "text-xs leading-4 font-normal overflow-hidden text-ellipsis flex-shrink").text
    price_now = soup.find('div', class_='text-5xl font-bold leading-9 md:text-[42px] md:leading-[60px] text-[#232526]').text
    div_tags = soup.find_all('div', class_='text-base font-bold leading-6 md:text-xl md:leading-7 rtl:force-ltr')

    values = []
    # 각 <div> 태그에서 값 추출
    for div_tag in div_tags:
        value = div_tag.text.strip('()')
        values.append(value)

    price_change = values[0]
    price_change_percent = values[1]
    return name, market, price_now, price_change, price_change_percent



async def process_search_value(update: Update, context: ContextTypes.DEFAULT_TYPE, search_value: str):
    code, name, type_market = searchCrawling(search_value)
    type = ""
    market = ""

    if type_market:
        # type_market의 첫 번째 값에서 " - "를 기준으로 type과 market 구분
        split_values = type_market[0].split(" - ")
        if len(split_values) == 2:
            type = split_values[0].strip()
            market = split_values[1].strip()

    if not code:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Can't find any result."
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{name[0]} ({code[0]})\n{market} - {type}"
        )

async def process_now_value(update: Update, context: ContextTypes.DEFAULT_TYPE, ticker: str):
    name, market, price_now, price_change, price_change_percent = nowCrawling(ticker)

    if not name:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Can't find any result."
        )
    else:
        if price_change[0] == "+":
            price_change = "⬆ " + price_change
        elif price_change[0] == "-":
            price_change = "⬇ " + price_change
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{name} - {market}\n{price_now} {price_change} ({price_change_percent})"
        )


async def find(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("find")
    # 입력 메시지에서 '/test'를 제외한 텍스트 추출
    search_value = update.message.text.replace('/find', '').strip()
    if search_value == "":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please enter your search value\ne.g.)\t/find Apple"
        )
    else:
        await process_search_value(update, context, search_value)


async def f(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("f")
    # 입력 메시지에서 '/test'를 제외한 텍스트 추출
    search_value = update.message.text.replace('/f', '').strip()
    if search_value == "":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please enter your search value\ne.g.)\t/f Apple"
        )
    else:
        await process_search_value(update, context, search_value)

async def now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("now")
    # 입력 메시지에서 '/test'를 제외한 텍스트 추출
    ticker = update.message.text.replace('/now', '').strip()
    if ticker == "":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please enter the ticker\ne.g.)\t/now AAPL"
        )
    else:
        await process_now_value(update, context, ticker)


async def n(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("n")
    # 입력 메시지에서 '/test'를 제외한 텍스트 추출
    ticker = update.message.text.replace('/n', '').strip()
    if ticker == "":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please enter the ticker\ne.g.)\t/n AAPL"
        )
    else:
        await process_now_value(update, context, ticker)
# 명령어 끝

# 메인 함수
if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    find_handler = CommandHandler('find', find)
    application.add_handler(find_handler)
    f_handler = CommandHandler('f', f)
    application.add_handler(f_handler)

    now_handler = CommandHandler('now', now)
    application.add_handler(now_handler)
    n_handler = CommandHandler('n', n)
    application.add_handler(n_handler)


    application.run_polling()
