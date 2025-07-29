


import inspect

def inspect_stack_check(keywords: list[str]):
    for frame in inspect.stack():
        for keyword in keywords:
            if keyword in frame.filename:
                return True
    return False