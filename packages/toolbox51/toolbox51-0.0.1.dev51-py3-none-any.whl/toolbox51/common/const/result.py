from enum import Enum

class ResultEnum(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    
    
    
if __name__ == "__main__":
    print(ResultEnum.SUCCESS)
    print(ResultEnum.FAILURE)