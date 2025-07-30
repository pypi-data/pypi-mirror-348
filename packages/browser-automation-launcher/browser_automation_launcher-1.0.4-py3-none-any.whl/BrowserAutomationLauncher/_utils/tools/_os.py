"""
Copyright (c) 2025-now Martian Bugs All rights reserved.
Build Date: 2025-05-19
Author: Martian Bugs
Description: 系统工具类, 例如文件操作、路径操作等
"""

from os import path, remove


class OsTools:
    @staticmethod
    def file_remove(file_path: str):
        """
        删除文件

        Args:
            file_path: 文件路径
        Returns:
            是否删除成功, 如果文件不存在或不是文件, 则返回False
        """

        if not path.exists(file_path) or not path.isfile(file_path):
            return False

        remove(file_path)
        return True
