# black-T.U.E.S.D.A.Y
Telegram-bot Ultimately Essential Service Definitively Assist You

<img src="https://github.com/hyotaime/black-tuesday/assets/109580929/9210d736-a41a-4749-83b9-1f43c3401ee3" width="200" height="200"/>

## Introduction
### English
This is a bot project that provides various convenience functions using 
[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

Initially, it was developed for the purpose of a stock alert bot, so it was named Black Tuesday, 
which refers to the last day of the 1929 Wall Street crash.

### 한국어
[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)을 이용하여 여러 편의 기능들을 제공하는 봇 프로젝트입니다.

초기에는 주식 알림 봇을 목적으로 개발하였기 때문에 1929년 월스트리트 대폭락의 마지막 날을 지칭하는 검은 화요일로 이름을 짓게 되었습니다.
___
## Release
You can use the latest version of the bot in the Releases on the right.
The current latest version is **[v1.0-beta1](https://github.com/hyotaime/black-tuesday/releases/tag/v1.0-beta1)**.

우측의 Releases에서 최신 버전의 봇을 사용할 수 있습니다.
현재 최신 버전은 **[v1.0-beta1](https://github.com/hyotaime/black-tuesday/releases/tag/v1.0-beta1)** 입니다.
___
## Commands
* `/help` - Show command list
* `/alarm` - Show alarm list
  * `/alarm [alarm time]` - Set an alarm at the specified time
  * `/alarm [alarm index]` - Remove the alarm at the specified index
  * `/alarm [alarm ID]` - Remove the alarm with the specified ID
  * `/alarm all` - Remove all alarms
* `/search [search value]`- Search anything you want at google.com
* `/weather` - Show weather information
  * `/weather [weather notification time]` - Set weather notification every day at the specified time
  * `/weather off` - Turn off weather notification
* `/setloc [x-coordinate] [y-coordinate]` - Set location for weather command using `기상청41_단기예보 조회서비스_오픈API활용가이드_격자_위경도(20230611).xlsx`
* `/kbo` - Show KBO league table
* `/kbonow` - Show today's KBO game schedule
* `/gpt [ask value]` - Ask anything to chatGPT
* `/gptkeyset [gpt API key]` - Set the key for chatGPT
* `/find [find value]` - Search stock ticker with company name
* `/now [stock ticker]` - Show real time price of the stock
___
## Bug Report
If you find a bug, please report it in the Issues with **specific time** and **command** to let me know.

버그를 발견하신다면, Issues에 **해당 시간**과 **명령어**를 명시하여 알려주시기 바랍니다.
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
  * [`search.py`](src/commands/search.py) - Search command module
  * [`start.py`](src/commands/start.py) - Start command module
  * [`weather.py`](src/commands/weather.py) - Weather command module
* [`requirements.txt`](requirements.txt) - Packages required to run the bot
___
## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details

이 프로젝트는 GNU General Public License v3.0으로 라이선스가 부여되어 있습니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하시기 바랍니다.
