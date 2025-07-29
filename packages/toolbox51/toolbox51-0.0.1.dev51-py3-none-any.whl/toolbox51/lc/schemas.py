__all__ = ["ChainTypesMeta", "ChainParams", "ChainResult"]

from typing import Generic, TypeVar
from langserve.schema import CustomUserType

class ChainTypesMeta(type):
    """禁止实例化"""
    def __call__(cls, *args, **kwargs):
        raise TypeError("{cls.__name__} should not be instantiated")
    
InputSettings = TypeVar("InputSettings")
InputContent = TypeVar("InputContent")
class ChainParams(CustomUserType, Generic[InputSettings, InputContent]):
    timestamp: float | None = None
    settings: InputSettings | None = None
    content: InputContent | None = None
    extra: dict = {}
    
OutputInfo = TypeVar("OutputInfo")
OutputContent = TypeVar("OutputContent")
class ChainResult(CustomUserType, Generic[OutputInfo, OutputContent]):
    timestamp: float
    info: OutputInfo
    content: OutputContent
    extra: dict = {}    