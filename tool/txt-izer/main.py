"""
txt-izer 程序入口。

负责初始化服务、加载配置和语言包，并启动用户界面。
不包含任何交互逻辑（交互由 ui 层处理）。
"""

import sys
import json
from pathlib import Path

from src import load_config,load_language
from ui import run_interactive


def main() -> None:
    # 路径约定（相对于项目根目录，即 main.py 所在目录）
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / "config" / "config.json"


    # 1. 加载配置
    try:
        config = load_config(config_path)
    except (FileNotFoundError, ValueError, Exception) as e:
        # 除 JSON 解析错误外，load_config 会创建默认文件，一般不会失败，
        # 但为防御意外情况（如无权限），统一捕获并退出。
        print(f"Failed to load config: {e}", file=sys.stderr)
        sys.exit(1)

    config = {
    key: value.replace("{ROOT}", str(base_dir)) if isinstance(value, str) else value
    for key, value in config.items()
    }


    locales_dir = Path(config.get('locales_dir','')) or base_dir / "config" / "locales"
    # 2. 确定语言代码（优先从配置读取，否则默认中文）
    lang_code = config.get("language", "nya")

    # 3. 加载语言包
    try:
        lang = load_language(lang_code, locales_dir)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Failed to load language pack: {e}", file=sys.stderr)
        sys.exit(1)

    # 4. 根据命令行参数启动对应模式（未来可扩展 GUI / Web 等）
    # 当前仅支持默认交互模式（无参数或任意参数暂不区分）
    run_interactive(lang, config)


if __name__ == "__main__":
    main()
