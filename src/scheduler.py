from apscheduler.schedulers.asyncio import AsyncIOScheduler
from log import logger

logger.warn(f"Scheduler started.")

weather_alarm_job = None

scheduler = AsyncIOScheduler()
