# black-T.U.E.S.D.A.Y
![Python](https://img.shields.io/badge/python-3.11-3670A0?logo=python&logoColor=white)
![Python-Telegram-Bot](https://img.shields.io/badge/python--telegram--bot-blue?logo=pypi&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?logo=telegram&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-003545?logo=mariadb)
![OpenAI](https://img.shields.io/badge/OpenAI-000000?logo=OpenAI&logoColor=white)
![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?logo=openai&logoColor=white)
![Yahoo!](https://img.shields.io/badge/Yahoo!-6001D2?logo=Yahoo!&logoColor=white)
![Korea public data portal](https://img.shields.io/badge/Korea_public_data_portal-blue)

Telegram-bot Ultimately Essential Service Definitively Assist You

<img width="200" height="200" alt="bt-profile" src="https://github.com/hyotaime/black-tuesday/assets/109580929/9210d736-a41a-4749-83b9-1f43c3401ee3"/>

## Introduction
This is a bot project that provides various convenience functions using 
[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

Initially, it was developed for the purpose of a stock alert bot, so it was named Black Tuesday, 
which refers to the last day of the 1929 Wall Street crash.
___
## Release
You can use the latest version of the bot in the Releases on the right.
The current latest version is **[v1.0-beta2](https://github.com/hyotaime/black-tuesday/releases/tag/v1.0-beta2)**.

You can also use the bot by adding [@black_tuesday_bot](https://t.me/black_tuesday_bot) to your Telegram.
___
## Commands
* `/start` - Start the bot<br><img width="488" alt="start" src="https://github.com/hyotaime/black-tuesday/assets/109580929/72389170-4a70-46f0-a885-4f18619b8716">
* `/help` - Show command list<br><img width="488" alt="help" src="https://github.com/hyotaime/black-tuesday/assets/109580929/b0251d00-4a96-4894-8167-3279e336699b">
* `/alarm` - Show alarm list<br><img width="488" alt="alarm" src="https://github.com/hyotaime/black-tuesday/assets/109580929/e1ce3985-c573-4580-8acc-be590c50b0cb"><br><img width="488" alt="alarm_list" src="https://github.com/hyotaime/black-tuesday/assets/109580929/ce630eb4-1699-438f-9594-5528cc5bbccf"><br><img width="488" alt="alarm_gif" src="https://github.com/hyotaime/black-tuesday/assets/109580929/35ae7b6e-3b41-4e71-890b-1ff5ac0127fc">
  * `/alarm [alarm time]` - Set an alarm at the specified time<br><img width="488" alt="alarm_time" src="https://github.com/hyotaime/black-tuesday/assets/109580929/d2b32082-2deb-48b5-bdf1-b21ce916afea">
  * `/alarm [alarm index]` - Remove the alarm at the specified index<br><img width="488" alt="alarm_index" src="https://github.com/hyotaime/black-tuesday/assets/109580929/643f0e20-1baf-461c-8bd5-e55375568941">
  * `/alarm [alarm ID]` - Remove the alarm with the specified ID<br><img width="488" alt="alarm_id" src="https://github.com/hyotaime/black-tuesday/assets/109580929/973997c6-c4c4-42f4-9ca5-b202b64ac789">
  * `/alarm all` - Remove all alarms<br><img width="488" alt="alarm_all" src="https://github.com/hyotaime/black-tuesday/assets/109580929/7f1ca396-46b6-414c-8a09-3a31fff6df5f">
* `/search [search value]`- Search anything you want at google.com<br><img width="488" alt="search" src="https://github.com/hyotaime/black-tuesday/assets/109580929/913e854e-dee2-45ea-8c12-efd3d6f30dff">
* `/weather` - Show weather information<br><img width="488" alt="weather" src="https://github.com/hyotaime/black-tuesday/assets/109580929/e08731a4-9679-4d81-b527-f88cfb06cd7f">
  * `/weather [weather notification time]` - Set weather notification every day at the specified time<br><img width="488" alt="weather_noti" src="https://github.com/hyotaime/black-tuesday/assets/109580929/e1d42904-0841-4995-9c78-9fc200dfd25a">
  * `/weather off` - Turn off weather notification<br><img width="488" alt="weather_off" src="https://github.com/hyotaime/black-tuesday/assets/109580929/76c3377d-3aee-4459-a5b4-23b63a0c2c8e">
* `/setloc [x-coordinate] [y-coordinate]` - Set location for weather command<br><img width="488" alt="setloc" src="https://github.com/hyotaime/black-tuesday/assets/109580929/fb33ac7b-6835-4924-a31f-faacdf395568">
* `/kbo` - Show KBO league table<br><img width="488" alt="kbo" src="https://github.com/hyotaime/black-tuesday/assets/109580929/d1688929-443b-4453-b360-e1bbeb4afa44">
* `/kbonow` - Show today's KBO game schedule<br><img width="488" alt="kbonow" src="https://github.com/hyotaime/black-tuesday/assets/109580929/2fe53c01-51de-419d-8e36-54f60d2137de">
* `/npb` - Show NPB league table<br><img width="488" alt="npb" src="https://github.com/hyotaime/black-tuesday/assets/109580929/59d819d5-22a2-4517-b75b-d1a34c87899e">
* `/npbnow` - Show today's NPB game schedule<br><img width="488" alt="npbnow" src="https://github.com/hyotaime/black-tuesday/assets/109580929/015697eb-c4a6-4e25-a47b-7ba8acffea8e">
* `/gpt [ask value]` - Ask anything to chatGPT<br><img width="488" alt="gpt" src="https://github.com/hyotaime/black-tuesday/assets/109580929/582bac8d-703f-4a1a-b6c7-2cdc954506a1">
* `/gptkeyset [gpt API key]` - Set the API key for chatGPT<br><img width="488" alt="gptkeyset" src="https://github.com/hyotaime/black-tuesday/assets/109580929/ca14510b-fa47-4153-85a7-2ef1e5fef3a2">
* `/find [find value]` - Search stock ticker with company name<br><img width="488" alt="find" src="https://github.com/hyotaime/black-tuesday/assets/109580929/64626745-e52e-42e1-9373-82cd02b8b07b">
* `/now [stock ticker]` - Show real time price of the stock<br><img width="488" alt="now" src="https://github.com/hyotaime/black-tuesday/assets/109580929/e82d381e-467f-4cfc-9d3a-15f2d65cc3ff">
___
## Bug Report
If you find a bug, please report it in the Issues with **specific time** and **command** to let me know.
___
## About Files
* [`main.py`](src/main.py) - Main file of the bot
* [`log.py`](src/log.py) - Logging module
* [`scheduler.py`](src/scheduler.py) - Scheduler module
* [`database.py`](src/database.py) - Manage database
* [`crawling.py`](src/crawling.py) - Crawling module
* [`commands`](src/commands) directory
  * [`alarm.py`](src/commands/alarm.py) - Alarm command module
  * [`find.py`](src/commands/find.py) - Find command module
  * [`gpt.py`](src/commands/gpt.py) - GPT command module
  * [`help.py`](src/commands/help.py) - Help command module
  * [`kbo.py`](src/commands/kbo.py) - KBO command module
  * [`now.py`](src/commands/now.py) - Now command module
  * [`npb.py`](src/commands/npb.py) - NPB command module
  * [`search.py`](src/commands/search.py) - Search command module
  * [`start.py`](src/commands/start.py) - Start command module
  * [`weather.py`](src/commands/weather.py) - Weather command module
* [`requirements.txt`](requirements.txt) - Packages required to run the bot
___
## Reference
* Telegram Bot
  * [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
* Weather API (Meteorological Administration_Short-Term Forecast) for `/weather`
  * [Korea public data portal](https://www.data.go.kr/data/15084084/openapi.do)
  * [Usage of Weather API](https://github.com/az0t0/discord-seoultechbot/blob/main/src/weather.py)
* ChatGPT API for `/gpt`
  * [OpenAI API Reference Document](https://platform.openai.com/docs/api-reference)
* Ticker Search API for `/find`
  * [yashwanth2804's Ticker Search API](https://github.com/yashwanth2804/TickerSymbol)
* Yahoo Finance API for `/now`
  * Found the way to get information of the stock in the process of solving [yfinance issue #1729](https://github.com/ranaroussi/yfinance/issues/1729)
___
## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
