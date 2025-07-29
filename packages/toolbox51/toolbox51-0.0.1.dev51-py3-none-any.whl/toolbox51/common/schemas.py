# ruff: noqa: F401 - imported but unused
# ruff: noqa: E402 - module level import not at top of file

__all__ = ["id_uint"]

from typing import Annotated

id_uint = Annotated[int, "id为大于0的整数"]


from .string_processors import str_fmt_type