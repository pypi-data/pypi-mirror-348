import logging
from pathlib import Path
import asyncio

from ..utils import Colors, normalize_path


class Filter(logging.Filter):
    cwd:str|None
    home:str
    
    def __init__(
        self, 
        use_relative_path:bool = False, 
        log_task_id: bool = True,
    **kwargs) -> None:
        super().__init__(**kwargs)
        cwd = normalize_path(Path.cwd())
        home = normalize_path(Path.home())
        self.cwd = str(cwd) if(use_relative_path) else None
        self.home = str(home)
        self.log_task_id = log_task_id

    def filter(self, record: logging.LogRecord) -> bool:
        # print(record)
        # print(record.__dict__)
        if self.log_task_id:
            try:
                record._task_id = Colors.format(f"[{id(asyncio.current_task())}]", Colors.TASK_ID)
            except Exception:
                record._task_id = ""
        record._msecs = Colors.format(f".{int(record.msecs):03d}", Colors.TIME)
        record.levelname = f"{record.levelname: <8}"
        if(self.cwd and record.pathname.startswith(self.cwd)):
            record.pathname = record.pathname.replace(self.cwd, ".")
        elif self.home not in {"\\", "/"}:
            record.pathname = record.pathname.replace(self.home, "~")
        # record.pathname = record.pathname.replace("\\", "/")
        record._locate = Colors.format(f"{record.pathname}:{record.lineno}", Colors.LOCATE)
        record.funcName = Colors.format(record.funcName, Colors.FUNC_NAME)
        match record.levelno:
            case logging.DEBUG:
                record.levelname = Colors.format(record.levelname, Colors.DEBUG)
                record.msg = Colors.format(record.msg, Colors.DEBUG_MSG)
            case logging.INFO:
                record.levelname = Colors.format(record.levelname, Colors.INFO)
                record.msg = Colors.format(record.msg, Colors.INFO_MSG)
            case logging.WARNING:
                record.levelname = Colors.format(record.levelname, Colors.WARNING)
                record.msg = Colors.format(record.msg, Colors.WARNING_MSG)
            case logging.ERROR:
                record.levelname = Colors.format(record.levelname, Colors.ERROR)
                record.msg = Colors.format(record.msg, Colors.ERROR_MSG)
            case logging.CRITICAL:
                record.levelname = Colors.format(record.levelname, Colors.CRITICAL)
                record.msg = Colors.format(record.msg, Colors.CRITICAL_MSG)
            case _:
                raise ValueError(f"Invalid log level: {record.levelno}")
        
        record._eol = "\n" if "\n" in record.msg else ""
        return True
    
def get_handler(
    # name:str, 
    level:int = logging.INFO,
    fmt:str = """ \
%(asctime)s%(_msecs)s | %(levelname)s | %(locate)s | %(funcName)s - %(message)s \
""",
    # datefmt:str = Colors.format("%Y-%m-%d %H:%M:%S", Colors.TIME)
    datefmt:str = "%Y-%m-%d %H:%M:%S",
    use_relative_path:bool = False,
    log_task_id: bool = True,
) -> logging.Handler:
    
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(fmt, Colors.format(datefmt, Colors.TIME)))
    handler.addFilter(Filter(use_relative_path=use_relative_path, log_task_id=log_task_id))

    # logger = logging.getLogger(name)
    # logger.setLevel(level)
    # logger.addHandler(ch)
    return handler