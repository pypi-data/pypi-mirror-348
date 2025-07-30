import logging
import os
from typing import Any, Optional, Type, Union
from datetime import datetime, date
import pandas as pd

def validate_env_variable(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        logging.error(f"Environment variable {var_name} is not set.")
        raise ValueError(f"Missing environment variable: {var_name}")
    return value

def safe_int_conversion(value: str, default: int = 0) -> int:
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def format_date(date_obj: Union[datetime, date], format_string: str = "%Y-%m-%d") -> str:
    if isinstance(date_obj, (datetime, date)):
        return date_obj.strftime(format_string)
    return ""

def log_error(exception: Exception, context: str = ""):
    logging.error(f"Error in {context}: {exception}")

def safe_convert(value: Any, target_type: Type, default: Optional[Any] = None) -> Any:
    try:
        return target_type(value)
    except (ValueError, TypeError):
        return default

def safe_convert_int(value: Any, default: Optional[int] = None) -> Optional[int]:
    return safe_convert(value, int, default)

def safe_convert_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    return safe_convert(value, float, default)

def safe_convert_bool(value: Any, default: Optional[bool] = None) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        if value.lower() in ['true', '1', 'yes']:
            return True
        if value.lower() in ['false', '0', 'no']:
            return False
    return default

def safe_parse_datetime(date_input: Union[str, datetime, date, pd.Timestamp]) -> Optional[datetime]:
    if isinstance(date_input, datetime):
        return date_input
    if isinstance(date_input, (date, pd.Timestamp)):
        return datetime.combine(date_input, datetime.min.time())
    if isinstance(date_input, str):
        try:
            return pd.to_datetime(date_input).to_pydatetime()
        except Exception:
            return None
    return None

def safe_parse_date(date_input: Union[str, date, pd.Timestamp]) -> Optional[date]:
    dt = safe_parse_datetime(date_input)
    return dt.date() if dt else None