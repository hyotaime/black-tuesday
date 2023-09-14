import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


def find_crawling(find_value):
    # https://github.com/yashwanth2804/TickerSymbol
    # Using tickersearch API By Yashwanth2804
    url = "https://ticker-2e1ica8b9.now.sh//keyword/" + find_value
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    result = ""
    for item in data:
        result += (f"{item['name']}\n"
                   f"Ticker: {item['symbol']}\n"
                   f"\n")

    return result


def search_crawling(search_value):
    # Set the headers to mimic a web browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    url = "https://www.google.com/search?q=" + search_value
    # Send a GET request to the Google search URL with the query parameter
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the HTML content from the response
        html_content = response.text

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Find all the search result elements
        search_results = soup.find_all("div", class_="yuRUbf")

        # Extract the search result titles and URLs
        message = ""
        for result in search_results:
            title = result.find("h3").text
            result_url = result.find("a")["href"]
            message += f"{title}\n{result_url}\n\n"

        return message
    else:
        return None


def kbo_crawling():
    url = "https://www.koreabaseball.com/Record/TeamRank/TeamRank.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }

    # 주어진 URL에 GET 요청 보내기
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table")
    table_rows = table.find_all("tr")[1:]  # Skip the header row

    team_data_list = []

    for row in table_rows:
        columns = row.find_all("td")
        rank = columns[0].get_text()
        team_name = columns[1].get_text()
        games_played = columns[2].get_text()
        wins = columns[3].get_text()
        losses = columns[4].get_text()
        draws = columns[5].get_text()
        win_streak = columns[7].get_text()
        recent_wins = columns[9].get_text()

        team_data = {
            "순위": rank,
            "팀명": team_name,
            "게임": games_played,
            "승": wins,
            "패": losses,
            "무": draws,
            "게임차": win_streak,
            "연속": recent_wins
        }

        team_data_list.append(team_data)

    return team_data_list


def kbo_now_crawling():
    # 국내 야구
    url = "https://api-gw.sports.naver.com/schedule/games?fields=basic%2CsuperCategoryId%2CcategoryName%2Cstadium%2CstatusNum%2CgameOnAir%2Ctitle%2CspecialMatchInfo%2CroundCode%2CseriesOutcome%2CseriesGameNo%2ChomeStarterName%2CawayStarterName%2CwinPitcherName%2ClosePitcherName%2ChomeCurrentPitcherName%2CawayCurrentPitcherName%2CbroadChannel&upperCategoryId=kbaseball&categoryId=kbo&roundCodes=&size=500"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers).json()

    results = []
    for game in response['result']['games']:
        result = {'time': '-', 'away': '-', 'away_score': '-', 'home': '-', 'home_score': '-', 'broadcast': '-',
                  'stadium': '-', 'status_code': '-', 'status_info': '-', 'home_pitcher': '-', 'away_pitcher': '-',
                  'home_starter': '-', 'away_starter': '-'}
        result.update({
            'time': game['gameDateTime'][-8:-3],
            'away': game['awayTeamName'],
            'away_score': game['awayTeamScore'],
            'home': game['homeTeamName'],
            'home_score': game['homeTeamScore'],
            'broadcast': game['broadChannel'].replace('^', ', '),
            'stadium': game['stadium'],
            'status_code': game['statusCode'],
            'status_info': game['statusInfo'],
            'home_pitcher': game['homeCurrentPitcherName'],
            'away_pitcher': game['awayCurrentPitcherName'],
            'home_starter': game['homeStarterName'],
            'away_starter': game['awayStarterName']
        })
        if result['status_code'] == 'RESULT':
            result['status_info'] = '종료'
        results.append(result)
    return results


def weather_crawling(nx, ny):
    # https://github.com/az0t0/discord-seoultechbot/blob/main/src/weather.py
    # 위 repository 참고함
    load_dotenv()
    token = os.environ.get('WEATHER_API_TOKEN')

    today = datetime.now()
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
    direction = ['북', '북북동', '북동', '동북동', '동', '동남동', '남동', '남남동', '남',
                 '남남서', '남서', '서남서', '서', '서북서', '북서', '북북서', '북']

    basetime = today
    if int(basetime.strftime('%H%M')[2:4]) < 45:
        basetime = today - timedelta(hours=1)

    params = {'serviceKey': token, 'dataType': 'JSON', 'numOfRows': '1000', 'base_date': basetime.strftime('%Y%m%d'),
              'base_time': basetime.strftime('%H') + '30', 'nx': nx, 'ny': ny}

    response = requests.get(url, params=params, timeout=20)
    items = response.json().get('response').get('body').get('items')

    data = [[], [], [], [], [], []]

    for i, item in enumerate(items['item']):
        if i < 6:
            # Kor. to Eng.
            data[i] = ['temperature', 'status_num', 'status', 'rain_type', 'precipitation', 'humidity', 'wind_vane', 'wind_direction', 'wind_speed', 'time']
            if int(item['fcstTime'][0:2]) < 10:
                data[i % 6][9] = item['fcstTime'][1]
            else:
                data[i % 6][9] = item['fcstTime'][0:2]

        # 강수 형태 (PTY)
        # Add few more options
        elif 6 <= i < 12:
            data[i % 6][3] = item['fcstValue']
            if item['fcstValue'] == '0':
                continue
            elif item['fcstValue'] == '1':
                data[i % 6][3] = '☔비'
            elif item['fcstValue'] == '2':
                data[i % 6][3] = '🌧비/눈'
            elif item['fcstValue'] == '5':
                data[i % 6][3] = '💦빗방울'
            elif item['fcstValue'] == '6':
                data[i % 6][3] = '💦빗방울눈날림'
            elif item['fcstValue'] == '7':
                data[i % 6][3] = '❄️눈날림'
            else:
                data[i % 6][3] = '⚠️API 에러'


        # 강수량 (RN1)
        elif 12 <= i < 18:
            data[i % 6][4] = item['fcstValue']

        # 하늘 상태 (SKY)
        # Add few more options
        elif 18 <= i < 24:
            if item['fcstValue'] == '1':
                data[i % 6][1] = '☀️'
                data[i % 6][2] = '맑음'
            elif item['fcstValue'] == '3':
                data[i % 6][1] = '🌥'
                data[i % 6][2] = '구름많음'
            elif item['fcstValue'] == '4':
                data[i % 6][1] = '☁️'
                data[i % 6][2] = '흐림'
            else:
                data[i % 6][1] = '⚠️'
                data[i % 6][2] = 'API 에러'

        # 기온 (TH1)
        elif 24 <= i < 30:
            data[i % 6][0] = item['fcstValue']

        # 습도 (REH)
        elif 30 <= i < 36:
            data[i % 6][5] = item['fcstValue']

        # 풍향 (VEC)
        elif 48 <= i < 54:
            data[i % 6][6] = item['fcstValue']
            direction_num = int((int(item['fcstValue']) + 22.5 * 0.5) / 22.5)
            data[i % 6][7] = direction[direction_num]

        # 풍속 (WSD)
        elif 54 <= i < 60:
            data[i % 6][8] = item['fcstValue']
    return today, data
