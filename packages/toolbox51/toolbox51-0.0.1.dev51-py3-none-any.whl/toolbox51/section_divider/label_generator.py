from typing import Generator, Iterator
# from pydantic import BaseModel

#TODO 对于迭代器用尽时的检查

class LabelGenerator:
    r"""
    - prefix不包含前置空格
    - suffix不包含后置空格
    """
    
    _prefix:str
    _suffix:str
    _ordinal_indicator:Iterator[str]
    
    _current_label:str
    _next_label:str
    
    @property
    def CurrentLabel(self) -> str:
        return self._current_label
    @property
    def NextLabel(self) -> str:
        return self._next_label
    
    @property
    def Prefix(self) -> str:
        return self._prefix
    @property
    def Suffix(self) -> str:
        return self._suffix
    
    def __init__(
        self,
        ordinal_indicator: list[str]|Iterator[str] = [],
        prefix: str = "",
        suffix: str = "",
        root: bool = False,
    ):
        if(root):
            # 根节点的空生成器
            self._prefix = self._suffix = self._current_label = self._next_label = ""
            return
        self._prefix = prefix
        self._suffix = suffix
        if isinstance(ordinal_indicator, list):
            self._ordinal_indicator = iter(ordinal_indicator)
        self._ordinal_indicator = ordinal_indicator if isinstance(ordinal_indicator, Iterator) else iter(ordinal_indicator)
        # 初始化时，CurrentLabel中储存第一项，NextLabel中储存第二项，__next__则往后平移。
        self._current_label = self._prefix + next(self._ordinal_indicator) + self._suffix
        self._next_label = self._prefix + next(self._ordinal_indicator) + self._suffix
    
    def __iter__(self):
        return self
    
    def __next__(self):
        self._current_label = self._next_label
        self._next_label = self._prefix + next(self._ordinal_indicator) + self._suffix
        return self._current_label