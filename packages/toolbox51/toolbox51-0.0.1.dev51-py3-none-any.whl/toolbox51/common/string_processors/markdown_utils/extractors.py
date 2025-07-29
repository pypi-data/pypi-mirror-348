"""从markdown中提取目标数据的方法集合"""


import re
import json



def code_blocks(text: str, language: str = '') -> list[str]:
    """提取指定代码块"""
    pattern = f"```{language}(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    return [match.strip() for match in matches]

def code_block(text: str, language: str = '') -> str|None:
    """提取第一个代码块"""
    pattern = f"```{language}(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return None


def json_blocks(text: str) -> list[dict|list|None]:
    """提取JSON代码块并解析成字典或列表"""
    pattern = r'```json(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    results = []
    for match in matches:
        try:
            results.append(json.loads(match.strip()))
        except json.JSONDecodeError:
            results.append(None)
    return results

def json_block(text: str) -> dict|list|None:
    """提取第一个JSON代码块并解析成字典或列表"""
    pattern = r'```json(.*?)```'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            return None
    else:
        return None

    
