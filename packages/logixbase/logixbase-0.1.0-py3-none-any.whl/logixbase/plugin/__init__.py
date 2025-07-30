# 版本信息
__version__ = "0.1.0"

# plugin模块，提供插件管理功能
from .base import BasePlugin
from .manager import PluginManager
from .log_monitor import LogMonitorPlugin
from .progress import ProgressPlugin

__all__ = [
    'BasePlugin',
    'PluginManager',
    'LogMonitorPlugin',
    'ProgressPlugin'
]