import warnings
import string
from pathlib import Path


# 用 PartialDict 保留未填充的字段
class PartialDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'

formatter = string.Formatter()

class Template:
        
    @property
    def Content(self) -> str:
        """返回当前字符串，未填充的字段用<xxx>表示"""
        x = self._current
        for _, field_name, _, _ in formatter.parse(x):
            if field_name is not None:
                x = x.replace(f'{{{field_name}}}', f'<{field_name}>')
        return x
    
    def __init__(
        self, 
        template: str|None = None, 
        *,
        filename: str|Path|None = None,
    ):
        if template is None:
            assert filename is not None, "filename must be provided if template is None"
            with open(str(filename), 'r', encoding='utf-8') as f:    
                template = f.read()
        self._template = template
        self._current = template
        
    @classmethod
    def from_file(cls, filename: str|Path) -> 'Template':
        """从文件中读取模板"""
        return cls(filename=filename)

    

    def format(self, **kwargs) -> 'Template':
        """分批次填充"""
        self._current = self._current.format_map(PartialDict(**kwargs))
        return self

    def __str__(self) -> str:
        """返回当前字符串"""
        if self._has_unfilled():
            warnings.warn(f"StringFormatter warning: still has unfilled placeholders in '{self._current}'")
        return self._current

    def _has_unfilled(self):
        """检查还有没有 {xxx} 占位符"""
        for _, field_name, _, _ in formatter.parse(self._current):
            if field_name is not None:
                return True
        return False

    def reset(self) -> 'Template':
        """重置回最初的模板"""
        self._current = self._template
        return self
