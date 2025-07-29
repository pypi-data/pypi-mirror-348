#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        typings.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      定义“类型标注”相关的类和函数。
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2025/05/02     finish
# ------------------------------------------------------------------
# 导包 =============================================================
from typing import (Union, TypeVar, List, Tuple)
from collections.abc import (Iterable, Sequence)

import numpy as np
import numpy.typing as npt

# 声明 =============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defining functions and classes for `type annotations`.
"""

__all__ = [
    'Number',
    'is_number',
    'NumberArrayLike',
    'is_number_array_like',
    'NumberSequence',
    'is_number_sequence',
    'Numbers',
    'is_numbers',
    'Numeric',
    'is_numeric',
    'NumberNDArray',
    'is_number_ndarray',
    'is_number_1darray',
]

# 定义 ===============================================================
Number = TypeVar('Number', int, float, np.number)
"""
表示数值类型的类型变量。
该类型变量所标注的变量可以是整数（int）、
浮点数（float）或np.number 类型。
"""


def is_number(value: Number) -> bool:
    """
    判断指定值是否为数值类型。

    :param value: 要判断的值，可以是整数（int）、
                  浮点数（float）或np.number 类型。
    :return: 如果指定的值是数值，返回 True；否则返回 False。
    """
    return isinstance(value, (int, float, np.number))


NumberArrayLike = Union[
    List[Union[int, float]],
    Tuple[Union[int, float], ...],
    npt.NDArray[np.number]
]
"""
表示数值型类数组的类型。

该类型可以是以下几种之一：
    - 包含整数或浮点数的列表（List[Union[int, float]]）
    - 包含整数或浮点数的元组（Tuple[Union[int, float], ...]）
    - 包含数值类型元素的 NumPy 数组（npt.NDArray[np.number]）
"""


def is_number_array_like(data: NumberArrayLike) -> bool:
    """
    检查给定的数据是否为 NumberArrayLike 类型。

    :param data: 要检查的数据，可以是以下几种之一：
                 - 包含整数或浮点数的列表（List[Union[int, float]]）
                 - 包含整数或浮点数的元组（Tuple[Union[int, float], ...]）
                 - 包含数值类型元素的 NumPy 数组（npt.NDArray[np.number]）
    :return: 如果数据是 NumberArrayLike 类型则返回 True，否则返回 False。
    """
    if isinstance(data, (list, tuple)):
        # 检查列表或元组中的所有元素是否都是 int 或 float
        return all(is_number(item) for item in data)
    elif isinstance(data, np.ndarray):
        # 检查 NumPy 数组是否只包含数值类型的元素
        return issubclass(data.dtype.type, np.number)
    else:
        # 数据既不是 list/tuple 也不是 np.ndarray
        return False


NumberSequence = Union[
    Sequence[Number],
    npt.NDArray[np.number]
]
"""
表示数值型序列的类型。

该类型可以是以下几种之一：
    - 包含整数或浮点数的序列（Sequence[Number]）
    - 包含数值类型元素的 NumPy 数组（npt.NDArray[np.number]）
"""


def is_number_sequence(data: NumberSequence) -> bool:
    """
    检查给定的数据是否为 NumberSequence 类型。

    :param data: 要检查的数据，可以是以下几种之一：
                 - 包含整数或浮点数的序列（Sequence[Number]）
                 - 包含数值类型元素的 NumPy 数组（npt.NDArray[np.number]）
    :return: 如果数据是 NumberSequence 类型则返回 True，否则返回 False。
    """
    if isinstance(data, np.ndarray):
        return issubclass(data.dtype.type, np.number)
    if isinstance(data, Sequence):
        return all(is_number(item) for item in data)
    return False


Numbers = Union[
    Iterable[Number],
    npt.NDArray[np.number]
]
"""
表示数值集的类型。

该类型可以是以下几种之一：
    - 包含整数或浮点数的可迭代对象（Iterable[Number]）
    - 包含数值类型元素的 NumPy 数组（npt.NDArray[np.number]）
"""


def is_numbers(data: Numbers) -> bool:
    """
    检查给定的数据是否为 Numbers 类型。

    :param data: 要检查的数据，可以是以下几种之一：
                 - 包含整数或浮点数的可迭代对象（Iterable[Number]）
                 - 包含数值类型元素的 NumPy 数组（npt.NDArray[np.number]）
    :return: 如果数据是 Numbers 类型则返回 True，否则返回 False。
    """
    if isinstance(data, np.ndarray):
        # 检查 NumPy 数组是否只包含数值类型的元素
        return issubclass(data.dtype.type, np.number)
    if hasattr(data, '__iter__'):
        # 检查可迭代对象中的所有元素是否都是数字
        try:
            return all(is_number(item) for item in data)
        except TypeError:
            # 如果迭代过程中出现类型错误，则认为不符合条件
            return False
    return False


Numeric = TypeVar('Numeric', int, float, np.number, npt.NDArray[np.number])
"""
表示数值类型的类型变量。

该类型变量可以是以下几种之一：
    - 整数（int）
    - 浮点数（float）
    - 包含数值类型元素的 NumPy 数组（npt.NDArray[np.number]）
"""


def is_numeric(data: Numeric) -> bool:
    """
    检查给定的数据是否为 Numeric 类型。

    :param data: 要检查的数据，可以是以下几种之一：
                 - 整数（int）
                 - 浮点数（float）
                 - 包含数值类型元素的 NumPy 数组（npt.NDArray[np.number]）
    :return: 如果数据是 Numeric 类型则返回 True，否则返回 False。
    """
    if isinstance(data, (int, float, np.number)):
        return True
    if isinstance(data, np.ndarray):
        # 检查 NumPy 数组是否只包含数值类型的元素
        return issubclass(data.dtype.type, np.number)
    return False


NumberNDArray = npt.NDArray[np.number]
"""
表示包含数值类型元素的 NumPy 数组类型。

该类型别名用于简化类型标注，适用于以下场景：
    - 函数参数或返回值类型为包含数值类型元素的 NumPy 数组时。
"""


def is_number_ndarray(data: NumberNDArray) -> bool:
    """
    检查给定的数据是否为 NumberNDArray 类型。

    :param data: 要检查的数据，必须是包含数值类型元素的 NumPy 数组。
    :return: 如果数据是 NumberNDArray 类型则返回 True，否则返回 False。
    """
    return isinstance(data, np.ndarray) and issubclass(data.dtype.type, np.number)


def is_number_1darray(data: NumberNDArray) -> bool:
    """
    检查给定的数据是否为一维 NumberNDArray 类型。

    :param data: 要检查的数据，必须是一维的 NumPy 数组，并且包含数值类型元素。
    :return: 如果数据是一维的 NumberNDArray 类型则返回 True，否则返回 False。
    """
    return isinstance(data, np.ndarray) and issubclass(data.dtype.type, np.number) and data.ndim == 1
