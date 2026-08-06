"""
命令实现模块：将所有 CLI 命令分支封装为命令类。

每个命令负责：
- 解析参数
- 调用服务层（通过 context 提供的接口）
- 返回 CommandResult（包含已翻译的消息、退出标志、语言包更新）
"""

import json
from pathlib import Path
from typing import List
from src.services.language_service import load_language
from src.services.merge_service import merge_files
from src.utils import safe_format
from src.models import CommandResult
from .base import Command


class ExitCommand(Command):
    name = "exit"
    aliases = ["quit"]

    def execute(self, args: str, context) -> CommandResult:
        msg = safe_format(context.lang, "goodbye")
        return CommandResult(messages=[msg], exit_requested=True)


class MergeCommand(Command):
    name = "merge"
    aliases = ["m"]

    def execute(self, args: str, context) -> CommandResult:
        if context.is_empty():
            return CommandResult(messages=[safe_format(context.lang, "list_empty")])

        output_dir = context.config.get("output_dir", ".")
        output_filename = context.config.get("output_filename", "merged.txt")
        output_path = Path(output_dir) / output_filename

        msgs = [safe_format(context.lang, "merging")]

        result = merge_files(
            file_list=context.get_files(),
            output_path=output_path,
            lang=context.lang,
            on_progress=lambda cur, total, f: msgs.append(f"  [{cur}/{total}] {f}")
        )

        if result.success:
            msgs.append(safe_format(context.lang, "merge_success", output=result.output_path))
        else:
            msgs.append(safe_format(context.lang, "merge_failed"))

        if result.errors:
            msgs.append(safe_format(context.lang, "merge_errors"))
            msgs.extend(result.errors)

        return CommandResult(messages=msgs)


class ListCommand(Command):
    name = "list"
    aliases = ["ls"]

    def execute(self, args: str, context) -> CommandResult:
        files = context.get_files()
        if not files:
            return CommandResult(messages=[safe_format(context.lang, "list_empty")])

        msgs = [safe_format(context.lang, "list_header")]
        for i, f in enumerate(files, 1):
            msgs.append(f"  {i}. {f}")
        return CommandResult(messages=msgs)


class HelpCommand(Command):
    name = "help"
    aliases = ["h", "?"]

    def execute(self, args: str, context) -> CommandResult:
        return CommandResult(messages=[safe_format(context.lang, "help_text")])


class ClearCommand(Command):
    name = "clear"
    aliases = ["cls"]

    def execute(self, args: str, context) -> CommandResult:
        context.clear_files()
        return CommandResult(messages=[safe_format(context.lang, "list_cleared")])


class RemoveCommand(Command):
    name = "remove"
    aliases = ["rm"]

    def execute(self, args: str, context) -> CommandResult:
        target = args.strip()
        if not target:
            return CommandResult(messages=[safe_format(context.lang, "invalid_index")])

        # 按编号删除
        if target.isdigit():
            idx = int(target) - 1
            files = context.get_files()
            if 0 <= idx < len(files):
                removed = files[idx]
                context.remove_file(idx)
                return CommandResult(messages=[safe_format(context.lang, "file_removed", file=removed)])
            else:
                return CommandResult(messages=[safe_format(context.lang, "invalid_index")])

        # 按路径删除
        if target in context.get_files():
            context.remove_file_by_path(target)
            return CommandResult(messages=[safe_format(context.lang, "file_removed", file=target)])
        else:
            return CommandResult(messages=[safe_format(context.lang, "file_not_in_list", file=target)])


class LangCommand(Command):
    name = "lang"
    aliases = ["language"]

    def execute(self, args: str, context) -> CommandResult:
        lang_code = args.strip()
        if not lang_code:
            return CommandResult(messages=[safe_format(context.lang, "error.language.empty")])

        base_dir = Path(__file__).resolve().parent
        locales_dir = Path(context.config.get("locales_dir",'') or base_dir/'config'/'locales')
        lang_file = locales_dir / f"{lang_code}.json"

        try:
            new_lang = load_language(lang_code=lang_code, locales_dir=locales_dir)
        except FileNotFoundError as e:
            return CommandResult(messages=[
                safe_format(context.lang, "error.language.file_not_found", lang_file=str(lang_file)),
                str(e)
            ])
        except json.JSONDecodeError as e:
            return CommandResult(messages=[
                safe_format(context.lang, "error.language.json_decode", lang_file=str(lang_file)),
                str(e)
            ])
        except ValueError as e:
            return CommandResult(messages=[
                safe_format(context.lang, "error.language.empty"),
                str(e)
            ])

        # 更新语言包
        context.lang = new_lang
        return CommandResult(
            messages=[safe_format(new_lang, "language_switched", lang_code=lang_code)],
            lang_updated=new_lang
        )


class AddFileCommand(Command):
    """默认命令：将用户输入视为文件路径进行添加。"""
    name = "__add_file__"  # 不作为显式命令匹配，由调度器兜底
    aliases = []

    def execute(self, args: str, context) -> CommandResult:
        path_input = args.strip()

        # 去掉可能的首尾引号
        if len(path_input) >= 2 and path_input[0] == path_input[-1] and path_input[0] in ('"', "'"):
            path_input = path_input[1:-1]

        if path_input in context.get_files():
            return CommandResult(messages=[safe_format(context.lang, "file_exists", file=path_input)])
        else:
            context.add_file(path_input)
            return CommandResult(messages=[safe_format(context.lang, "file_added", file=path_input)])

commands:list =[ExitCommand, MergeCommand, ListCommand,
    HelpCommand, ClearCommand, RemoveCommand,
    LangCommand, AddFileCommand]