import functools
from typing import Callable
import traceback


from ..logging import logger


def wrapper_factory_default(func: Callable, message: str):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"{message} start", stacklevel = 2)
        result = func(*args, **kwargs)
        logger.info(f"{message} end", stacklevel = 2)
        return result
    return wrapper

def wrapper_factory_with_exceptions(func: Callable, message: str):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"{message} start", stacklevel = 2)
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logger.warning(f"{message} failed with exception: {e}")
            traceback.print_exc()
            result = None #TODO: 是否需要根据参数数量返回默认值？
        logger.info(f"{message} end", stacklevel = 2)
        return result
    return wrapper


def func_logger(
    *args, 
    message = "", with_exceptions = False,
):
    """
    装饰器函数，用于记录函数的调用信息，也可以用于处理函数的异常。
    注意如果用来处理函数异常，那么异常时会返回None。
    如果要使用此功能，需要在调用函数时对结果进行判断，再进行拆包。
    """
    
    assert(isinstance(message, str))
    assert(isinstance(with_exceptions, bool))
    
    match len(args):
        case 0:
            ...
        case 1:
            x = args[0]
            if(isinstance(x, str) and not message):
                message = x
            elif(isinstance(x, bool) and not with_exceptions):
                with_exceptions = x
            elif(callable(x)): # 直接调用@func_logger
                assert(not message)
                assert(not with_exceptions)
                wrapper = wrapper_factory_default(x, x.__name__)
                return wrapper
        case 2:
            assert(not message)
            assert(not with_exceptions)
            message = args[0]
            with_exceptions = args[1]
        case _:
            logger.warning("too many args")

    wrapper_factory = wrapper_factory_with_exceptions if(with_exceptions) else wrapper_factory_default
    
    def f(func):
        wrapper = wrapper_factory(func, message or func.__name__)
        return wrapper
    return f


if(__name__ == "__main__"):

    @func_logger
    def func1(p):
        """test"""
        logger.info(p)
        return 1
        
    print(func1)
    func1(2)

    @func_logger(True)
    def func2(p):
        """test"""
        logger.info(p)
        return 1
        
    print(func2)
    func2(2)