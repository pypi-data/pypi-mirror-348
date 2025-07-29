__all__ = ["formatter"]

import functools
from typing import Any

from .schema import str_fmt_type

def message(timestamp: float, message: Any) -> str:
    return f"{timestamp} | {message}"
def formatter(timestamp: float) -> str_fmt_type:
    return functools.partial(message, timestamp)