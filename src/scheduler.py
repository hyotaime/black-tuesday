from apscheduler.schedulers.asyncio import AsyncIOScheduler
from log import logger

logger.warn(f"Scheduler started.")

scheduler = AsyncIOScheduler()
