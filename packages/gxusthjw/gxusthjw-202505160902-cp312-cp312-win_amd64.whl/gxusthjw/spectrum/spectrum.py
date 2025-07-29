#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        spectrum.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      定义“表征`谱数据`”的类。
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2025/05/05     finish
# ------------------------------------------------------------------
# 导包 ==============================================================
import os
import math
from pathlib import Path
from typing import Optional, Dict, Tuple, Union

import numpy as np
import numpy.typing as npt
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from pybaselines import Baseline
from scipy.optimize import leastsq

from ..commons import DataTable
from ..commons import (is_sorted_descending,
                       is_sorted_ascending,
                       Ordering)
from ..findpeaks import ampd
from ..statistics import FittingStatistics
from ..zhxyao import deriv_quasi_sech

# 声明 ==============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defines a class that represents `spectrum`.
"""

__all__ = [
    'Spectrum',
]


# 定义 ==============================================================
class Spectrum(object):
    """
    类`Spectrum`表征“谱数据”。

        “谱数据”可包含3列数据，分别为：

            1. y：y坐标数据。

            2. x：x坐标数据。

            3. e：误差数据。

            其中，y坐标数据是必要的，而x坐标数据和误差数据（e）可以没有。

            1. 如果x坐标数据没有，则使用有序整数列（从0开始）代替。

            2. 如果误差数据没有，则使用None代替。

        参考fityk-manual，“谱数据”还包含了2列理论计算数据，分别为：

            1. s: 理论计算误差数据。

            2. w: 理论计算权重数据。
    """

    def __init__(self, y: npt.ArrayLike,
                 x: Optional[npt.ArrayLike] = None,
                 e: Optional[npt.ArrayLike] = None,
                 **kwargs):
        """
        类`Spectrum`的初始化方法。

        考虑到x坐标数据为可选的，故将y坐标数据作为第一个参数。

        在可选关键字参数kwargs中，本类用到的可选关键字参数为：

           1. sigma: 理论计算误差数据的计算方式。

               （1）如果sigma是数字（float或int），则将其填充至理论计算误差数据。

               （2）如果sigma是列表、元组或np.ndarray，则将其转换为np.ndarray，赋值给理论计算误差数据。

               （3）如果sigma是可调用对象（callable），则以y为参数，调用该可调用对象计算理论计算误差数据，
                  再将所得计算值填充至理论计算误差数据。

               （4）如果未指定sigma参数或sigma参数为None或sigma参数为忽略大小写的‘default’，
                  则根据y数据，计算 max(sqrt(abs(y)),1)值作为理论计算误差数据。

               （5）除上述四种情况外，其他参数值将抛出异常。

           2. weight: 理论计算权重数据的计算方式。

               （1）如果weight是数字（float或int），则将其填充至理论计算权重数据。

               （2）如果weight是列表、元组或np.ndarray，则将其转换为np.ndarray，赋值给理论计算权重数据。

               （3）如果weight是可调用对象（callable），则以e为参数（如果e为None,则以s为参数），
                   调用该可调用对象计算理论计算权重数据，所得计算值作为理论计算权重数据。

               （4）如果未指定weight参数或weight参数为None或weight参数为忽略大小写的‘default’，
                  则根据e数据，计算 1.0 / e**2 （如果e为None，则计算1.0 / s**2）值作为
                  理论计算权重数据。

               （5）除上述四种情况外，其他参数值将抛出异常。

        对于数据的保存规则：

            1. y坐标数据，将被保存为numpy.ndarray，数据元素类型为与所传入的y数据元素的类型一致。

            2. x坐标数据，将被保存为numpy.ndarray，数据元素类型为与所传入的x数据元素的类型一致或numpy.int32。

            3. 误差数据e，将被保存为None或numpy.ndarray，数据元素类型为与所传入的e数据元素的类型一致。

            4. 理论计算误差数据s，将被保存为numpy.ndarray，数据元素类型为与所传入的s数据元素的类型一致或numpy.float64。

            5. 理论计算权重数据w，将被保存为numpy.ndarray，数据元素类型为与所传入的w数据元素的类型一致或numpy.float64。

        :param y: array_like, y坐标数据。
        :param x: array_like, x坐标数据。
        :param e: array_like, 误差数据。
        :param kwargs: dict，可选关键字参数。
                       除sigma、weight、x、y、e、s、w外，
                       其它的关键字参数均被转换为对象的属性。
        """
        # 保存y坐标数据。
        self.__y = np.array(y, copy=True)

        # 保存数据的长度。
        self.__len = self.__y.shape[0]

        # 保存x坐标数据。
        if x is None:
            # 只有此情况下，x数据的dtype为np.int32。
            self.__x = np.arange(self.__len, dtype=np.int32)
        else:
            self.__x = np.array(x, copy=True)

        # 确保x与y数据的长度相同。
        if self.__len != self.__x.shape[0]:
            raise ValueError(
                "Expected the length of x and y is same, "
                "but got {{len(x) = {},len(y) = {}}}.".format(
                    self.__x.shape[0], self.__len)
            )

        # 判断x坐标数据的有序性。
        if is_sorted_ascending(self.__x):
            # 升序。
            self.__x_sorted_type = Ordering.ASCENDING
        elif is_sorted_descending(self.__x):
            # 降序。
            self.__x_sorted_type = Ordering.DESCENDING
        else:
            # 无序。
            self.__x_sorted_type = Ordering.UNORDERED

        # 保存误差数据。
        if e is not None:
            self.__e = np.array(e, copy=True)
            # 确保e与y数据的长度相同。
            if self.__len != self.__e.shape[0]:
                raise ValueError(
                    "Expected the length of e and y is same, "
                    "but got {{len(e) = {},len(y) = {}}}.".format(
                        self.__e.shape[0], self.__len
                    )
                )
        else:
            self.__e = None

        # 理论计算误差数据列，参考自：fityk—manual。
        if 'sigma' in kwargs:
            self.__sigma = kwargs['sigma']
            if isinstance(self.__sigma, (int, float)):
                self.__s = np.full_like(self.__y, self.__sigma)
            elif isinstance(self.__sigma, (list, tuple, np.ndarray)):
                self.__s = np.array(self.__sigma, copy=True)
            elif callable(self.__sigma):
                self.__s = np.array([self.__sigma(yi) for yi in self.__y],
                                    copy=True, dtype=np.float64)
            elif self.__sigma is None or (isinstance(self.__sigma, str) and
                                          self.__sigma.lower() == 'default'):
                self.__s = np.array([max(math.sqrt(abs(yi)), 1) for yi in self.__y],
                                    copy=True, dtype=np.float64)
            else:
                raise ValueError(
                    "Expected sigma is one of {{int, float, callable, "
                    "None, 'default'(case-Ignored)}}, "
                    "but got {} ({}) type.".format(type(self.__sigma),
                                                   self.__sigma))
        else:
            self.__sigma = None
            self.__s = np.array([max(math.sqrt(abs(yi)), 1) for yi in self.__y],
                                copy=True, dtype=np.float64)

        if self.__len != self.__s.shape[0]:
            raise ValueError(
                "Expected the length of s and y is same, "
                "but got {{len(s) = {},len(y) = {}}}.".format(
                    self.__s.shape[0], self.__len
                )
            )

        # 理论计算权重数据，参考自：fityk—manual。
        if self.__e is not None:
            __err = self.__e
        else:
            __err = self.__s

        if 'weight' in kwargs:
            self.__weight = kwargs['weight']
            if isinstance(self.__weight, (int, float)):
                self.__w = np.full_like(self.__y, self.__weight)
            elif isinstance(self.__weight, (list, tuple, np.ndarray)):
                self.__w = np.array(self.__weight, copy=True)
            elif callable(self.__weight):
                self.__w = np.array([self.__weight(err_i) for err_i in __err],
                                    copy=True, dtype=np.float64)
            elif self.__weight is None or (isinstance(self.__weight, str) and
                                           self.__weight.lower() == 'default'):
                self.__w = 1.0 / np.power(__err, 2.0)
            else:
                raise ValueError(
                    "Expected weight is one of {{int, float, callable, "
                    "None, 'default'(case-Ignored)}}, "
                    "but got {} ({}) type.".format(type(self.__weight),
                                                   self.__weight))
        else:
            self.__weight = None
            self.__w = 1.0 / np.power(__err, 2.0)

        # 用于保存计算过程数据。
        self.__data_capsule = DataTable(self.__x, self.__y, self.__e,
                                          self.__s, self.__w,
                                          item_names=('x', 'y', 'e', 's', 'w'))

        # 其他关键字参数将被转换为对象的属性。
        for key in kwargs.keys():
            if (hasattr(self, key) or "sigma".__eq__(key) or "weight".__eq__(key)
                    or "x".__eq__(key) or "y".__eq__(key) or "e".__eq__(key)
                    or "s".__eq__(key) or "w".__eq__(key)):
                continue
            else:
                setattr(self, key, kwargs[key])

        # 保存备用。
        self.__kwargs = kwargs

    @property
    def y(self) -> npt.NDArray:
        """
        获取y坐标数据。

        :return: y坐标数据。
        """
        return self.__y

    @property
    def x(self) -> npt.NDArray:
        """
        获取x坐标数据。

        :return: x坐标数据。
        """
        return self.__x

    @property
    def e(self) -> Optional[npt.NDArray]:
        """
        获取误差数据。

        :return: 误差数据。
        """
        return self.__e

    @property
    def s(self) -> npt.NDArray:
        """
        获取理论计算误差数据。

        :return: 理论计算误差数据。
        """
        return self.__s

    @property
    def w(self) -> npt.NDArray:
        """
        获取理论计算权重数据。

        :return: 理论计算权重数据。
        """
        return self.__w

    @property
    def len(self) -> int:
        """
        获取数据的长度。

        :return: 数据的长度。
        """
        return self.__len

    @property
    def kwargs(self) -> Dict:
        """
        获取其他可选关键字参数字典。

        :return: 其他可选关键字参数字典。
        """
        return self.__kwargs

    @property
    def sigma(self):
        """
        获取理论计算误差列的计算方式。

        :return: 理论计算误差列的计算方式。
        """
        return self.__sigma

    @property
    def weight(self):
        """
        获取理论计算权重列的计算方式。

        :return: 理论计算权重列的计算方式。
        """
        return self.__weight

    @property
    def x_sorted_type(self) -> Ordering:
        """
        获取x坐标数据的有序性，潜在的结果为：

           “ascending”，“descending”，“unordered”。

        :return: x坐标数据的有序性
        """
        return self.__x_sorted_type

    @property
    def data_capsule(self):
        """
        获取谱数据所包含的数据容器（数据囊）。

        :return:谱数据所包含的数据容器（数据囊）。
        """
        return self.__data_capsule

    @property
    def baseline_fitter(self):
        """
        获取基线拟合器。

        :return: 基线拟合器。
        """
        return Baseline(x_data=self.x)

    # -------------------------------------------------------------------------
    @property
    def x_start(self):
        """
        获取x坐标数据的第一个值。

        :return: x坐标数据的第一个值。
        """
        return self.x[0]

    @property
    def x_end(self):
        """
        获取x坐标数据的最后一个值。

        :return: x坐标数据的最后一个值。
        """
        return self.x[-1]

    @property
    def x_min(self):
        """
        获取x坐标数据的最小值。

        :return: x坐标数据的最小值。
        """
        return np.min(self.x)

    @property
    def x_max(self):
        """
        获取x坐标数据的最大值。

        :return: x坐标数据的最大值。
        """
        return np.max(self.x)

    @property
    def x_width(self):
        """
        获取x坐标数据的宽度。

        :return:x坐标数据的宽度。
        """
        return self.x_max - self.x_min

    @property
    def y_start(self):
        """
        获取y坐标数据的第一个值。

        :return: y坐标数据的第一个值。
        """
        return self.y[0]

    @property
    def y_end(self):
        """
        获取y坐标数据的最后一个值。

        :return: y坐标数据的最后一个值。
        """
        return self.y[-1]

    @property
    def y_min(self):
        """
        获取y坐标数据的最小值。

        :return: y坐标数据的最小值。
        """
        return np.min(self.y)

    @property
    def y_max(self):
        """
        获取y坐标数据的最大值。

        :return: y坐标数据的最大值。
        """
        return np.max(self.y)

    @property
    def y_height(self):
        """
        获取y坐标数据的高度。

        :return:y坐标数据的高度。
        """
        return self.y_max - self.y_min

    @property
    def y_mean(self):
        """
        获取y坐标数据的均值。

        :return:y坐标数据的均值。
        """
        return np.mean(self.y)

    @property
    def y_var0(self):
        """
        获取y坐标数据的总体方差。

        :return:y坐标数据的总体方差。
        """
        return np.var(self.y, ddof=0)

    @property
    def y_var1(self):
        """
        获取y坐标数据的样本方差。

        :return:y坐标数据的样本方差。
        """
        return np.var(self.y, ddof=1)

    @property
    def y_std0(self):
        """
        获取y坐标数据的总体均方差。

        :return:y坐标数据的总体均方差。
        """
        return np.std(self.y, ddof=0)

    @property
    def y_std1(self):
        """
        获取y坐标数据的样本均方差。

        :return:y坐标数据的样本均方差。
        """
        return np.std(self.y, ddof=1)

    @property
    def y_exp(self):
        """
        获取y坐标数据的exp值。

        :return: y坐标数据的exp值。
        """
        return np.exp(self.y)

    @property
    def y_log(self):
        """
        获取y坐标数据的log值。

        :return: y坐标数据的log值。
        """
        return np.log(self.y)

    @property
    def y_sqrt(self):
        """
        获取y坐标数据的sqrt值。

        :return: y坐标数据的sqrt值。
        """
        return np.sqrt(self.y)

    @property
    def y_square(self):
        """
        获取y坐标数据的square值。

        :return: y坐标数据的square值。
        """
        return np.square(self.y)

    # ================================================================

    def y_normalize(self, lower: Union[int, float] = 0,
                    upper: Union[int, float] = 1):
        """
        将y坐标数据归一化至指定的区间内。

        :param lower: 区间下限。
        :param upper: 区间上限。
        :return: 归一化的y坐标数据。
        """
        if upper <= lower:
            raise ValueError("Expected upper > lower, "
                             "but got {lower=%f,upper=%f}" % (lower, upper))

        k = (upper - lower) / self.y_height
        return lower + k * (self.y - self.y_min)

    @property
    def y_norm(self):
        """
        将y坐标数据归一化至[0,1]区间内。

        :return: 归一化的y坐标数据。
        """
        return self.y_normalize()

    @property
    def y_zscore0(self):
        """
        获取y坐标数据的Z-Score (总体)。

        :return:y坐标数据的Z-Score (总体)。
        """
        return (self.y - self.y_mean) / self.y_var0

    @property
    def y_zscore1(self):
        """
        获取y坐标数据的Z-Score (样本)。

        :return:y坐标数据的Z-Score (样本)。
        """
        return (self.y - self.y_mean) / self.y_var1

    # ================================================================
    def horizontal_shift(self, shift_amount: Union[int, float]):
        """
        谱数据横向移动。

        :param shift_amount:移动量。
        :return: 移动后的数据。
        """
        self.__x = self.__x + shift_amount
        self.__data_capsule.update(self.x, "x_shift_{}".format(shift_amount))
        return self.x

    def vertical__shift(self, shift_amount: Union[int, float]):
        """
        谱数据纵向移动。

        :param shift_amount:移动量。
        :return: 移动后的数据。
        """
        self.__y = self.__y + shift_amount
        self.__data_capsule.update(self.y, "y_shift_{}".format(shift_amount))
        return self.y

    # ================================================================

    def find_index_x(self, xi: Union[int, float]):
        """
        找到指定xi值在x中的索引。如果在x中没有找到与xi值相等值的索引，
        则返回以一个与xi值最接近值的索引，此时，存在3种情况：

        1. x为升序排列，则找到一个小于xi值的最大索引。

        2. x为降序排列，则找到一个大于xi值的最小索引。

        3. x为无序的，则找到所有与xi值相等的索引。

        :param xi: 指定的xi值。
        :return: 索引。
        """
        # 帮我优化以下代码
        if self.x_sorted_type == Ordering.ASCENDING:
            res_a = 0
            for i in range(self.len):
                if self.x[i] <= xi:
                    res_a = i
                else:
                    break
            return res_a
        elif self.x_sorted_type == Ordering.DESCENDING:
            res_d = 0
            for j in range(self.len):
                if self.x[j] >= xi:
                    res_d = j
                else:
                    break
            return res_d
        else:
            res_u = list()
            for k in range(self.len):
                if self.x[k] == xi:
                    res_u = k
                else:
                    break
            return res_u

    def find_index_xrange(self, xi: Union[int, float], xj: Union[int, float]):
        """
        找到指定xi和xj的索引。

        :param xi: 指定的xi。
        :param xj: 指定的xi。
        :return: xi的索引和xj索引组成的元组，其中小者在前，大者在后。
        """
        xi_index = self.find_index_x(xi)
        xj_index = self.find_index_x(xj)
        if self.x_sorted_type == Ordering.ASCENDING or \
                self.x_sorted_type == Ordering.DESCENDING:
            return (xi_index, xj_index) if xi_index <= xj_index else (xj_index, xi_index)
        else:
            res_set = set(xi_index) | set(xj_index)
            if len(res_set) <= 1:
                raise RuntimeError("index range unfounded.")
            return min(res_set), max(res_set)

    def slice(self, xi: Union[int, float], xj: Union[int, float]):
        """
        从光谱数据中截取一个片段。

        :param xi: 指定的波数1。
        :param xj: 指定的波数2。
        :return: 截取到的片段。
        """
        index_xi, index_xj = self.find_index_xrange(xi, xj)
        slice_x = self.x[index_xi:index_xj + 1]
        slice_y = self.y[index_xi:index_xj + 1]
        if self.e is not None:
            slice_e = self.e[index_xi:index_xj + 1]
        else:
            slice_e = None
        return Spectrum(slice_y, slice_x, slice_e, **self.kwargs)

    def find_x_peak(self, x_start: Union[int, float],
                    x_end: Union[int, float],
                    peak_type: Union[int, float] = 0):
        """
        找到指定区间内的最大值或最小值所对应的x坐标。

        :param x_start: 指定的波数1。
        :param x_end: 指定的波数2。
        :param peak_type: 0表示找到最大值，1表示找到最小值。
        :return: 最大值或最小值的x值和y值。
        """
        _slice = self.slice(x_start, x_end)
        _x = _slice.x
        _y = _slice.y
        if peak_type == 0 or peak_type.__eq__('max'):
            __extreme_value = _slice.y_max
        else:
            __extreme_value = _slice.y_min
        r = np.where(np.diff(np.sign(_y - __extreme_value)) != 0)
        idx = r + (__extreme_value - _y[r]) / (_y[r + np.ones_like(r)] - _y[r])
        idx = np.append(idx, np.where(_y == __extreme_value))
        idx = np.sort(idx)
        return _x[int(np.round(idx)[0])], __extreme_value

    # ================================================================
    def savgol_filter(self, window_length, polyorder=3,
                      deriv=0, delta=1.0, mode='nearest', cval=0.0,
                      **kwargs):
        """
        对谱数据执行Savitzky-Golay滤波。

            1. window_length：窗口长度，该值需为正奇整数。

            2. polyorder：polyorder为对窗口内的数据点进行polyorder阶多项式拟合，
                polyorder的值需要小于window_length。

            3. mode：确定了要应用滤波器的填充信号的扩展类型。

        调参规律：

        现在看一下window_length和polyorder这两个值对曲线的影响。

            1. window_length对曲线的平滑作用： window_length的值越小，
            曲线越贴近真实曲线；window_length值越大，平滑效果越厉害（备注：该值必须为正奇整数）。

            2. polyorder值对曲线的平滑作用： k值越大，曲线越贴近真实曲线；k值越小，
            曲线平滑越厉害。另外，当k值较大时，受窗口长度限制，拟合会出现问题，高频曲线会变成直线。

        :param window_length : int
                The length of the filter window (i.e., the number of coefficients).
                If `mode` is 'interp', `window_length` must be less than or equal
                to the size of `x`.
        :param polyorder : int
                The order of the polynomial used to fit the samples.
                `polyorder` must be less than `window_length`.
        :param deriv : int, optional
                The order of the derivative to compute. This must be a
                nonnegative integer. The default is 0, which means to filter
                the data without differentiating.
        :param delta : float, optional
                The spacing of the samples to which the filter will be applied.
                This is only used if deriv > 0. Default is 1.0.
        :param mode : str, optional
                Must be 'mirror', 'constant', 'nearest', 'wrap' or 'interp'. This
                determines the type of extension to use for the padded signal to
                which the filter is applied.  When `mode` is 'constant', the padding
                value is given by `cval`.  See the Notes for more details on 'mirror',
                'constant', 'wrap', and 'nearest'.
                When the 'interp' mode is selected (the default), no extension
                is used.  Instead, a degree `polyorder` polynomial is fit to the
                last `window_length` values of the edges, and this polynomial is
                used to evaluate the last `window_length // 2` output values.
        :param cval : scalar, optional
                Value to fill past the edges of the input if `mode` is 'constant'.
                Default is 0.0.
        :return: 拟合后的谱数据。
        """
        # 使用scipy.signal.savgol_filter函数执行平滑处理。
        y_smoothed = sp.signal.savgol_filter(self.y, window_length=window_length,
                                             polyorder=polyorder, deriv=deriv,
                                             delta=delta, mode=mode, cval=cval)

        # 对平滑效果做统计分析，注意：这里的拟合变量数量使用了多项式阶数+1，这获取并不科学
        # 因为拟合变量数量不严谨，应注重其：rsquared。
        __fs = FittingStatistics(self.y, y_smoothed, nvars_fitted=polyorder + 1, x=self.x)

        print("R^2={}".format(__fs.rsquared))
        # 制作数据准备输出。
        res_data = pd.DataFrame({"x": self.x, "y": self.y, "y_smoothed": y_smoothed,
                                 "residuals": self.y - y_smoothed})
        res_data_smoothed = pd.DataFrame({"x": self.x, "y_smoothed": y_smoothed})

        if ("sample_name" in kwargs) and (kwargs["sample_name"] is not None):
            sample_name = kwargs["sample_name"]
        else:
            sample_name = "sample"

        if "data_outpath" in kwargs:
            if kwargs["data_outpath"] is None:
                data_outpath = os.path.abspath(os.path.dirname(__file__))
            else:
                data_outpath = kwargs["data_outpath"]
            if not os.path.exists(data_outpath):
                os.mkdir(data_outpath)
            data_outfile = os.path.join(
                data_outpath,
                "{}_savgol_{}_{}_{}_{}_{}_{}.csv".format(
                    sample_name, window_length, polyorder, deriv, delta, mode, cval)
            )
            data_outfile_smoothed = os.path.join(
                data_outpath,
                "{}_savgol_{}_{}_{}_{}_{}_{}_smoothed.csv".format(
                    sample_name, window_length, polyorder, deriv, delta, mode, cval)
            )
            res_data.to_csv(data_outfile, index=False)
            res_data_smoothed.to_csv(data_outfile_smoothed, index=False)

        if "is_show_data" in kwargs and kwargs["is_show_data"]:
            print(res_data)

        # 绘图时显示中文。
        plt.rcParams['font.family'] = 'SimHei'
        plt.rcParams['axes.unicode_minus'] = False

        if "with_plot" in kwargs and kwargs["with_plot"]:
            plt.figure(figsize=(16, 6))
            plt.subplot(1, 2, 1)
            plt.plot(self.x, self.y, label="raw")
            plt.plot(self.x, y_smoothed, label="savgol_{}_{}_{}_{}_{}_{}".format(
                window_length, polyorder, deriv, delta, mode, cval))
            plt.title('savgol_filter')
            plt.xlabel("x")
            plt.ylabel("y")
            plt.legend(loc='best')

            plt.subplot(1, 2, 2)
            plt.plot(self.x, self.y - y_smoothed,
                     label="savgol_{}_{}_{}_{}_{}_{}_residuals".format(
                         window_length, polyorder, deriv, delta, mode, cval))
            plt.title('residuals')
            plt.xlabel("x")
            plt.ylabel("y")
            plt.legend(loc='best')

            if "fig_outpath" in kwargs:
                if kwargs["fig_outpath"] is None:
                    fig_outpath = os.path.abspath(os.path.dirname(__file__))
                else:
                    fig_outpath = kwargs["fig_outpath"]
                if not os.path.exists(fig_outpath):
                    os.mkdir(fig_outpath)
                fig_outfile = os.path.join(
                    fig_outpath,
                    "{}_savgol_{}_{}_{}_{}_{}_{}.png".format(
                        sample_name, window_length, polyorder, deriv, delta, mode, cval)
                )
                plt.savefig(fig_outfile)

            if "is_show_fig" in kwargs and kwargs["is_show_fig"]:
                plt.show()
        return Spectrum(y_smoothed, self.x, self.y - y_smoothed,
                        raw_y=self.y, fitting_statistics=__fs, **self.kwargs)

    # noinspection DuplicatedCode
    def deriv_zhxyao(self, v: float, b: float = None, p: float = None, **kwargs):
        """
        计算谱数据的任意阶导数。

        :param v: 导数的阶，2阶导朝下，4阶朝上，6阶又往下。
        :param b: 峰宽，如果值太大容易造成过拟合，失真。
        :param p: 峰类型，p值为2时，峰型为高斯，p越小，越像洛伦兹。
        :param kwargs: 其他可选关键字参数。
        :return:谱值的导数。
        """
        t, s, _, _, _, = deriv_quasi_sech(self.y, v, b, p)
        t_domain_residual = self.y - t
        f_domain_residual = np.real(np.fft.fftshift(np.fft.fft(t_domain_residual)))
        res_data = pd.DataFrame({'x': self.x, "y": self.y,
                                 's': s, "t": t,
                                 't_domain_residual': t_domain_residual,
                                 'f_domain_residual': f_domain_residual})
        t_res_data = pd.DataFrame({'x': self.x, "t": t})

        fs = FittingStatistics(self.y, t, 3, self.x)

        if "ampd_method" in kwargs and kwargs["ampd_method"] is not None:
            ampd_method = kwargs["ampd_method"]
        else:
            ampd_method = "ampd"

        peak_up_index = ampd(s, peak_type=0, method=ampd_method, **kwargs)
        peak_down_index = ampd(s, peak_type=1, method=ampd_method, **kwargs)

        if ("sample_name" in kwargs) and (kwargs["sample_name"] is not None):
            sample_name = kwargs["sample_name"]
        else:
            sample_name = "sample"

        if "data_outpath" in kwargs:
            if kwargs["data_outpath"] is None:
                data_outpath = os.path.abspath(os.path.dirname(__file__))
            else:
                data_outpath = kwargs["data_outpath"]
            if not os.path.exists(data_outpath):
                os.mkdir(data_outpath)
            data_outfile = os.path.join(
                data_outpath,
                "{}_deriv_{}_{}_{}.csv".format(
                    sample_name, v, b, p)
            )
            data_outfile_t = os.path.join(
                data_outpath,
                "{}_deriv_{}_{}_{}_t.csv".format(
                    sample_name, v, b, p)
            )
            res_data.to_csv(data_outfile, index=False)
            t_res_data.to_csv(data_outfile_t, index=False)

        if "is_show_data" in kwargs and kwargs["is_show_data"]:
            print(res_data)

        if "with_plot" in kwargs and kwargs["with_plot"]:

            plt.subplot(2, 2, 1)
            plt.plot(self.x, self.y, label="raw")
            plt.plot(self.x, t, label="Derivate 0")
            plt.title('RAW & 0-ORDER')
            plt.legend(loc='best')

            plt.subplot(2, 2, 2)
            plt.plot(self.x, s, label="Derivate {}".format(v))
            plt.scatter(self.x[peak_up_index], s[peak_up_index], c='red', label="upper")
            plt.scatter(self.x[peak_down_index], s[peak_down_index], c='green', label="down")
            plt.title('RESULTS')
            plt.legend(loc='best')

            plt.subplot(2, 2, 3)
            plt.plot(self.x, t_domain_residual, label="t_domain_residual")
            plt.title('T-DOMAIN RESIDUALS')
            plt.legend(loc='best')

            plt.subplot(2, 2, 4)
            plt.plot(self.x, f_domain_residual, label="f_domain_residual")
            plt.title('F-DOMAIN RESIDUALS')
            plt.legend(loc='best')
            plt.tight_layout()

            if "fig_outpath" in kwargs:
                if kwargs["fig_outpath"] is None:
                    fig_outpath = os.path.abspath(os.path.dirname(__file__))
                else:
                    fig_outpath = kwargs["fig_outpath"]
                if not os.path.exists(fig_outpath):
                    os.mkdir(fig_outpath)
                fig_outfile = os.path.join(
                    fig_outpath,
                    "{}_deriv_{}_{}_{}.png".format(
                        sample_name, v, b, p)
                )
                plt.savefig(fig_outfile)

            if "is_show_fig" in kwargs and kwargs["is_show_fig"]:
                plt.show()

        return res_data, fs, peak_up_index, peak_down_index

    def smoothing_criterion(self, r_squared_criteria: float = 0.999,
                            peak_width_start: float = 10,
                            peak_width_step: float = 1,
                            peak_width_iterations: int = 100,
                            init_peak_steepness: float = 1,
                            min_peak_steepness_criteria: float = 0.5):
        """
        基于指定的标准对谱进行拟合。

        :param peak_width_start: 峰宽的起点。
        :param peak_width_step: 峰宽的步长。
        :param peak_width_iterations: 峰宽的迭代次数。
        :param init_peak_steepness: 初始峰陡峭度标准。
        :param r_squared_criteria: R^2标准。
        :param min_peak_steepness_criteria: 最小峰陡峭度标准。
        :return: (data_fitted, peak_width, peak_steepness_fitted, r_squared)
        """
        from ..zhxyao import smoothing_zhxyao
        return smoothing_zhxyao(self.y, peak_width_start,
                                peak_width_step, peak_width_iterations,
                                init_peak_steepness, r_squared_criteria,
                                min_peak_steepness_criteria)

    # noinspection DuplicatedCode
    def smoothing_zhxyao(self, b: float = None, **kwargs):
        """
        基于任意阶导数（“姚志祥老师开发的算法”）的谱数据平滑处理。

        :param b: 峰宽，如果值太大容易造成过拟合，失真。
        :param kwargs: 其他可选关键字参数。
        :return:谱值的导数。
        """

        def loss_func(p_arg):
            smoothing_y = deriv_quasi_sech(self.y, 0, b, p_arg)
            ret = self.y - smoothing_y
            return ret

        p_init = 2
        # noinspection PyTypeChecker
        p_lsq = leastsq(loss_func, p_init)
        p = p_lsq[0][0]
        # noinspection PyTypeChecker
        t,_,_,_,_ = deriv_quasi_sech(self.y, 0, b, p)
        fs = FittingStatistics(self.y, t, 1, self.x)

        if "deriv_order" in kwargs:
            deriv_order = kwargs["deriv_order"]
        else:
            deriv_order = 2
        # noinspection PyTypeChecker
        s = deriv_quasi_sech(self.y, deriv_order, b, p)

        t_domain_residual = self.y - t
        f_domain_residual = np.real(np.fft.fftshift(np.fft.fft(t_domain_residual)))
        res_data = pd.DataFrame({'x': self.x, "y": self.y,
                                 's': s, "t": t,
                                 't_domain_residual': t_domain_residual,
                                 'f_domain_residual': f_domain_residual})
        t_res_data = pd.DataFrame({'x': self.x, "t": t})
        if "ampd_method" in kwargs and kwargs["ampd_method"] is not None:
            ampd_method = kwargs["ampd_method"]
        else:
            ampd_method = "ampd"

        peak_up_index = ampd(s, peak_type=0, method=ampd_method, **kwargs)
        peak_down_index = ampd(s, peak_type=1, method=ampd_method, **kwargs)

        if ("sample_name" in kwargs) and (kwargs["sample_name"] is not None):
            sample_name = kwargs["sample_name"]
        else:
            sample_name = "sample"

        if "data_outpath" in kwargs:
            if kwargs["data_outpath"] is None:
                data_outpath = os.path.abspath(os.path.dirname(__file__))
            else:
                data_outpath = kwargs["data_outpath"]
            if not os.path.exists(data_outpath):
                os.mkdir(data_outpath)
            data_outfile = os.path.join(
                data_outpath,
                "{}_deriv_{}_{}_{}.csv".format(
                    sample_name, deriv_order, b, p)
            )
            data_outfile_t = os.path.join(
                data_outpath,
                "{}_deriv_{}_{}_{}_t.csv".format(
                    sample_name, deriv_order, b, p)
            )
            res_data.to_csv(data_outfile, index=False)
            t_res_data.to_csv(data_outfile_t, index=False)

        if "is_show_data" in kwargs and kwargs["is_show_data"]:
            print(res_data)

        if "with_plot" in kwargs and kwargs["with_plot"]:

            plt.subplot(2, 2, 1)
            plt.plot(self.x, self.y, label="raw")
            plt.plot(self.x, t, label="Derivate 0")
            plt.title('RAW & 0-ORDER')
            plt.legend(loc='best')

            plt.subplot(2, 2, 2)
            plt.plot(self.x, s, label="Derivate {}".format(deriv_order))
            plt.scatter(self.x[peak_up_index], s[peak_up_index], c='red', label="upper")
            plt.scatter(self.x[peak_down_index], s[peak_down_index], c='green', label="down")
            plt.title('RESULTS')
            plt.legend(loc='best')

            plt.subplot(2, 2, 3)
            plt.plot(self.x, t_domain_residual, label="t_domain_residual")
            plt.title('T-DOMAIN RESIDUALS')
            plt.legend(loc='best')

            plt.subplot(2, 2, 4)
            plt.plot(self.x, f_domain_residual, label="f_domain_residual")
            plt.title('F-DOMAIN RESIDUALS')
            plt.legend(loc='best')
            plt.tight_layout()

            if "fig_outpath" in kwargs:
                if kwargs["fig_outpath"] is None:
                    fig_outpath = os.path.abspath(os.path.dirname(__file__))
                else:
                    fig_outpath = kwargs["fig_outpath"]
                if not os.path.exists(fig_outpath):
                    os.mkdir(fig_outpath)
                fig_outfile = os.path.join(
                    fig_outpath,
                    "{}_deriv_{}_{}_{}.png".format(
                        sample_name, deriv_order, b, p)
                )
                plt.savefig(fig_outfile)

            if "is_show_fig" in kwargs and kwargs["is_show_fig"]:
                plt.show()

        return res_data, fs, peak_up_index, peak_down_index, p

    def sharpen_zhxyao(self, v: float, b: float, p: float, k: float):
        """
        对y坐标数据进行锐化处理。

        :param v: 导数的阶，2阶导朝下，4阶朝上，6阶又往下。
        :param b: 峰宽，如果值太大容易造成过拟合，失真。
        :param p: 峰类型，p值为2时，峰型为高斯，p越小，越像洛伦兹。
        :param k: 锐化系数。
        :return: 数据锐化后的谱，锐化后的y坐标数据。
        """
        t, _, _, _, _ = deriv_quasi_sech(self.y, 0, b, p)
        s, _, _, _, _ = deriv_quasi_sech(self.y, v, b, p)
        y_sharpen = t - k * s
        return Spectrum(y_sharpen, self.x, self.e, **self.kwargs), y_sharpen

    # ================================================================

    def peak_detect(self, peak_type: int = 0, method="ampd", **kwargs):
        """
        基于多尺度的自动峰值检测（automatic multiscale-based peak detection）。

        参考文献：An Efficient Algorithm for Automatic Peak Detection
                in Noisy Periodic and Quasi-Periodic Signals

        支持的算法：

           1. find_peaks_original(spectrum, scale=scale, debug=debug)

           2. find_peaks(spectrum, scale=scale, debug=debug)

           3. find_peaks_adaptive(spectrum, window=window, debug=debug)

           4. ampd(spectrum, lsm_limit=lsm_limit)

           5. ampd_fast(spectrum, window_length=window_length, hop_length=hop_length, lsm_limit=lsm_limit,
                        verbose=verbose)

           6. ampd_fast_sub(spectrum, order=order, lsm_limit=lsm_limit, verbose=verbose)

           7. ampd_wangjy(spectrum)

        :param peak_type: 0代表波峰、1代表波谷。
        :param method: 算法库选择。
        :return: 峰所在索引值的数组。
        :rtype: np.ndarray
        """
        return ampd(self.y, peak_type=peak_type, method=method, **kwargs)

    # ================================================================
    def summary(self, **kwargs) -> Tuple[pd.DataFrame, dict]:
        """
        将`Spectrum`数据转换为pandas.DataFrame对象。

        可识别的关键字参数包括：

            1. y_name: y列名。

            2. x_name: x列名。

            3. e_name: 误差列名。

            4. s_name: 理论计算误差列名。

            5. w_name: 理论计算权重列名。

            6. is_contain_e: 是否包含e列，如果为True，且e列非None，则包含列，否则表示不包含。

            7. is_contain_s: 是否包含s列，如果为True，则包含列，否则表示不包含。

            8. is_contain_w: 是否包含w列，如果为True，则包含列，否则表示不包含。

            9. data_outfile: 数据输出文件的路径。

        :return: 一个元组，元组的第1个元素为pandas.DataFrame对象，第2个元素为dict对象。
        :rtype:Tuple[pd.DataFrame,dict]
        """
        if ("y_name" not in kwargs) or (kwargs["y_name"] is None):
            y_name = "y"
        else:
            y_name = kwargs["y_name"]

        if ("x_name" not in kwargs) or (kwargs["x_name"] is None):
            x_name = "x"
        else:
            x_name = kwargs["x_name"]

        res_dict = {x_name: self.x, y_name: self.y}

        if "is_contain_e" in kwargs and kwargs["is_contain_e"]:
            if self.e is not None:
                if ("e_name" not in kwargs) or (kwargs["e_name"] is None):
                    e_name = "Err"
                else:
                    e_name = kwargs["e_name"]
                res_dict[e_name] = self.e

        if "is_contain_s" in kwargs and kwargs["is_contain_s"]:
            if ("s_name" not in kwargs) or (kwargs["s_name"] is None):
                s_name = "s"
            else:
                s_name = kwargs["s_name"]
            res_dict[s_name] = self.s

        if "is_contain_w" in kwargs and kwargs["is_contain_w"]:
            if ("w_name" not in kwargs) or (kwargs["w_name"] is None):
                w_name = "w"
            else:
                w_name = kwargs["w_name"]
            res_dict[w_name] = self.w

        res_data = pd.DataFrame(res_dict)

        if "data_outfile" in kwargs and kwargs["data_outfile"] is not None:
            res_data.to_csv(kwargs["data_outfile"], sep=',', index=False)

        return res_data, res_dict

    # noinspection DuplicatedCode
    def plot(self, **kwargs):
        """
        绘制图谱。

        可选参数：
            is_with_e：bool, 指示是否绘制误差数据。

            fig_outfile：str，指示图片保存的完整路径。

        :param kwargs: 可选关键字参数。
        """
        plt.plot(self.x, self.y, label="y~x")

        if 'is_with_e' in kwargs and kwargs['is_with_e']:
            if self.e is not None:
                plt.fill_between(self.x, self.y - self.e, self.y + self.e, alpha=0.5)
            else:
                plt.fill_between(self.x, self.y - self.s, self.y + self.s, alpha=0.5)

        plt.legend(loc='best')
        plt.tight_layout()

        if 'fig_outfile' in kwargs and kwargs['fig_outfile'] is not None:
            fig_outfile = kwargs['fig_outfile']
            plt.savefig(fig_outfile)

        plt.show()

    def to_csv(self, csv_file: str, index=False):
        res_dict = {'x': self.x, 'y': self.y}
        if not os.path.exists(Path(csv_file).parent):
            os.makedirs(Path(csv_file).parent)
        pd.DataFrame(res_dict).to_csv(csv_file, index=index)
