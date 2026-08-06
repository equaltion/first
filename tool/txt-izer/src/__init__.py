# src/__init__.py

# 1. 显式暴露核心函数（给外部用）
from .core import merge_contents

# 2. 显式暴露服务层函数（给外部用）
from .services import (
    merge_files,
    load_config,
    save_config,
    load_language,
    TaskService,
    CommandDispatcher
)

# 3. 显式暴露工具函数
from .utils import safe_format

# 4. 显式暴露数据模型
from .models import SourceContent, MergeResult,CommandResult
