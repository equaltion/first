"""
服务层：合并任务编排。

负责文件 I/O、错误处理、进度通知与原子写入。
所有用户可见文本通过 lang 字典获取，不硬编码任何字符串。
不包含任何业务算法（算法由 core.merger 提供），
也不包含任何用户交互（交互由 ui 负责）。
"""

import os
import tempfile
from pathlib import Path
from typing import List, Dict, Optional, Callable

from src.core import merge_contents
from src.utils import safe_format
from src.models import MergeResult, SourceContent


def _read_file_content(filepath: Path, encodings=('utf-8', 'gbk', 'latin-1')) -> str:
    """
    尝试用多种编码读取文件内容。
    全部失败时返回空字符串并抛出异常（由调用者捕获）。
    """
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    # 所有编码都失败，最后用 errors='replace' 强制读取
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()


def merge_files(
    file_list: List[str],
    output_path: Path,
    lang: Dict[str, str],
    header_template: Optional[str] = None,
    separator: str = "\n\n",
    on_progress: Optional[Callable[[int, int, str], None]] = None
) -> MergeResult:
    """
    读取文件列表，合并内容，原子写入输出文件。

    Args:
        file_list: 源文件路径列表。
        output_path: 合并后的输出文件路径。
        lang: 语言包字典，用于生成用户可见的错误/提示信息。
              必需键：
                - "error.read_file":  读取失败时的消息模板，支持 {filepath} 和 {error}
                - "error.write_file": 写入失败时的消息模板，支持 {path} 和 {error}
                - "error.placeholder": 当文件读取失败时，插入输出中的占位文本模板，支持 {filepath} 和 {error}

        header_template: 自定义文件头部模板，默认使用分隔线。
        separator: 文件内容之间的分隔符。
        on_progress: 进度回调 (current_index, total, filepath) -> None

    Returns:
        dict:
            - success (bool): 是否成功生成输出文件。
            - output (str): 成功时返回输出文件路径。
            - errors (list[str]): 每个读取失败文件的错误描述。
    """
    # 默认头部模板
    if header_template is None:
        header_template = "\n" + "="*60 + "\n{source}\n" + "="*60 + "\n"

    errors = []
    total = len(file_list)

    def source_generator():
        for idx, filepath in enumerate(file_list, start=1):
            if on_progress:
                # 进度通知
                on_progress(idx, total, filepath)

            try:
                content = _read_file_content(Path(filepath))
                yield SourceContent(source=filepath, content=content)
            except Exception as e:
                error_msg = safe_format(lang,"error.read_file", filepath=filepath, error=e)
                errors.append(error_msg)
                placeholder = safe_format(lang,"error.placeholder", filepath=filepath, error=e)
                # 生成一个占位内容，保证输出中仍保留文件标识
                yield SourceContent(source=filepath, content=placeholder)

    # 调用纯合并逻辑
    merged_text, _ = merge_contents(
        sources=source_generator(),
        header_template=header_template,
        separator=separator
    )

    # 原子写入
    output_dir =Path (os.path.dirname(output_path) or '.')
    temp_name = None
    try:
        
        output_dir.mkdir(parents=True, exist_ok=True)
        # 使用临时文件（与目标文件在同一目录，确保同一文件系统）
        with tempfile.NamedTemporaryFile(
            mode='w',
            encoding='utf-8',
            dir=output_dir,
            delete=False,
            suffix='.tmp'
        ) as tmp:
            tmp.write(merged_text)
            temp_name = tmp.name
        os.replace(temp_name, output_path)
    except Exception as e:
        error_msg = safe_format(lang,"error.write_file", path=output_path, error=e)
        # 清理可能残留的临时文件
        errors.append(error_msg)
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)
        return MergeResult(success=False, errors=errors)

    return MergeResult(
        success=True,
        output_path=Path(output_path),
        errors=errors
    )