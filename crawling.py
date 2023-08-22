import requests
from bs4 import BeautifulSoup


def find_crawling(find_value):
    url = "https://finance.yahoo.com/lookup?s="
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    response = requests.get(url + find_value, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')

    second_elements = soup.select('.second')
    third_elements = soup.select('.third')
    fourth_elements = soup.select('.fourth')

    # 내부 값이 기호나 공백이 아닌 경우에만 추출하여 리스트에 저장
    second_values = [element.text.strip() for element in second_elements if
                     element.text.strip() and not any(c in element.text for c in ('{', '}', '[', ']'))][:3]
    third_values = [element.text.strip() for element in third_elements if
                    element.text.strip() and not any(c in element.text for c in ('{', '}', '[', ']'))][:3]
    fourth_values = [element.text.strip() for element in fourth_elements if
                     element.text.strip() and not any(c in element.text for c in ('{', '}', '[', ']'))][:3]
    return second_values, third_values, fourth_values


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
    url = "https://www.koreabaseball.com/TeamRank/TeamRank.aspx"
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
        winning_percentage = columns[6].get_text()
        win_streak = columns[7].get_text()
        recent_wins = columns[9].get_text()

        team_data = {
            "Rank": rank,
            "Team Name": team_name,
            "Games Played": games_played,
            "Wins": wins,
            "Losses": losses,
            "Draws": draws,
            "Winning Percentage": winning_percentage,
            "Win Streak": win_streak,
            "Recent Wins": recent_wins
        }

        team_data_list.append(team_data)

    return team_data_list


def kbo_now_crawling():
    # https://velog.io/@hjw4287/BeautifulSoup%EB%A5%BC-%ED%86%B5%ED%95%9C-%EB%84%A4%EC%9D%B4%EB%B2%84-%EC%8A%A4%ED%8F%AC%EC%B8%A0-%ED%81%AC%EB%A1%A4%EB%A7%81
    # 위 블로그 참고함

    # 국내 야구
    url = "https://sports.news.naver.com/kbaseball/schedule/index"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, 'lxml')
    # naver에서 div를 날짜별 홀수와 짝수로 나누어 놓음
    soup_data = [soup.find_all("div", {"class": "sch_tb"}), soup.find_all("div", {"class": "sch_tb2"})]
    datalist = []
    for data_table in soup_data:
        for data in data_table:
            # 일자
            date_value = data.find("span", {"class": "td_date"}).text
            # 정렬을 위한 일자 포맷 통일
            if len(date_value.split(" ")[0].split(".")[1]) == 1:
                date_value = date_value.split(" ")[0].split(".")[0] + ".0" + date_value.split(" ")[0].split(".")[
                    1] + " " + date_value.split(" ")[1]
            match_cnt = data.find("td")["rowspan"]
            for i in range(int(match_cnt)):
                match_data = {"date": date_value,
                              "time": data.find_all("tr")[i].find("span", {"class": "td_hour"}).text}
                # 해당 일자에 경기가 없을 시 naver sports에서 match_data["time"] = "-" 반환
                if match_data["time"] != "-":
                    # 홈팀
                    match_data["home"] = data.find_all("tr")[i].find("span", {"class": "team_rgt"}).text
                    # 어웨이팀
                    match_data["away"] = data.find_all("tr")[i].find("span", {"class": "team_lft"}).text
                    # VS일 시 예정 경기
                    if data.find_all("tr")[i].find("strong", {"class": "td_score"}).text != "VS":
                        # 홈팀 점수
                        match_data["home_score"] = \
                        data.find_all("tr")[i].find("strong", {"class": "td_score"}).text.split(":")[1]
                        # 어웨이팀 점수
                        match_data["away_score"] = \
                        data.find_all("tr")[i].find("strong", {"class": "td_score"}).text.split(":")[0]
                    else:
                        match_data["home_score"] = "-"
                        match_data["away_score"] = "-"
                    # 중계
                    match_data["broadcast"] = data.find_all("tr")[i].find_all("span", {"class": "td_stadium"})[
                        0].text.strip().replace("\n", "").replace("\t", "")
                    # 경기장
                    match_data["stadium"] = data.find_all("tr")[i].find_all("span", {"class": "td_stadium"})[1].text
                else:
                    match_data["home"] = "-"
                    match_data["away"] = "-"
                    match_data["home_score"] = "-"
                    match_data["away_score"] = "-"
                    match_data["broadcast"] = "-"
                    match_data["stadium"] = "-"
                datalist.append(match_data)
    results = sorted(datalist, key=lambda k: (k["date"], k["time"]))
    return results
