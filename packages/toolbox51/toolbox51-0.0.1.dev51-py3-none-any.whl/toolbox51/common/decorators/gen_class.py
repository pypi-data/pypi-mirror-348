import functools
from typing import Generator, TypeVar, Callable, Generic, Optional, Any

T = TypeVar("T")

class GeneratorClass(Generic[T]):
    def __init__(self, gen_func: Callable[..., Generator[T, None, Any]], info: Optional[dict] = None, *args, **kwargs):
        self.gen_func = gen_func
        self.args = args
        self.kwargs = kwargs
        self.gen: Optional[Generator[T, None, Any]] = None  # 生成器实例
        self.info: dict[str, Any] = info if info is not None else {}  # 额外信息

    def __iter__(self) -> "GeneratorClass[T]":
        self.gen = self.gen_func(*self.args, **self.kwargs)
        return self

    def __next__(self) -> T:
        if self.gen is None:
            raise RuntimeError("迭代器未初始化，请使用 iter()")
        try:
            return next(self.gen)
        except StopIteration as e:
            self.info["return"] = e.value  # 存储 return 的返回值
            raise

    def send(self, value: Any) -> T:
        """允许向生成器发送值"""
        if self.gen is None:
            raise RuntimeError("迭代器未初始化，请使用 iter()")
        try:
            return self.gen.send(value)
        except StopIteration as e:
            self.info["return"] = e.value
            raise RuntimeError("生成器已结束，无法继续 send")

def gen_class(info=None):
    def decorator(gen_func: Callable[..., Generator[T, None, Any]]) -> Callable[..., "GeneratorClass[T]"]:
        @functools.wraps(gen_func)
        def wrapper(*args, **kwargs) -> "GeneratorClass[T]":
            return GeneratorClass(gen_func, info, *args, **kwargs)
        return wrapper
    return decorator

if __name__ == '__main__':
    
    @gen_class(info={"progress": 0, "status": "running"})
    def my_generator(n: int) -> Generator[int, None, str]:
        for i in range(n):
            received = yield i  # 接收 send 传入的值
            print(f"收到的 send 值: {received}")
        return "迭代结束"

    gen_instance = my_generator(3)

    print("初始 info:", gen_instance.info)

    print(next(gen_instance))  # 0
    print(gen_instance.send(100))  # send(100) 传值

    print(next(gen_instance))  # 1
    print(gen_instance.send(200))  # send(200) 传值

    try:
        print(next(gen_instance))  # 2
        print(next(gen_instance))  # 这里会抛出 StopIteration
    except StopIteration as e:
        print("生成器返回值:", e.value)
        gen_instance.info["return_value"] = e.value  # 也可以从 info 里取值

    print("最终 info:", gen_instance.info)
