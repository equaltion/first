"""命令调度器：注册命令并根据用户输入分派执行。"""

from typing import Dict, Optional
from src.models import CommandResult
from src.services.command.base import Command


class CommandDispatcher:
    """管理命令注册表，并将用户输入分派到对应命令。"""

    def __init__(self):
        self._commands: Dict[str, Command] = {}
        self._default_command: Optional[Command] = None

    def register(self, command: Command) -> None:
        """注册一个命令及其所有别名。"""
        self._commands[command.name] = command
        for alias in command.aliases:
            self._commands[alias] = command

    def set_default(self, command: Command) -> None:
        """设置当输入不匹配任何命令时使用的默认命令。"""
        self._default_command = command

    def dispatch(self, user_input: str, context) -> CommandResult:
        """
        解析用户输入并执行对应命令。

        Args:
            user_input: 用户输入的原始字符串。
            context: 应用上下文(TaskService 实例）。

        Returns:
            CommandResult 对象。
        """
        if not user_input.strip():
            return CommandResult(messages=[])

        parts = user_input.split(maxsplit=1)
        name = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        command = self._commands.get(name)
        if command:
            return command.execute(args, context)
        elif self._default_command:
            # 默认命令将整个用户输入作为参数（因为可能是文件路径）
            return self._default_command.execute(user_input, context)
        else:
            return CommandResult(messages=[f"Unknown command: {name}"])