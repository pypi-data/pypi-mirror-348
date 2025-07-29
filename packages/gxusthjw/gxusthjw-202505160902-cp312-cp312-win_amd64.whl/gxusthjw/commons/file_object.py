#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        file_object.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      定义“表征`文件对象`”的类。
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2025/05/02     finish
# ------------------------------------------------------------------
# 导包 ==============================================================
import os
from typing import Optional, Union

from .file_info import (encoding_of, FileInfo)

# 声明 ==============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defining a class that represents `file object`.
"""

__all__ = [
    'FileObject'
]

# 定义 ==============================================================


# 哈希计算乘子，常用质数用于减少碰撞
__HASH_MULTIPLIER__ = 31


class FileObject(object):
    """
    类`FileObject`表征“文件对象”。
    """

    def __init__(self, file: Union[str, FileInfo],
                 encoding: Optional[str] = None,
                 **kwargs):
        """
        类`FileObject`的初始化方法。

        :param file: 文件的完整路径或文件信息（FileInfo）对象。
        :param encoding: 文件编码。
        :param kwargs: 其他可选关键字参数，这些参数全部转化为对象的属性。
        """
        if isinstance(file, str):
            self.__file_full_path = file.strip()
            # 分离文件的路径、文件名和文件扩展名。
            (self.__file_directory_path, self.__file_full_name) = \
                os.path.split(self.__file_full_path)
            (self.__file_base_name, self.__file_ext_name) = \
                os.path.splitext(self.__file_full_name)
            self.__file_ext_name = self.__file_ext_name.strip()
            # 如果文件扩展名包含点，则将点删除。
            if self.__file_ext_name.startswith('.'):
                self.__file_ext_name = self.__file_ext_name[1:]
            # 尝试获取文件的编码。
            self.__encoding = encoding
            if self.__encoding is None:
                self.__encoding = encoding_of(self.__file_full_path)
        else:
            self.__file_full_path = file.full_path
            self.__file_directory_path = file.directory_path
            self.__file_full_name = file.full_name
            self.__file_base_name = file.base_name
            self.__file_ext_name = file.ext_name
            for key in file.__dict__:
                if not key.startswith("_FileInfo__"):
                    if not hasattr(self, key):
                        setattr(self, key, file.__dict__[key])
            # 尝试获取文件的编码。
            self.__encoding = encoding
            if self.__encoding is None:
                self.__encoding = file.encoding

        # 其他关键字参数被转换为对象的属性。
        for key in kwargs.keys():
            if not hasattr(self, key):
                setattr(self, key, kwargs[key])

    @property
    def file_full_path(self) -> str:
        """
        获取文件的完整路径。

        :return: 文件的完整路径。
        """
        return self.__file_full_path

    @property
    def file_directory_path(self) -> str:
        """
        获取文件所在目录的完整路径。

        :return: 文件所在目录的完整路径。
        """
        return self.__file_directory_path

    @property
    def file_full_name(self) -> str:
        """
        获取文件的完整文件名（包含扩展名）。

        :return: 文件的完整文件名（包含扩展名）。
        """
        return self.__file_full_name

    @property
    def file_base_name(self) -> str:
        """
        获取文件的基文件名（不包含扩展名）。

        :return: 文件的基文件名（不包含扩展名）。
        """
        return self.__file_base_name

    @property
    def file_ext_name(self) -> str:
        """
        获取文件的扩展名（不包含‘.’）。

        :return: 文件的扩展名（不包含‘.’）。
        """
        return self.__file_ext_name

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

    def to_file_info(self) -> FileInfo:
        """
        将其文件对象转换为文件信息对象。

        :return: 文件信息对象。
        """
        return FileInfo(self.file_directory_path, self.file_base_name, self.file_ext_name)

    def make_directory(self):
        """
        创建文件目录

        :return: None
        """
        if not os.path.exists(self.file_directory_path):
            os.makedirs(self.file_directory_path, exist_ok=True)

    def make_file(self):
        """
        创建文件。

        :return: None
        """
        self.make_directory()
        if not os.path.exists(self.file_full_path):
            open(self.file_full_path, "w").close()

    # noinspection PyBroadException
    def __eq__(self, other):
        """
        重载`==`操作符，支持与另一个FileObject对象或表示路径的字符串进行比较。

        :param other: 另一个FileObject对象或字符串形式的路径。
        :return: 相等返回True，否则返回False。
        """
        if isinstance(other, str):
            try:
                other = file_object_of(other)
            except Exception:
                return False

        if isinstance(other, FileObject):
            if self.file_full_path == other.file_full_path:
                return True
            return False
        else:
            return False

    def __ne__(self, other):
        """
        重载`!=`操作符。

        :param other: 另一个FileObject对象。
        :return: 不相等返回True，否则返回False。
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        获取对象的hash码。

        :return: 对象的hash码。
        """
        result: int = 1
        for arg in (self.file_directory_path, self.file_base_name, self.file_ext_name):
            result = __HASH_MULTIPLIER__ * result + (0 if arg is None else hash(arg))

        return result

    def __str__(self):
        """
        获取对象字符串。

        :return:对象字符串。
        """
        return self.file_full_path

    def __repr__(self):
        """
        获取对象的文本式。

        :return:对象的文本式。
        """
        res_dict = dict()
        for key in self.__dict__:
            if key.startswith("_FileObject__"):
                res_dict[key.removeprefix("_FileObject__")] = self.__dict__[key]
            else:
                res_dict[key] = self.__dict__[key]
        return "FileObject{}".format(res_dict)


def file_object_of(file: Union[str, FileInfo],
                   encoding: Optional[str] = None,
                   **kwargs) -> FileObject:
    """
    获取文件对象。

    :param file: 文件的完整路径。
    :param encoding: 文件编码，缺省为None。
    :param kwargs: 有关文件的其他信息，将被转化为对象属性。
    :return: FileObject对象。
    """
    return FileObject(file, encoding, **kwargs)
