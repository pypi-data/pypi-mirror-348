from datetime import datetime
from typing import Literal

from ..logging import logger

class ContextTimer:
    message: str
    log_mode: Literal["default", "logger", "print"]
    time_mode: Literal["default", "hms", "seconds"]
    start_time: datetime
    
    def __init__(
        self, 
        message: str = "spent time",
        log_mode: Literal["default", "logger", "print"] = "logger",
        time_mode: Literal["default", "hms", "seconds"] = "hms",
    ):
        self.message = message
        self.log_mode = log_mode
        self.time_mode = time_mode
        
    def __enter__(self):
        self.start_time = datetime.now()
        
    async def __aenter__(self):
        self.start_time = datetime.now()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = datetime.now()
        match self.time_mode:
            case "hms":
                duration = end_time - self.start_time
            case "seconds":
                duration = (end_time - self.start_time).total_seconds()
            case _:
                duration = end_time - self.start_time
        match self.log_mode:
            case "logger":
                logger.info(f"{self.message}: {duration}", stacklevel=2)
            case "print":
                print(f"{self.message}: {duration}")
            case _:
                logger.info(f"{self.message}: {duration}", stacklevel=2)
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        end_time = datetime.now()
        match self.time_mode:
            case "hms":
                duration = end_time - self.start_time
            case "seconds":
                duration = (end_time - self.start_time).total_seconds()
            case _:
                duration = end_time - self.start_time
        match self.log_mode:
            case "logger":
                logger.info(f"{self.message}: {duration}", stacklevel=2)
            case "print":
                print(f"{self.message}: {duration}")
            case _:
                logger.info(f"{self.message}: {duration}", stacklevel=2)
