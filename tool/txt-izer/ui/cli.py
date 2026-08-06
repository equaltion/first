"""
命令行交互界面。

提供交互式循环，负责收集用户输入、调用服务层并显示结果。
所有用户可见文本从语言包获取，不包含任何硬编码字符串。
"""
import json
from pathlib import Path
from typing import Dict, Any, List
from src.services.merge_service import merge_files
from src.services.language_service import load_language
from src.utils import safe_format

def run_interactive(lang: Dict[str, str], config: Dict[str, Any]) -> None:
    """
    启动交互式命令行界面。

    Args:
        lang: 语言包字典，所有界面文本均从中获取。
        config: 配置字典，需包含 'output_dir' 和 'output_filename'。
    """
    # 显示欢迎语
    print(safe_format(lang,"welcome"))

    # 构造输出路径
    output_dir = Path(config.get("output_dir", "."))
    output_filename = config.get("output_filename", "merged.txt")
    output_path = output_dir / output_filename

    file_list: List[str] = []

    while True:
        try:
            user_input = input(safe_format(lang,"prompt")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print(safe_format(lang,"goodbye"))
            break

        if user_input.lower() == "merge":
            if not file_list:
                print(safe_format(lang,"list_empty" ))
                continue

            print(safe_format(lang,"merging"))
            result = merge_files(
                file_list=file_list,
                output_path=output_path,
                lang=lang,
                on_progress=lambda cur, total, f: print(
                    f"  [{cur}/{total}] {f}"
                )
            )

            if result.success:
                print(safe_format(lang, "merge_success",output=result.output_path))
            else:
                print(safe_format(lang,"merge_failed"))

            if result.errors:
                print(safe_format(lang,"merge_errors"))
                for e in result.errors:
                    print(f"  - {e}")
            continue

        if user_input.lower() == "list":
            if not file_list:
                print(safe_format(lang,"list_empty"))
            else:
                print(safe_format(lang,"list_header"))
                for i, f in enumerate(file_list, 1):
                    print(f"  {i}. {f}")
            continue

        if user_input.lower() == "help":
            print(safe_format(lang,"help_text"))
            continue

        if user_input.lower() == "clear":
            file_list.clear()
            print(safe_format(lang,"list_cleared"))
            continue

        if user_input.lower().startswith("remove "):
            # 支持按编号或路径删除
            target = user_input[7:].strip()
            if target.isdigit():
                idx = int(target) - 1
                if 0 <= idx < len(file_list):
                    removed = file_list.pop(idx)
                    print(safe_format(lang,"file_removed",file=removed))
                else:
                    print(safe_format(lang,"invalid_index"))
            else:
                if target in file_list:
                    file_list.remove(target)
                    print(safe_format(lang,"file_removed",file=target))
                else:
                    print(safe_format(lang,"file_not_in_list",file=target))
            continue

        if user_input.lower().startswith("lang "):
            # 支持更改设置的语言
            lang_code =user_input[5:].strip()
            locales_dir:Path=(config['locales_dir'])
            lang_file:Path= locales_dir/ f"{lang_code}.json"
            try: 
                temp_lang=load_language(
                    lang_code=lang_code,
                    locales_dir=locales_dir
                )
            except FileNotFoundError as e:
                print(safe_format(lang,"error.language.empty"),e,sep='/n')
            except json.JSONDecodeError as e:
                print(safe_format(lang,"error.language.file_not_found",lang_file=lang_file),e,sep='/n')
            except ValueError as e:
                print(safe_format(lang, "error.language.json_decode",lang_file=lang_file),e,sep='/n')
            else:
                print(safe_format(lang,"language_switched",lang_code=lang_code))
                lang =temp_lang
                print(safe_format(lang,"language_switched",lang_code=lang_code))

        # 默认当作文件路径处理
        path = Path(user_input)
        # 不进行文件校验，仅简单处理用户输入
        # 支持用引号括起来的路径？这里按原始输入添加
        if user_input.startswith(('"',"'")) and user_input.endswith(('"',"'")):
            user_input = user_input[1:-1]  # 去掉引号

        if user_input in file_list:
            print(safe_format(lang,"file_exists",file=user_input))
        else:
            file_list.append(user_input)
            print(safe_format(lang,"file_added",file=user_input))

