


import asyncio
import logging
import uuid
from typing import Coroutine

from ..singleton import SingletonMeta
from ..logging import touch_logger

class Task:
    id: uuid.UUID
    task: asyncio.Task
    logger: logging.Logger
    
    def __init__(
        self,
        id: uuid.UUID,
        task: asyncio.Task,
        logger: logging.Logger
    ):
        self.id = id
        self.task = task
        self.logger = logger

class TaskManager(metaclass=SingletonMeta):
    
    task_map: dict[str, Task] = {}
    logger: logging.Logger
    
    def __init__(self):
        self.logger = touch_logger("GLOBAL", level=logging.DEBUG)
    
    # task相关
    
    def create_task(self, coro:Coroutine) -> asyncio.Task:
        id = uuid.uuid4()
        name = id.hex
        coro_task = asyncio.create_task(coro, name=name)
        self.register(id, coro_task)
        coro_task.add_done_callback(lambda task: self.unregister(name))
        return coro_task
    
    def register(self, id:uuid.UUID, coro_task:asyncio.Task):
        name = id.hex
        if(name in self.task_map):
            self.logger.debug(f"任务{name}已存在，注册失败。")
            raise Exception(f"任务{name}已存在，注册失败。")
        logger = touch_logger(name, level=logging.DEBUG)
        task = Task(id, coro_task, logger)
        self.task_map[name] = task
        
    def unregister(self, name:str):
        if(name not in self.task_map):
            self.logger.debug(f"任务{name}不存在，注销失败。")
            raise Exception(f"任务{name}不存在，注销失败。")
    
        task = self.task_map[name]
        if not task.task.done():
            raise Exception(f"任务{task.id}尚未完成时尝试注销任务。")
        self.task_map.pop(name)

        assert(task.id.hex == task.logger.name)
        handlers = task.logger.handlers[:]
        for handler in handlers:
            task.logger.removeHandler(handler)
            handler.close()
        if task.logger.name in logging.Logger.manager.loggerDict:
            logging.Logger.manager.loggerDict.pop(task.logger.name)
        self.logger.info(f"任务{task.id}已完成，注销志记录器。")
        
        del task
        
    # logger相关
        
    # @property
    # def current_name(self) -> str:
    #     current_task = asyncio.current_task()
    #     current_name = current_task.get_name() if current_task else "GLOBAL"
    #     return current_name
    
    @property
    def current_name(self) -> str:
        try:
            current_task = asyncio.current_task()
            current_name = current_task.get_name() if current_task else "GLOBAL"
            if(current_name not in self.task_map):
                self.logger.debug(f"当前任务{current_name}未注册，使用全局记录器。")
                current_name = "GLOBAL"
        except RuntimeError:
            # 如果不在协程或没有事件循环，返回 "GLOBAL"
            current_name = "GLOBAL"
        return current_name

    
    @property
    def current_logger(self) -> logging.Logger:
        current_name = self.current_name
        return logging.getLogger(name=current_name)
    
    def debug(self, msg:object):
        msg_s = self._obj2str(msg)
        self.current_logger.debug(msg_s)
    
    def info(self, msg:object):
        msg_s = self._obj2str(msg)
        self.current_logger.info(msg_s)
    
    def warning(self, msg:object):
        msg_s = self._obj2str(msg)
        self.current_logger.warning(msg_s)
    
    def error(self, msg:object):
        msg_s = self._obj2str(msg)
        self.current_logger.error(msg_s)
    
    def critical(self, msg:object):
        msg_s = self._obj2str(msg)
        self.current_logger.critical(msg_s)
    
    def _obj2str(self, obj:object) -> str:
        match obj:
            case str():
                return obj
            case int() | float() | bool():
                return str(obj)
            case _:
                return str(obj)