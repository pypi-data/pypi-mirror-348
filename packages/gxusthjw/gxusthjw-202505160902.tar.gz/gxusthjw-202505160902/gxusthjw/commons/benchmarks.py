#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        benchmarks.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      定义基准测试相关的函数和类。
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2025/05/10     revise
# ------------------------------------------------------------------
# 导包 ==============================================================
from typing import Callable, Any
import numpy as np
import timeit

# 声明 ==============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defines the functions and classes related to benchmarking.
"""

__all__ = [
    'benchmark_func',
]


# 定义 ==============================================================

# noinspection PyBroadException
def benchmark_func(func: Callable[..., Any],
                   repeat: int, *args, **kwargs):
    """
    对给定函数执行性能基准测试，返回平均执行时间（单位：秒）

    :param func: 要测试的函数。
    :param repeat: 执行次数。
    :param args: func 的位置参数。
    :param kwargs: 可选关键字参数，其中，
                   1. 'use_np_errstate'用于支持控制 NumPy 错误状态；
                   2. 'use_try'用于指示是否采用try语句截收函数执行的异常。
                   3. 其余关键字参数全部传给func，作为func 的关键字参数。
    :return: 平均单次执行时间（秒）。
    """
    use_np_errstate: bool = kwargs.pop('use_np_errstate', False)
    use_try: bool = kwargs.pop('use_try', False)

    def wrapper():
        if use_np_errstate:
            with np.errstate(all='ignore'):
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    if use_try:
        try:
            duration = timeit.timeit(wrapper, number=repeat)
            return duration / repeat
        except Exception:
            return float('inf')  # 返回无穷大表示无效结果
    else:
        duration = timeit.timeit(wrapper, number=repeat)
        return duration / repeat
