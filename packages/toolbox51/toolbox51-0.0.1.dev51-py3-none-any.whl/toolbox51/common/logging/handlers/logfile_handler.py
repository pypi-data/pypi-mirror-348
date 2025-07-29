import logging
from pathlib import Path
from datetime import datetime
import asyncio

from ..utils import normalize_path

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
                record._task_id = f"[{id(asyncio.current_task())}]"
            except Exception:
                record._task_id = ""
        record._msecs = f".{int(record.msecs):03d}"
        record.levelname = f"{record.levelname: <8}"
        if(self.cwd and record.pathname.startswith(self.cwd)):
            record.pathname = record.pathname.replace(self.cwd, ".")
        elif self.home not in {"\\", "/"}:
            record.pathname = record.pathname.replace(self.home, "~")
        # record.pathname = record.pathname.replace("\\", "/")
        record._locate = f"{record.pathname}:{record.lineno}"
        record.funcName = record.funcName
        match record.levelno:
            case logging.DEBUG:
                record.levelname = record.levelname
                record.msg = record.msg
            case logging.INFO:
                record.levelname = record.levelname
                record.msg = record.msg
            case logging.WARNING:
                record.levelname = record.levelname
                record.msg = record.msg
            case logging.ERROR:
                record.levelname = record.levelname
                record.msg = record.msg
            case logging.CRITICAL:
                record.levelname = record.levelname
                record.msg = record.msg
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
    logfile_path: str|Path|None = None,
) -> logging.Handler:
    
    match logfile_path:
        case str():
            root = Path(logfile_path)
        case Path():
            root = logfile_path
        case _:
            root = Path("logs")
    root.mkdir(exist_ok=True)
    filepath = root / f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    handler = logging.FileHandler(str(filepath))
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(fmt, datefmt))
    handler.addFilter(Filter(use_relative_path=use_relative_path, log_task_id=log_task_id))

    # logger = logging.getLogger(name)
    # logger.setLevel(level)
    # logger.addHandler(ch)
    return handler