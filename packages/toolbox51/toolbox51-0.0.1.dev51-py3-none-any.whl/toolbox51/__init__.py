r"""
51's personal toolbox
"""


__version__ = "0.0.1.dev51"

__changelog__ = """\
## update history
- 0.0.1.dev51
    - [new] common.string_formatters.markdown_utils
    - [new] common.string_formatters.StrTmpl
    - [new] common.logging
    - [new] common.logger_manager
    - [new] common.context_managers.timer
    - [new] common.decorators.func_logger
    - [new] common.singleton
    - [new] common.stream_utils.stream_pipeline
"""

####################################
# ruff: noqa
from .common import * 