#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        specimen.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      定义“表征`样本`”的类。
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2024/10/17     revise
#       Jiwei Huang        0.0.1         2025/05/05     finish
# ----------------------------------------------------------------
# 导包 ============================================================
from .data_analyzer import DataAnalyzer

# 声明 ============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defining a class that represents `specimen`.
"""

__all__ = [
    'Specimen',
]


# 定义 =============================================================
class Specimen(DataAnalyzer):
    """
    抽象类`Specimen`表征“样本”。

        此类实质上是一个基类，所有承载样本数据的类均应继承自此类。

        所有承载样本数据的对象均拥有2个基本属性：

            1. 样本名（specimen_name）：str，通常指代某一个样本。

            2. 测试编号（specimen_no）：int，为了区分同一样本在重复测试时所得到的数据，特设置此编号。

        而样本名与测试编号可合并得到：

            1. 样品名称（sample_name）：str，样本名_测试编号。此样品名在概念上应具有唯一性。
    """

    def __init__(self, *args, **kwargs):
        """
        类`Specimen`的构造方法。

            用到的关键字参数如下：

                1. specimen_name：str，样本名，缺省值为：‘specimen’。

                2. specimen_no：int，测试编号，缺省值为：0。

                3. sample_name：str，样品名，格式为：样本名_测试编号。
                               如果指定了sample_name，
                               则其分拆值将覆盖specimen_name和specimen_no。

            其他未用到的关键字参数，同样将被全部转化为对象的属性。

        :param kwargs: 可选关键字参数。
        """
        # 样品名。
        if 'specimen_name' in kwargs:
            __specimen_name: str = kwargs.pop('specimen_name')
            if (__specimen_name is not None and
                    isinstance(__specimen_name, str) and
                    __specimen_name.strip()):
                self.__specimen_name: str = __specimen_name.strip()
            else:
                self.__specimen_name: str = 'specimen'
        else:
            self.__specimen_name: str = 'specimen'

        # 测试编号。
        if 'specimen_no' in kwargs:
            __specimen_no: int = kwargs.pop('specimen_no')
            if (__specimen_no is not None and
                    isinstance(__specimen_no, int) and
                    __specimen_no >= 0):
                self.__specimen_no: int = __specimen_no
            else:
                self.__specimen_no: int = 0
        else:
            self.__specimen_no: int = 0

        # 如果指定了sample_name，则其结果将覆盖`specimen_name`和`specimen_no`所指定的值。
        if 'sample_name' in kwargs:
            sample_name: str = kwargs.pop('sample_name')
            try:
                __name, __no = sample_name.split('_', 1)
                self.__specimen_name = __name.strip()
                self.__specimen_no = int(__no)
                if not self.__specimen_name:
                    self.__specimen_name = 'specimen'
                if self.__specimen_no < 0:
                    self.__specimen_no = 0
            except (ValueError, TypeError):
                # 使用默认值。
                self.__specimen_name = 'specimen'
                self.__specimen_no = 0

        super(Specimen, self).__init__(*args, **kwargs)
        self.data_logger.log(self.specimen_name, "SpecimenName")
        self.data_logger.log(self.specimen_no, "SpecimenNo")
        self.data_logger.log(self.sample_name, "SampleName")

    @property
    def specimen_name(self) -> str:
        """
        获取样本名。

        :return: 样本名。
        """
        return self.__specimen_name

    @specimen_name.setter
    def specimen_name(self, new_value: str):
        """
        设置样本名。

        :param new_value: 样本名。
        """
        if (not isinstance(new_value, str)) or (not new_value.strip()):
            raise ValueError("new_value must be a non-empty str.")
        self.__specimen_name = new_value
        self.data_logger.log(self.specimen_name, "SpecimenName")
        self.data_logger.log(self.sample_name, "SampleName")

    @property
    def specimen_no(self) -> int:
        """
        获取测试编号。

        :return: 测试编号。
        """
        return self.__specimen_no

    @specimen_no.setter
    def specimen_no(self, new_value: int):
        """
        设置测试编号。

        :param new_value: 测试编号。
        """
        if (not isinstance(new_value, int)) or (new_value < 0):
            raise ValueError("new_value must be a int number and greater than or equal to 0.")
        self.__specimen_no = new_value
        self.data_logger.log(self.specimen_no, "SpecimenNo")
        self.data_logger.log(self.sample_name, "SampleName")

    def set_sample_name(self, specimen_name: str, specimen_no: int = 0):
        """
        设置样品名称。

        :param specimen_name: 样本名。
        :param specimen_no: 测试编号。
        :return:
        """
        if (not isinstance(specimen_name, str)) or (not specimen_name.strip()):
            raise ValueError("specimen_name must be a non-empty str.")
        if (not isinstance(specimen_no, int)) or (specimen_no < 0):
            raise ValueError("specimen_no must be a int number and greater than or equal to 0.")
        self.__specimen_name = specimen_name
        self.__specimen_no = specimen_no
        self.data_logger.log(self.specimen_name, "SpecimenName")
        self.data_logger.log(self.specimen_no, "SpecimenNo")
        self.data_logger.log(self.sample_name, "SampleName")

    @property
    def sample_name(self) -> str:
        """
        获取样品名称。

        :return: 样品名称。
        """
        return "{}_{}".format(self.specimen_name, self.specimen_no)

    @sample_name.setter
    def sample_name(self, new_value: str):
        """
        设置样品名称。

        指定的参数`new_value`必须为以`_`为分隔符的字符串，
        且第2部分必须为数字。

        :param new_value: 样品名称（必须为以`_`为分隔符的字符串）。
        """
        try:
            name, no = new_value.split('_', 1)
            self.__specimen_name = name
            self.__specimen_no = int(no)
            if not self.__specimen_name.strip() or self.__specimen_no < 0:
                raise ValueError("specimen_name must be a non-empty str,"
                                 "specimen_no must be a int number and greater than or equal to 0.")
        except (ValueError, TypeError):
            raise ValueError("new_value can not convert to 'specimen_name' and 'specimen_no'.")
        self.data_logger.log(self.specimen_name, "SpecimenName")
        self.data_logger.log(self.specimen_no, "SpecimenNo")
        self.data_logger.log(self.sample_name, "SampleName")

# ===================================================================
