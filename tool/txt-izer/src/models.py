"""核心数据类，业务层与服务层共享"""

from dataclasses import dataclass, field
from typing import List,Optional,Dict
from pathlib import Path

@dataclass
class SourceContent:
    """待合并的内容项"""
    source: str      # 来源标识（如文件路径）
    content: str     # 文本内容

@dataclass
class MergeResult:
    """合并操作的返回结果"""
    success: bool
    output_path: Path=Path('.')
    errors: List[str] = field(default_factory=list)

@dataclass
class CommandResult:
    messages: List[str]     # 要显示给用户的文本（多行）
    exit_requested: bool = False
    lang_updated: Optional[Dict[str, str]] = None  # 若语言包被切换，返回新包