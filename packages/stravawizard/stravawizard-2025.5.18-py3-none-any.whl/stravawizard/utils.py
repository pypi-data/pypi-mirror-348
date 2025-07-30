import logging
import datetime
from functools import singledispatch, wraps

logger = logging.getLogger(__name__)


def requires_ready(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.is_ready:
            msg = f"Cannot execute '{func.__name__}' when is_ready is False."
            logger.error(msg)
            raise ValueError(msg)
        return func(self, *args, **kwargs)

    return wrapper


@singledispatch
def convert_to_timestamp(input_date):
    """
    Converts various date formats to UNIX timestamp.
    Base implementation for unsupported types.

    Args:
        input_date: Date in an unsupported format

    Raises:
        ValueError: For unsupported input types
    """
    logger.error(f"Unsupported input type: {type(input_date)}")
    raise ValueError("Unsupported input type")


@convert_to_timestamp.register
def _(input_date: int) -> int:
    """Convert integer timestamp to integer timestamp (identity)"""
    return input_date


@convert_to_timestamp.register
def _(input_date: float) -> int:
    """Convert float timestamp to integer timestamp"""
    return int(input_date)


@convert_to_timestamp.register
def _(input_date: datetime.datetime) -> float:
    """Convert datetime object to timestamp"""
    return input_date.timestamp()


@convert_to_timestamp.register
def _(input_date: datetime.date) -> int:
    """Convert date object to timestamp"""
    date_object = datetime.datetime.combine(input_date, datetime.time.min)
    return int(date_object.timestamp())


@convert_to_timestamp.register
def _(input_date: str) -> float:
    """
    Convert string date to timestamp
    Supports formats: '%Y-%m-%d %H:%M:%S' and '%Y-%m-%d'
    """
    try:
        date_object = datetime.datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            date_object = datetime.datetime.strptime(input_date, "%Y-%m-%d")
        except ValueError:
            logger.error("Unsupported date format: %s", input_date)
            raise ValueError("Unsupported date format")
    return date_object.timestamp()
