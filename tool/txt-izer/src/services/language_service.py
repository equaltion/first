"""
服务层：语言包加载。

根据语言代码加载对应的 JSON 文件，返回文本字典。
不包含任何用户交互，所有错误通过异常向上层报告。
"""

import json
from pathlib import Path
from typing import Dict


def load_language(lang_code: str, locales_dir: Path) -> Dict[str, str]:
    """
    加载指定语言的语言包 JSON 文件，返回键值对字典。

    Args:
        lang_code: 语言代码，如 'zh' 或 'en'。
        locales_dir: 语言包存放目录的路径，例如 'config/locales'。

    Returns:
        解析后的语言字典，所有值均为字符串。

    Raises:
        FileNotFoundError: 语言文件不存在。
        json.JSONDecodeError: JSON 文件格式错误。
        ValueError: lang_code 或 locales_dir 为空字符串。
    """
    if not lang_code or not locales_dir:
        raise ValueError("Language code and locales directory cannot be empty.")

    lang_file:Path= locales_dir/ f"{lang_code}.json"

    # 检查文件是否存在，若不存在则给出清晰错误
    if not lang_file.is_file():
        raise FileNotFoundError(f"Locale file not found: {lang_file}")

    try:
        with open(lang_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON in locale file: {lang_file}", e.doc, e.pos
        ) from e

    # 确保所有值均为字符串（非字符串值转换为字符串）
    return {key: str(value) for key, value in data.items()}