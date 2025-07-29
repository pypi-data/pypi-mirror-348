from enum import Enum

class Colors(Enum):
    
    # base colors
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'
    
    # high intensity colors
    RED_HI = '\033[1;31m'
    GREEN_HI = '\033[1;32m'
    YELLOW_HI = '\033[1;33m'
    BLUE_HI = '\033[1;34m'
    MAGENTA_HI = '\033[1;35m'
    CYAN_HI = '\033[1;36m'
    WHITE_HI = '\033[1;37m'
    
    # background colors
    RED_BG = '\033[41m'
    GREEN_BG = '\033[42m'
    YELLOW_BG = '\033[43m'
    BLUE_BG = '\033[44m'
    MAGENTA_BG = '\033[45m'
    CYAN_BG = '\033[46m'
    WHITE_BG = '\033[47m'
    
    # background high intensity colors
    RED_BG_HI = '\033[1;41m'
    GREEN_BG_HI = '\033[1;42m'
    YELLOW_BG_HI = '\033[1;43m'
    BLUE_BG_HI = '\033[1;44m'
    MAGENTA_BG_HI = '\033[1;45m'
    CYAN_BG_HI = '\033[1;46m'
    WHITE_BG_HI = '\033[1;47m'
    
    # logger strategies
    DEBUG = BLUE_HI
    DEBUG_MSG = DEBUG
    INFO = WHITE_HI
    INFO_MSG = INFO
    WARNING = YELLOW_HI
    WARNING_MSG = WARNING
    ERROR = RED_HI
    ERROR_MSG = ERROR
    CRITICAL = RED_BG_HI
    CRITICAL_MSG = CRITICAL
    
    LOCATE = CYAN
    TIME = GREEN
    FUNC_NAME = WHITE
    TASK_ID = WHITE
    
    @classmethod
    def format(cls, text, color=None):
        if(color is None):
            return text
        return f"{color.value}{text}{Colors.RESET.value}"
    
    
FMTDCIT = {
    'ERROR'   : "\033[31mERROR   \033[0m",
    'INFO'    : "\033[37mINFO    \033[0m",
    'DEBUG'   : "\033[1mDEBUG   \033[0m",
    'WARN'    : "\033[33mWARN    \033[0m",
    'WARNING' : "\033[33mWARNING \033[0m",
    'CRITICAL': "\033[35mCRITICAL\033[0m",
}