#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        data_logger_group.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      定义“表征`数据记录器组`的类”。
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2024/10/31     revise
# ------------------------------------------------------------------
# 导包 ==============================================================
from typing import Union, Optional

from .file_info import FileInfo
from .data_logger import DataLogger
from .data_logger_file import DataLoggerFile
from .specimen import Specimen

# 声明 ==============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defining a class that represents `data logger group`.
"""

__all__ = [
    "DataLoggerGroup",
]


# 定义 ==============================================================
class DataLoggerGroup(object):
    """
    类`DataLoggerGroup`表征"数据记录器组"。
    """

    def __init__(self, group_name: str):
        """
        类`CreMechDataAnalysisResultGroup`的初始化方法。

        :param group_name: 结果组的名称。
        """
        self.__group_name = group_name
        self.__results = {}

    @property
    def group_name(self) -> str:
        """
        返回结果组的名称。

        :return: 结果组的名称。
        """
        return self.__group_name

    # -----------------------------------------------------
    @property
    def results(self):
        """
        返回分析结果。
        """
        return self.__results

    # -----------------------------------------------------
    def add_from_datalyzer(self, datalzyer: Specimen):
        """
        从恒（常）应变速率力学数据分析器添加分析结果。

        :param datalzyer:恒（常）应变速率力学数据分析器。
        """
        self.__results[datalzyer.sample_name] = datalzyer.data_logger.to_dataframe()

    def add_from_datalogger(self, datalogger: DataLogger):
        """
        从恒（常）应变速率力学数据分析器的数据记录器添加分析结果。

        :param datalogger: 恒（常）应变速率力学数据分析器的数据记录器。
        """
        self.__results[datalogger.get("sample_name")] = datalogger.to_dataframe()

    def add_from_file(
        self, file: Union[str, FileInfo], encoding: Optional[str] = None, **kwargs
    ):
        """
        从文件中读取分析结果。
        """
        dlf = DataLoggerFile(file, encoding)
        self.add_from_datalogger(dlf.read(**kwargs))
