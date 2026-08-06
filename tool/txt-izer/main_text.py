"""
txt-izer 程序入口（诊断增强版）。

负责初始化服务、加载配置和语言包，并启动用户界面。
加入详细诊断日志，便于排查路径、配置和语言包加载问题。
"""

import sys
import json
from pathlib import Path

from src.services.config_service import load_config
from src.services.language_service import load_language
from .ui import run_interactive


def main() -> None:
    # 路径约定（相对于项目根目录，即 main.py 所在目录）
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / "config" / "config.json"

    print(f"[DIAG] 项目根目录: {base_dir}")
    print(f"[DIAG] 配置文件路径: {config_path}")

    # 1. 加载配置
    try:
        config = load_config(config_path)
        print("[DIAG] 配置文件加载成功。")
    except Exception as e:
        print(f"[ERROR] 加载配置文件失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 替换 {ROOT} 占位符
    config = {
        key: value.replace("{ROOT}", str(base_dir)) if isinstance(value, str) else value
        for key, value in config.items()
    }
    print("[DIAG] 占位符替换完成。")

    # 2. 确定 locales_dir（更安全的方式）
    raw_locales = config.get('locales_dir', '').strip()  # 去除首尾空格
    if raw_locales:
        # 如果配置里写了路径，就使用它（可能是相对或绝对）
        locales_dir = Path(raw_locales)
        print(f"[DIAG] 从配置文件读取 locales_dir: {locales_dir}")
        # 如果路径是相对路径，相对于当前工作目录，但我们可以根据情况调整为绝对路径
        if not locales_dir.is_absolute():
            # 尝试相对于 base_dir 解析
            locales_dir = base_dir / locales_dir
            print(f"[DIAG] 转为相对于项目根目录: {locales_dir}")
    else:
        # 配置里没有，或为空，使用默认路径
        locales_dir = base_dir / "config" / "locales"
        print(f"[DIAG] 使用默认 locales_dir: {locales_dir}")

    # 确保 locales_dir 存在，如果不存在则尝试创建
    if not locales_dir.exists():
        try:
            locales_dir.mkdir(parents=True, exist_ok=True)
            print(f"[DIAG] 创建了缺失的 locales 目录: {locales_dir}")
        except Exception as e:
            print(f"[ERROR] 无法创建 locales 目录: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"[DIAG] locales 目录已存在: {locales_dir}")

    # 3. 确定语言代码
    lang_code = config.get("language", "nya")
    print(f"[DIAG] 语言代码: {lang_code}")

    # 4. 加载语言包（增加详细错误信息）
    try:
        lang = load_language(lang_code, locales_dir)
        print("[DIAG] 语言包加载成功。")
    except FileNotFoundError as e:
        print(f"[ERROR] 语言文件不存在: {e}", file=sys.stderr)
        # 打印当前目录下的文件列表，便于排查
        print(f"[DIAG] 当前 locales_dir 下的文件: {list(locales_dir.glob('*.json'))}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[ERROR] 语言文件 JSON 格式错误: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"[ERROR] 语言参数无效: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] 加载语言包时发生未知错误: {e}", file=sys.stderr)
        sys.exit(1)

    # 5. 启动交互界面
    print("[DIAG] 启动 CLI 交互界面...")
    run_interactive(lang, config)


if __name__ == "__main__":
    main()