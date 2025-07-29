from pydantic import BaseModel
from typing import Union


class Section(BaseModel):
    r"""
    label - 完整的标题编号，包含编号的前缀后缀，但不包含空格
    title - 文章标题/章节标题，不包含编号
    contents - 正文内容，为字符串或次级章节（Section）
    
    metadata - 预留的元信息存储位置，比如文件名、作者、发布日期等
    extra - 预留的额外信息存储位置，比如生成的摘要、标签、问答对等
    """
    
    label: str = ""
    title: str = ""
    contents: list[Union[str, "Section"]] = []
    
    metadata: dict = {}
    extra: dict = {}