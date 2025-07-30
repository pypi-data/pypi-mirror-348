# shared_architecture/utils/datetime_utils.py

from datetime import datetime, timezone
import pandas as pd

def utc_now() -> datetime:
    """Returns current UTC time as a timezone-aware datetime object."""
    return datetime.now(timezone.utc)

def format_datetime_utc(dt: datetime) -> str:
    """Formats a datetime object to UTC string format YYYY-MM-DD HH:MM:SS."""
    if dt is None:
        return ""
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
