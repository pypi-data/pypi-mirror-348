#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        data_logger_file.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      定义“表征`数据记录器输出文件`的类”。
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2024/10/31     revise
# ------------------------------------------------------------------
# 导包 ==============================================================
from typing import Union, Optional

from . import DataLogger
from .file_object import FileObject
from .file_info import FileInfo
# 声明 ==============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defining a class that represents `data logger file`.
"""

__all__ = [
    "DataLoggerFile",
]


# 定义 ==============================================================
class DataLoggerFile(FileObject):
    """
    类`DataLoggerFile`表征“数据记录器输出文件”。
    """

    def __init__(
        self, file: Union[str, FileInfo], encoding: Optional[str] = None, **kwargs
    ):
        """
        类`DataLoggerFile`的初始化方法。

        :param file: 文件的路径或文件信息对象。
        :param encoding: 文件编码。
        :param kwargs: 其他可选关键字参数，这些参数全部转化为对象的属性。
        """
        super(DataLoggerFile, self).__init__(file, encoding, **kwargs)

    def read(self, file_type: str = None, **kwargs):
        """
        读取数据记录器文件的数据。

        :param file_type: 数据记录器文件的类型。
        :param kwargs: 读取数据所需的关键字参数。
        :return: 数据记录器对象。
        """
        data_logger = DataLogger()
        if file_type is None:
            file_type = self.file_ext_name
        if file_type == "csv":
            data_logger.from_dict(self.file_full_path, **kwargs)
        elif file_type == "xlsx" or file_type == "xls":
            data_logger.from_excel(self.file_full_path, **kwargs)
        elif file_type == "table" or file_type == "txt":
            data_logger.from_table(self.file_full_path, **kwargs)
        elif file_type == "json":
            data_logger.from_excel(self.file_full_path, **kwargs)
        elif file_type == "html":
            data_logger.from_html(self.file_full_path, **kwargs)
        else:
            raise ValueError("Unsupported file type: {}".format(file_type))
        return data_logger
