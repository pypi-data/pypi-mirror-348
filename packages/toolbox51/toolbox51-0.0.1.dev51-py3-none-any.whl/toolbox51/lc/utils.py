__all__ = ["trust_last", "ChainBuilder", "ChainFactory"]

import functools
from collections.abc import Callable
from typing import Literal
from abc import ABC, abstractmethod

from langchain_core.runnables import Runnable
from langserve import RemoteRunnable

# langgraph

def trust_last(x, y):
    return x if y is None else y


# chain: 为了remote与local隔离，factory与type部分需要避免import专用模块

class ChainBuilder(ABC):
    @abstractmethod
    def build_all(self, *args, **kwargs) -> "ChainBuilder":
        raise NotImplementedError
    
    @property
    @abstractmethod
    def Chain(self) -> Runnable:
        raise NotImplementedError

class ChainFactory(ABC):
    _local_params:dict
    
    @abstractmethod
    def create(self, *args, **kwargs) -> Runnable:
        raise NotImplementedError
    
    def _create(
        self,
        mode: Literal["local","remote"] = "local",
        remote_url: str|None = None,
        remote_timeout: float|None = None,
    ) -> Runnable:
        match mode:
            case "remote":
                if(not remote_url):
                    raise ValueError("remote_url不能为空")
                return self._create_remote(remote_url, remote_timeout)
            case "local":
                if(getattr(self, "_local_params", None) is None):
                    self._local_params = {}
                return self._create_with_builder()
        raise ValueError(f"mode {mode} 无效")
    
    def _create_remote(
        self,
        remote_url: str,
        remote_timeout: float|None = None,
    ) -> RemoteRunnable:
        return RemoteRunnable(url=remote_url, timeout=remote_timeout)
    
    def _create_with_builder(self) -> Runnable:
        return self._get_builder().build_all(**self._local_params).Chain
    
    @abstractmethod
    def _get_builder(self) -> ChainBuilder:
        raise NotImplementedError
    
    def _set_local_params(self, *args, **kwargs) -> None:
        raise DeprecationWarning
        if(args):
            raise ValueError("本地模式不支持传入位置参数")
        self._local_params = kwargs

