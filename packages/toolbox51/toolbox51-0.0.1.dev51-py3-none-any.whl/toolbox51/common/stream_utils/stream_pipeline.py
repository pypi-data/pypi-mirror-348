


from typing import TypeVar, Callable, AsyncIterator, AsyncGenerator, Awaitable

from ..singleton import SingletonMeta
from ..utils import NotGiven, NOT_GIVEN

T_in = TypeVar("T_in")
T_out = TypeVar("T_out")
T_end = TypeVar("T_end")

class InvalidDataDetected:
    def __bool__(self):
        return False
INVALID_DATA_DETECTED = InvalidDataDetected()


class AsyncStreamPipeline(metaclass=SingletonMeta):
    INVALID_DATA_DETECTED: InvalidDataDetected = INVALID_DATA_DETECTED
    
    async def __call__(
        self,
        stream: AsyncIterator[T_in],
        *,
        async_transform_func: Callable[[T_in], Awaitable[T_out]]|NotGiven = NOT_GIVEN, 
        transform_func: Callable[[T_in], T_out]|NotGiven = NOT_GIVEN,
        invalid_tail: AsyncIterator[T_out]|NotGiven = NOT_GIVEN,
        end_signal: T_end|NotGiven = NOT_GIVEN,
    ) -> AsyncGenerator[T_out|T_end|InvalidDataDetected, None]:
        """
        实时转发并检查`stream`，然后转换类型后转发
        - 优先使用`async_transform_func`转换数据，如果为`None`则使用`transform_func`
            - 遇到不合法数据时，请抛出`ValueError`
            - 日志请自行打印
            - 本函数仅处理`ValueError`，请在外部处理其他异常
        - 遇到不合法数据时，固定返回`InvalidDataDetected`，并停止转发
        - 若定义了`invalid_tail`，则返回`InvalidDataDetected`后，转发`invalid_tail`
        """
        if isinstance(async_transform_func, NotGiven):
            if isinstance(transform_func, NotGiven):
                raise ValueError("Either async_transform_func or transform_func should be given.")
            async def _(item: T_in) -> T_out:
                return transform_func(item)
            func = _
        else:
            func = async_transform_func
        async for item in stream:
            try:
                yield await func(item)
            except ValueError:
                yield self.INVALID_DATA_DETECTED
                if not isinstance(invalid_tail, NotGiven):
                    async for tail_item in invalid_tail:
                        yield tail_item
                return
        if not isinstance(end_signal, NotGiven):
            yield end_signal
        return

astream_pipeline = AsyncStreamPipeline()