import requests
from bs4 import BeautifulSoup

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
    second_values = [element.text.strip() for element in second_elements if
                     element.text.strip() and not any(c in element.text for c in ('{', '}', '[', ']'))][:3]
    third_values = [element.text.strip() for element in third_elements if
                    element.text.strip() and not any(c in element.text for c in ('{', '}', '[', ']'))][:3]
    fourth_values = [element.text.strip() for element in fourth_elements if
                     element.text.strip() and not any(c in element.text for c in ('{', '}', '[', ']'))][:3]
    return second_values, third_values, fourth_values


def nowCrawling(code):
    url = "https://investing.com/search/?q=" + code + "&tab=quotes"
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
    name = soup.find('h1',
                     class_='text-xl text-left font-bold leading-7 md:text-3xl md:leading-8 mb-2.5 md:mb-2 text-[#232526] rtl:soft-ltr').text
    market = soup.find("span", class_="text-xs leading-4 font-normal overflow-hidden text-ellipsis flex-shrink").text
    price_now = soup.find('div',
                          class_='text-5xl font-bold leading-9 md:text-[42px] md:leading-[60px] text-[#232526]').text
    div_tags = soup.find_all('div', class_='text-base font-bold leading-6 md:text-xl md:leading-7 rtl:force-ltr')

    values = []
    # 각 <div> 태그에서 값 추출
    for div_tag in div_tags:
        value = div_tag.text.strip('()')
        values.append(value)

    price_change = values[0]
    price_change_percent = values[1]
    return name, market, price_now, price_change, price_change_percent
