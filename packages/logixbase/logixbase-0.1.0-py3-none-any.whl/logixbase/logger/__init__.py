# 版本信息
__version__ = "0.1.0"

from .core import LogManager
from .decorator import auto_log

__all__ = ['LogManager', 'auto_log']