# shared_architecture/utils/custom_types.py

from sqlalchemy.types import TypeDecorator, DateTime
from datetime import datetime
import pytz

class TimezoneAwareDateTime(TypeDecorator):
    """
    Stores datetime as UTC in DB, converts to timezone-aware datetime in Python.
    """
    impl = DateTime(timezone=True)

    def process_bind_param(self, value, dialect):
        if value is not None:
            if value.tzinfo is None:
                # Assume UTC if not provided
                value = pytz.utc.localize(value)
            return value.astimezone(pytz.utc)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return value.replace(tzinfo=pytz.utc)
        return value
