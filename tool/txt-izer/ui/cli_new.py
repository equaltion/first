"""
命令行交互界面。

提供交互式循环，负责收集用户输入、调用服务层并显示结果。
所有用户可见文本从语言包获取，不包含任何硬编码字符串。
"""
import json
from pathlib import Path
from typing import Dict, Any, List
from src import merge_files, load_language, safe_format,TaskService,CommandDispatcher
from src.services.command.commands import (
    ExitCommand, MergeCommand, ListCommand,
    HelpCommand, ClearCommand, RemoveCommand,
    LangCommand, AddFileCommand
)
def run_interactive(lang: Dict[str, str], config: Dict[str, Any]) -> None:
    """
    启动交互式命令行界面。

    Args:
        lang: 语言包字典，所有界面文本均从中获取。
        config: 配置字典，需包含 'output_dir' 和 'output_filename'。
    """
        # 初始化服务
    context = TaskService(lang, config)

    # 初始化调度器并注册命令
    dispatcher = CommandDispatcher()
    dispatcher.register(ExitCommand())
    dispatcher.register(MergeCommand())
    dispatcher.register(ListCommand())
    dispatcher.register(HelpCommand())
    dispatcher.register(ClearCommand())
    dispatcher.register(RemoveCommand())
    dispatcher.register(LangCommand())
    dispatcher.set_default(AddFileCommand())  # 默认当作添加文件

    # 显示欢迎语
    print(safe_format(lang, "welcome"))

    # 主循环
    while True:
        try:
            user_input = input(safe_format(lang, "prompt")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        result = dispatcher.dispatch(user_input, context)

        for msg in result.messages:
            print(msg)

        if result.lang_updated:
            lang = result.lang_updated
        if result.exit_requested:
            break