import logging
from pathlib import Path

from ..handlers import get_console_handler, get_logfile_handler

def check_logger(name:str) -> bool:
    logger_dict = logging.Logger.manager.loggerDict
    return name in logger_dict
    
def new_logger(
    name: str, 
    debug: bool = __debug__, auto_config: bool = False,
    # ---
    level: int = logging.INFO,
    use_relative_path: bool = False,
    use_logfile: bool = False, logfile_path: str|Path|None = None,
    log_task_id: bool = True,
) -> logging.Logger:
    
    if auto_config:
        level = logging.DEBUG if debug else logging.INFO
        use_relative_path = True
        use_logfile = False
        log_task_id = True
        
    fmt_prefix_items: list[str] = []
    if log_task_id:
        fmt_prefix_items.append("%(_task_id)s")
    fmt_prefix = " | ".join(fmt_prefix_items)
    
    fmt_info_items: list[str] = []
    fmt_info_items.append("%(asctime)s%(_msecs)s")
    fmt_info_items.append("%(levelname)s")
    fmt_info_items.append("%(_locate)s")
    fmt_info_items.append("%(funcName)s - ")
    fmt_info = " | ".join(fmt_info_items)
    
    fmt_suffix_items: list[str] = []
    fmt_suffix_items.append("%(_eol)s")
    fmt_suffix = "".join(fmt_suffix_items)
    
    fmt_msg = "%(message)s"
    fmt = f"{fmt_prefix}{fmt_info}{fmt_suffix}{fmt_msg}"
    datefmt = "%Y-%m-%d %H:%M:%S"
    

    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.propagate = False # 禁止向上传播，屏蔽掉父类的日志记录
    logger.setLevel(level)
    if(use_logfile):
        logger.addHandler(get_logfile_handler(
            level = level,
            fmt = fmt,
            datefmt = datefmt,
            use_relative_path = use_relative_path,
            log_task_id = log_task_id,
            logfile_path = logfile_path,
        ))
    logger.addHandler(get_console_handler(
        level = level,
        fmt = fmt,
        datefmt = datefmt,
        use_relative_path = use_relative_path,
        log_task_id = log_task_id,
    ))
    return logger

def get_logger(name:str):
    if(check_logger(name)):
        return logging.getLogger(name)
    else:
        return new_logger(name)

def touch_logger(
    name: str, 
    debug: bool = __debug__, auto_config: bool = False,
    # ---
    level: int = logging.INFO,
    use_relative_path: bool = False,
    use_logfile: bool = False, logfile_path: str|Path|None = None,
    log_task_id: bool = True,
) -> logging.Logger:
    if(check_logger(name)):
        return logging.getLogger(name)
    else:
        return new_logger(name, debug, auto_config, level, use_relative_path, use_logfile, logfile_path, log_task_id)
    
# def drop_logger(name:str):