#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        file_info.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      定义“文件信息”相关的函数和类。
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2025/05/04     finish
# ------------------------------------------------------------------
# 导包 ==============================================================
import os
import sys
import inspect
from typing import Optional
from pathlib import Path

# chardet库需要安装：
# pip install chardet
import chardet

# 声明 ==============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defining functions and classes associated with `file information`.
"""

__all__ = [
    'encoding_of',
    'FileInfo',
    'info_of',
    'module_info_of',
]

# 定义 ==============================================================

# 用于编码检测的文件读取大小
__READ_SIZE__ = 10240

# 哈希计算乘子，常用质数用于减少碰撞
__HASH_MULTIPLIER__ = 31


# noinspection PyBroadException
def encoding_of(file: str) -> Optional[str]:
    """
    利用chardet库获取文件的编码。

    :param file: 文件的完整路径。
    :type: str
    :return: 文件的编码。注意：任何失败都将返回None。
    :rtype: Optional[str]
    """
    file = Path(file)
    if file.is_file():
        try:
            with open(file, 'rb') as f:
                raw_data = f.read(4)
                if raw_data.startswith(b'\xFF\xFE'):
                    return 'UTF-16'
                elif raw_data.startswith(b'\xFE\xFF'):
                    return 'UTF-16BE'
                elif raw_data.startswith(b'\xEF\xBB\xBF'):
                    return 'UTF-8'
                else:
                    raw_data += f.read(__READ_SIZE__ - 4)
                    result = chardet.detect(raw_data)
                    return result['encoding']
        except Exception:
            return None
    else:
        return None


class FileInfo(object):
    """
    类`FileInfo`用于承载“文件信息”。
    """

    def __init__(self, directory_path: str,
                 base_name: str,
                 ext_name: Optional[str] = None,
                 encoding: Optional[str] = None,
                 **kwargs):
        """
        类`FileInfo`的初始化方法。

        :param directory_path: 文件所在的目录路径。
        :param base_name: 文件基名。
        :param ext_name: 文件扩展名（不含`.`），
                        如果包含`.`，在内部将其删除，缺省为None。
        :param encoding: 文件编码，缺省为None。
        :param kwargs: 有关文件的其他信息，将被转化为对象属性。
        """
        self.__directory_path = directory_path
        self.__base_name = base_name
        self.__ext_name = ext_name

        # 如果文件扩展名包含点，则将点删除。
        if self.__ext_name.startswith('.'):
            self.__ext_name = self.__ext_name[1:]

        # 构建文件名。
        if ext_name is not None:
            self.__full_name = "{}.{}".format(
                self.__base_name,
                self.__ext_name)
        else:
            self.__full_name = self.__base_name

        # 构建文件的路径。
        self.__full_path = os.path.join(self.__directory_path,
                                        self.__full_name)

        # 尝试获取文件的编码。
        self.__encoding = encoding
        if self.__encoding is None:
            self.__encoding = encoding_of(self.__full_path)

        # 其他关键字参数被转换为对象的属性。
        for key in kwargs.keys():
            if not hasattr(self, key):
                setattr(self, key, kwargs[key])

    @property
    def directory_path(self) -> str:
        """
        获取文件所在目录的路径。

        :return: 文件所在目录的路径。
        """
        return self.__directory_path

    @property
    def base_name(self) -> str:
        """
        获取文件基名。

        :return: 文件基名。
        """
        return self.__base_name

    @property
    def ext_name(self) -> Optional[str]:
        """
        获取文件扩展名（不含`.`）。

        :return: 文件扩展名（不含`.`）。
        """
        return self.__ext_name

    @property
    def full_name(self) -> str:
        """
        获取文件名。

        :return: 文件名。
        """
        return self.__full_name

    @property
    def full_path(self) -> str:
        """
        获取文件的路径。

        :return: 文件的路径。
        """
        return self.__full_path

    @property
    def encoding(self) -> Optional[str]:
        """
        获取文件编码。

        :return: 文件编码。
        """
        return self.__encoding

    @encoding.setter
    def encoding(self, new_encoding: str):
        """
        设置文件编码。

        :param new_encoding: 新的文件编码。
        :return: None
        """
        self.__encoding = new_encoding

    def make_directory(self):
        """
        创建文件目录

        :return: None
        """
        if not os.path.exists(self.directory_path):
            os.makedirs(self.directory_path, exist_ok=True)

    # noinspection PyUnusedLocal
    def make_file(self):
        """
        创建文件。

        :return: None
        """
        self.make_directory()
        if not os.path.exists(self.full_path):
            with open(self.full_path, "w") as f:
                pass

    # noinspection PyBroadException
    def __eq__(self, other):
        """
        重载`==`操作符，支持与另一个FileInfo对象或表示路径的字符串进行比较。

        :param other: 另一个FileInfo对象或字符串形式的路径。
        :return: 相等返回True，否则返回False。
        """
        if isinstance(other, str):
            try:
                other = info_of(other)
            except Exception:
                # 如果info_of失败，认为无法比较
                return False

        if isinstance(other, FileInfo):
            if self.full_path == other.full_path:
                return True
            return False
        else:
            return False

    def __ne__(self, other):
        """
        重载`!=`操作符。

        :param other: 另一个FileInfo对象或字符串形式的路径。
        :return: 不相等返回True，否则返回False。
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        获取对象的hash码。

        :return: 对象的hash码。
        """
        result: int = 1
        for arg in (self.directory_path, self.base_name, self.ext_name):
            result = __HASH_MULTIPLIER__ * result + (0 if arg is None else hash(arg))
        return result

    def __str__(self):
        """
        获取对象字符串。

        :return:对象字符串。
        """
        return self.full_path

    def __repr__(self):
        """
        获取对象的文本式。

        :return:对象的文本式。
        """
        res_dict = dict()
        for key in self.__dict__:
            if key.startswith("_FileInfo__"):
                res_dict[key.removeprefix("_FileInfo__")] = self.__dict__[key]
            else:
                res_dict[key] = self.__dict__[key]
        return "FileInfo{}".format(res_dict)


def info_of(file: str,
            encoding: Optional[str] = None,
            **kwargs) -> FileInfo:
    """
    获取文件信息对象。

    :param file: 文件的完整路径。
    :param encoding: 文件编码，缺省为None。
    :param kwargs: 有关文件的其他信息，将被转化为对象属性。
    :return: FileInfo对象。
    """
    directory_path, file_name = os.path.split(file)
    base_name, ext_name = os.path.splitext(file_name)
    return FileInfo(directory_path, base_name, ext_name,
                    encoding, **kwargs)


def module_info_of(module: str) -> FileInfo:
    """
    利用inspect获取指定模块名的文件信息。

    :param module: 指定的模块名。
    :return: FileInfo对象。
    """
    file_path = inspect.getfile(sys.modules[module])
    return info_of(file_path)
