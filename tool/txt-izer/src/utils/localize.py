"""本地化辅助函数：安全地从语言包获取格式化文本。"""

from typing import Dict,Optional


def safe_format(lang: Dict[str, str], key: str, **kwargs) -> str:
    """
    从语言包获取指定 key 的模板，并用 kwargs 进行格式化。
    若 key 缺失或格式化参数不匹配，返回包含诊断信息的占位文本。
    
    Args:
        lang: 语言包字典。
        key: 目标键。
        **kwargs: 模板所需参数。

    Returns:
        格式化后的字符串，或缺失/错误提示。
    """
    template :Optional[str]= lang.get(key)
    if template is None:
        return f"[Missing locale key: '{key}']"
    try:
        return template.format(**kwargs)
    except (KeyError, IndexError) as e:
        return f"[Format error for locale key '{key}': {e}]"