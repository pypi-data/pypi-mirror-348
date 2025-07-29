from typing import Tuple
import re

from toolbox51.logger import touch_logger, INFO, DEBUG
logger = touch_logger("GLOBAL", level=DEBUG)

from .section import Section
from .label_generator import LabelGenerator
from .misc.const import ORDINAL_INDICATOR_LIST, PREFIX_LIST, SUFFIX_LIST, BRACKETS_LIST
from .misc.const import REGEX_SPACE_CHARS

class SectionDivider:
    def __init__(self):
        ...
        
    def __call__(self, text:str|list[str], title:str|None=None):
        return self.divide_section(text, title)
        
    def divide_section(self, text:str|list[str], title:str|None=None, metadata:dict|None=None):
        lines = text.splitlines() if isinstance(text, str) else text
        section = Section(
            title = title or "",
            contents = [],
            metadata = metadata or {},
        )
        label_generator = LabelGenerator() # CurrentLabel为""时，表示处在根节点
        stack = [(section, label_generator)]
        
        idx = 0
        while(idx < len(lines)):
            line = lines[idx]
            logger.info(f"{idx}: {line}")
            if(self.__filter_line(line)):
                idx += 1
                continue
            # 后继序列
            if(stack[-1][1].CurrentLabel): # CurrentLabel为""时，表示处在根节点，没有已存在的序列
                if((_ := self.__check_exist_ordinal_indicator(line, stack)) is not None):
                    idx += 1
                    continue
            # 新序列
            if((_ := self.__check_new_ordinal_indicator(line, stack)) is not None):
                idx += 1
                continue
            self.__append_section(stack[-1][0], line)
            idx += 1
            continue
        
        #TODO 有疑问
        stack[-1][0].contents = stack[-1][0].contents[:-1] + self.__split_text(stack[-1][0].contents[-1])
        # 保存full_content
        self.get_full_content(outline)
        
        return outline
    
    def __filter_line(self, line:str) -> bool:
        r"""
        用于过滤掉一些特殊行，比如页脚等
        """
        if(line.startswith("—") and line.endswith("—")):
            return True
        return False
    
    def __append_section(self, section:Section, item:str|Section):
        r"""
        将文本/子段落添加到段落中
        """
        if(isinstance(item, Section)):
            section.contents.append(item)
        elif(section.contents == []):
            section.contents.append(item)
        elif(isinstance(section.contents[-1], str)):
            section.contents[-1] += item
        else:
            # 意味着上一个content是子段落，item是文本，即通过文本判断一个子段落结束了
            # 目前尚未实现此功能，所以暂时到不了这里
            # section.contents = section.contents[:-1] + self.__split_text(section.contents[-1])
            section.contents.append(item)
    
    def __check_exist_ordinal_indicator(self, line:str, stack:list[Tuple[Section, LabelGenerator]]) -> bool:
        r"""
        检查现有序号的后继
        - 需要考虑栈中的所有层级的后续
        
        stack:
            1.1.3 xxxx
            [1, 1.1, 1.1.3]
                     ^^^^^
            ->
            [1, 1.1, 1.1.4]
            ----
            1.1 xxxx
            [1, 1.1, 1.1.3]
                ^^^
            ->
            [1, 1.2]
        """
        logger.info(f"check_exist_ordinal_indicator: {line}")
        # logger.debug(f"{stack})
        for idx in range(len(stack)-1, 0, -1): # 从后往前遍历。idx还有用，不要“优化”为reversed。
            label_generator = stack[idx][1]
            next_label = label_generator.NextLabel
            # TODO 序号超限的处理
            
            # logger.debug(f"{s}, {prefix + indice + suffix}")
            start = line.find(next_label)
            if(start == -1):
                continue
            if(line[:start].lstrip() != ""):
                continue
            
            # 锁定序号
            content = line[start+len(next_label):]
            if(label_generator.CurrentLabel == "" and not content.startswith(" ")):
                # 没有后缀时，需要有空格与正文隔开
                continue
            
            content = content.strip()
            section = Section(
                label = next_label, 
                contents = [content] if content else [], 
                metadata = stack[idx][0].metadata
            )
            self.__append_section(stack[idx-1][0], section)
            #TODO 整理stack中待删除section的contents
            next(label_generator)
            stack[idx] = (section, label_generator)
            del stack[idx+1:]
            return True
        return False
        
    
    def __check_new_ordinal_indicator(self, line:str, stack:list[Tuple[Section, LabelGenerator]]) -> bool:
        r"""
        检查新的章节序列
        - 全新的序号
        - 越级子序号
            - [第一章] -> [第一章, 1.1]
            - #TODO 继承上一级的index？
                - [第二章] -> [第二章, 2.1]
        新的章节序列一定是处在stack[-1]章节中的
        """
        logger.info(f"check_new_ordinal_indicator: {line}")
        
        
        # 找到匹配到的最前面的【序号1】
        # 如果能匹配到多个序号序列，则只处理第一个，**这是默认了prefix和序号不会重合的假设**
        start = None
        ordinal_indicator = None
        for _ordinal_indicator in ORDINAL_INDICATOR_LIST:
            _indice = _ordinal_indicator[0]
            _start = line.find(_indice)
            if(_start == -1):
                continue
            if(start is None or _start < start):
                start = _start
                ordinal_indicator = _ordinal_indicator
        if(start is None):
            return False
        assert(ordinal_indicator is not None)
        
        prefix = line[:start]
        content = line[start+len(ordinal_indicator[0]):]
        
        # 以下获取prefix、suffix和content，格式见各函数文档
        if((_ := self.__check_brackets(prefix, content)) is not None):
            prefix, suffix, content = _
        else:
            if((prefix := self.__check_prefix(prefix)) is None):
                return False
            if((_ := self.__check_suffix(content)) is None):
                return False
            suffix, content = _
        
        # 越级子序号问题验证
            
        if(suffix in {"."} and not content.startswith(" ")):
            if((_ := self.__check_cascade_ordinal_indicator_unit(prefix + ordinal_indicator[0] + suffix, content)) is not None):
                metadata = stack[-1][0].metadata
                section = Section(
                    label = prefix + ordinal_indicator[0] + suffix, 
                    contents = [], 
                    metadata = metadata,
                )
                label_generator = LabelGenerator(ordinal_indicator, prefix, suffix)
                #TODO 整理stack[-1][0].contents
                stack.append((section, label_generator))
                for item in _: # [prefix, ordinal_indicator, suffix, content]
                    section = Section(
                        label = item[0] + item[1][0] + item[2],
                        contents = [item[3]] if item[3] else [],
                        metadata = metadata,
                    )
                    label_generator = LabelGenerator(
                        ordinal_indicator = item[1],
                        prefix = item[0],
                        suffix = item[2],
                    )
                    self.__append_section(stack[-1][0], section)
                    stack.append((section, label_generator))
                return True
        
        content = content.strip()
        section = Section(
            label = prefix + ordinal_indicator[0] + suffix, 
            contents = [content] if content else [], 
            metadata = stack[-1][0].metadata,
        )
        label_generator = LabelGenerator(ordinal_indicator, prefix, suffix)
        #TODO 整理stack[-1][0].contents
        self.__append_section(stack[-1][0], section)
        stack.append((section, label_generator))
        return True
    
    def __check_cascade_ordinal_indicator_unit(self, prefix:str, content:str) -> list|None:
        r"""
        prefix以"."结尾，且content不以" "开头，则需要检查级联序号
        TODO returns:
        """
        logger.info(f"check_exist_cascade_ordinal_indicator: {content}")
        # logger.debug(f"{prefix}")
        
        for ordinal_indicator in ORDINAL_INDICATOR_LIST:
            if(content.startswith(ordinal_indicator[0])):
                content = content[len(ordinal_indicator[0]):]
                if((_ := self.__check_suffix(content)) is None):
                    return None
                suffix, content = _
                # res = [(prefix, indices_list, suffix, content.strip())]
                if(suffix in {"."} and not not content.startswith(" ")):
                    _ = self.__check_cascade_ordinal_indicator_unit(prefix + ordinal_indicator[0] + suffix, content)
                    if(_ is not None):
                        return [(prefix, ordinal_indicator, suffix, "")] + _
                return [(prefix, ordinal_indicator, suffix, content.strip())]
        return None
    
    def __check_brackets(self, prefix:str, content:str) -> tuple[str, str, str]|None:
        r"""
        returns:
        - prefix: 不包含左空格，包含右空格，空值设为空字符串
        - suffix: 包含左空格，不包含右空格，空值设为空格
        - content: 去除两侧空格
        """
        prefix = prefix.lstrip()
        _prefix = prefix.rstrip()
        _content = content.lstrip()
        num_spaces = len(content) - len(_content)
        for open_bracket, close_bracket in BRACKETS_LIST:
            if(_prefix == open_bracket and _content.startswith(close_bracket)):
                return prefix, " " * num_spaces + close_bracket, _content[len(close_bracket):].strip()
        return None
    
    def __check_prefix(self, prefix:str) -> str|None:
        r"""
        returns:
        - prefix: 不包含左空格，包含右空格，空值设为空字符串
        """
        prefix = prefix.lstrip()
        _prefix = prefix.rstrip()
        if(_prefix != "" and _prefix not in PREFIX_LIST):
            return None
        return prefix
    
    def __check_suffix(self, content:str) -> tuple[str, str]|None:
        r"""
        returns:
        - suffix: 包含左空格，不包含右空格，空值设为空字符串
        - content: 去除两侧空格
        """
        _content = content.lstrip()
        num_spaces = len(content) - len(_content)
        for _suffix in SUFFIX_LIST:
            if(_content.startswith(_suffix)):
                return " " * num_spaces + _suffix, _content[len(_suffix):].strip()
        if(num_spaces > 0):
            return "", _content
        return None
    
    
    def __split_text(self, s:str) -> list[str]:
        r"""
        断句规则：
            - 句号、句号后的引号判断
            - 分号？？
        """
        # logger.debug(s)
        if("\n" in s):
            logger.warning("split_text: 输入文本包含换行符，可能导致结果不准确")
        # assert("\n" not in s)
        
        # Unicode符号
        s = REGEX_SPACE_CHARS.sub(" ", s) # 将空格字符一律替换为普通空格
        
        # 常见噪音
        s = re.sub(r"(江|苏|省|人|民|政|府|公|报)\1{2,}", "", s)    # 删除连续三个及以上的特定汉字
        s = re.sub(r"江江苏苏省省人人民民政政府府公公报报", "", s)
        
        # 断句规则        
        s = re.sub(r'([;；!?。！？\?])([^"”’」』])', r"\1\n\2", s)   # 句号
        s = re.sub(r'(\.{6})([^"’”」』])', r"\1\n\2", s)        # 英文省略号
        s = re.sub(r'(\…{2})([^"’”」』])', r"\1\n\2", s)        # 中文省略号
        s = re.sub(r'([;；!?。！？\?]["’”」』])([^;；!?，。！？\?])', r'\1\n\2', s)    # 句号后面跟着引号
        s = re.sub(r'(\.{6}["’”」』])([^;；!?，。！？\?])', r'\1\n\2', s)              # 句号后面跟着引号
        s = re.sub(r'(\…{2}["’”」』])([^;；!?，。！？\?])', r'\1\n\2', s)              # 句号后面跟着引号
        lines = s.split("\n")
        
        
        # logger.debug(f"{lines}")
        return lines
    