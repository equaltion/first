"""
命令模式基类

定义所有命令必须实现的接口。每个命令对应一个用户操作（如合并、添加文件），
由 CommandDispatcher 根据用户输入进行匹配和调度。
"""

from abc import ABC, abstractmethod
from typing import Any, List
from src.models import CommandResult


class Command(ABC):
    """
    命令抽象基类。

    子类必须定义以下类属性：
        name: 命令的主要名称（如 "merge"），用于匹配用户输入。
        aliases: 命令的别名列表（如 ["m", "mg"]），可选。
        help_key: 语言包中帮助文本的键名（如 "help.merge"），可选。

    子类必须实现：
        execute(args: str, context: Any) -> CommandResult
            args: 命令后的参数字符串（可能为空）。
            context: 应用上下文，提供对语言包、配置、文件列表等状态的访问。
                     通常为 TaskService 实例，具体接口见 TaskService 文档。
    """

    name: str = ""
    aliases: List[str] = []
    help_key: str = ""

    @abstractmethod
    def execute(self, args: str, context: Any) -> CommandResult:
        """
        执行命令。

        Args:
            args: 除去命令名后的剩余输入字符串，可能为空。
            context: 应用上下文对象，应提供以下方法/属性：
                - lang: 当前语言包字典（可读写）
                - config: 配置字典
                - is_empty() -> bool
                - add_file(path: str) -> str (返回操作状态键)
                - remove_file(index: int) -> str
                - remove_file_by_path(path: str) -> str
                - clear_files()
                - get_files() -> List[str]
                - merge() -> MergeResult
                - process (可选的文本命令处理入口，但通常命令不调用此方法以免递归)

        Returns:
            CommandResult 对象，包含显示消息列表、退出标志、语言包更新等信息。
        """
        ...