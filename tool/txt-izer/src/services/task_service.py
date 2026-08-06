"""
任务服务：管理应用会话状态（文件列表、语言包、配置），
提供给命令对象作为上下文使用。
"""

from typing import List, Dict
from pathlib import Path
from src.services import merge_files

class TaskService:
    """命令上下文，持有并管理运行时状态。"""

    def __init__(self, lang: Dict[str, str], config: Dict):
        self.lang = lang          # 可读写，用于语言切换
        self.config = config      # 只读配置
        self._file_list: List[str] = []

    # ── 文件列表管理 ──

    def add_file(self, path: str) -> None:
        """添加文件路径，若已存在则忽略。"""
        if path not in self._file_list:
            self._file_list.append(path)

    def remove_file(self, index: int) -> None:
        """按索引移除文件，索引无效则无操作。"""
        if 0 <= index < len(self._file_list):
            self._file_list.pop(index)

    def remove_file_by_path(self, path: str) -> None:
        """按路径移除文件。"""
        if path in self._file_list:
            self._file_list.remove(path)

    def clear_files(self) -> None:
        self._file_list.clear()

    def get_files(self) -> List[str]:
        return list(self._file_list)

    def is_empty(self) -> bool:
        return len(self._file_list) == 0
    # 在 TaskService 类中添加
    def merge(self, on_progress=None):
        output_dir = self.config.get("output_dir", ".")
        output_filename = self.config.get("output_filename", "merged.txt")
        output_path = Path(output_dir) / output_filename

        return merge_files(
            file_list=self._file_list,
            output_path=output_path,
            lang=self.lang,
            on_progress=on_progress
        )