"""
纯业务逻辑：文件内容合并与分隔。

本模块不执行任何文件 I/O(不调用 open / os.path 等)。
所有内容由调用方传入，合并结果通过返回值给出。
"""

from typing import Iterator, Tuple, Optional, List
from src.models import SourceContent



def merge_contents(
    sources: Iterator[SourceContent],
    header_template: str = "====================\n{source}\n====================\n",
    separator: str = "\n\n"
) -> Tuple[str, List[str]]:
    """
    将多个来源的内容合并为单一字符串。

    Args:
        sources: SourceContent 对象的迭代器，每个对象包含来源标识和内容。
        header_template: 头部模板，用 {source} 格式化来源标识。
        separator: 不同来源内容之间的分隔符（放在头部之后，内容之前）。

    Returns:
        (merged_text, errors):
            merged_text: 合并后的完整文本。
            errors: 处理过程中遇到的错误信息列表（预留，当前仅作占位）。
    """
    parts = []
    errors = []

    for item in sources:
        # 即使来源为空字符串，也生成头部，保持输出完整
        header = header_template.format(source=item.source)
        parts.append(header + item.content)

    merged = separator.join(parts)
    return merged, errors