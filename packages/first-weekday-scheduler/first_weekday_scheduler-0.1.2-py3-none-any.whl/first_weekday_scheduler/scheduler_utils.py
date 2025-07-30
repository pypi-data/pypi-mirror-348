# scheduler/scheduler_utils.py

from datetime import datetime
import pytz
from .config import FIRST_WEEKDAY, FIRST_WEEK_DAY_THRESHOLD, AFTER_HOUR, TIMEZONE

def is_first_weekday_evening():
    now = datetime.now(pytz.utc).astimezone(pytz.timezone(TIMEZONE))
    is_weekday = now.weekday() == FIRST_WEEKDAY
    first_week = now.day <= FIRST_WEEK_DAY_THRESHOLD
    after_hour = now.hour >= AFTER_HOUR
    return is_weekday and first_week and after_hour