"""
此模块封装了命令行日志输出和交互功能，使用rich库提供丰富的文本显示效果。

console: rich.console.Console 对象，用于输出日志和消息。
logger: rich.logging.Logger 对象，用于记录日志。
StageAdapter: 日志适配器类，用于在日志消息中添加阶段信息。
"""

from .command_line_interface import console, logger, StageAdapter

__all__ = ['console', 'logger', 'StageAdapter']
