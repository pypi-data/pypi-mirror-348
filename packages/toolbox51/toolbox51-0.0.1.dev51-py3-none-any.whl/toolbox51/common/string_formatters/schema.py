__all__ = ["str_fmt_type"]

from typing import Any, Callable, Annotated

str_fmt_type = Annotated[Callable[[Any], str], "id为大于0的整数"]