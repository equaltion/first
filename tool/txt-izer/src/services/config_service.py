"""
服务层：配置文件管理。

负责应用配置的读取、写入、默认值与重置。
不包含任何用户交互（无 print/input)仅使用标准库 json 和 pathlib。
"""

import json
from pathlib import Path
from typing import Any, Dict


def get_default_config() -> Dict[str, Any]:
    """
    返回应用的默认配置字典。

    Returns:
        包含默认扩展名列表、输出目录和输出文件名的字典。
    """
    return {
        "extensions": [".txt", ".md", ".cpp", ".h", ".py", ".json"],
        "output_dir": "{ROOT}",
        "output_filename": "merged.txt",
        "locales_dir":"{ROOT}/config/locales"
    }


def load_config(config_path: Path) -> Dict[str, Any]:
    """
    加载 JSON 配置文件。如果文件不存在，则创建默认配置并写入，然后返回。

    Args:
        config_path: 配置文件路径(通常为 config/config.json)。

    Returns:
        配置字典。

    Raises:
        json.JSONDecodeError: 文件存在但内容不是有效的 JSON。
    """
    if config_path.is_file():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            # 格式错误直接向上抛出，由调用者决定如何处理
            raise
        return data
    else:
        # 文件不存在，创建默认配置并写入
        default_config = get_default_config()
        save_config(config_path, default_config)
        return default_config


def save_config(config_path: Path, config: Dict[str, Any]) -> None:
    """
    将配置字典写入指定的 JSON 文件。

    Args:
        config_path: 配置文件路径。
        config: 待保存的配置字典。
    """
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def reset_config(config_path: Path) -> None:
    """
    将配置文件重置为默认配置（覆盖现有文件）。

    Args:
        config_path: 配置文件路径。
    """
    default_config = get_default_config()
    save_config(config_path, default_config)