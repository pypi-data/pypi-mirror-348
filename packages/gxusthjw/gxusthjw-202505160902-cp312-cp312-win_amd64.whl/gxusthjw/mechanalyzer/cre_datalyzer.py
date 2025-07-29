#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        cre_datalyzer.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      定义“表征`恒（常）应变速率力学数据分析器`”的类。
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2024/10/26     finish
# ------------------------------------------------------------------
# 导包 ==============================================================
from typing import Optional

import numpy as np
import numpy.typing as npt
from matplotlib import pyplot as plt
from numpy import trapz

from ..commons import (
    NumberArrayLike, find_crossing_index,Specimen
)

from ..filters import Data2dRegionSavgolFilter
from ..fitters import interactive_linear_fitting_sm
from .unit_convert import (
    length_unit_to_mm,
    time_unit_to_s,
    force_unit_to_cn,
    area_unit_to_mm2,
    speed_unit_to_mms,
)
from .initial_modulus_region import InitialModulusRegion
from .yield_region import YieldRegion

# 声明 ==============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defines a class that represents `mechanical data analyzer of
 constant strain rate`.
"""

__all__ = ["CreMechDataAnalyzer"]


# 定义 ==============================================================
class CreMechDataAnalyzer(Specimen):
    """
    类`CreMechDataAnalyzer`表征“恒（常）应变速率力学数据分析器”。

    力学试验仪按照加载方式的不同，可分为三种基本类型：

        (1) 等速伸长型（Constant Rate of Extension, CRE）:
            试样以恒定的速度被拉伸，直到断裂。主要特点是伸长量与时间成正比。
            由于拉伸过程中，试样的应变率不变，故又称为恒（常）应变速率（Constant Strain Rate, CSR）型力学测试。

        (2)等加负荷型(Constant Rate of Loading, CRL):
           与等速伸长型（CRE）相比，在CRL测试中，试验机以恒定的速率增加施加于试样的载荷，
           而不是以恒定的速度拉伸试样。主要的特点是受力的大小与时间成正比。

        (3)等速牵引型(Constant Rate of Traverse, CRT)：
            等速牵引型强力机的主要代表是摆锤式强力仪，其发展比较早，也比较成熟，目前仍大量应用。
            例如,测棉花束纤维强力的斯特洛强力仪，其主要特点是牵引部件（夹持器）的位移与时间成正比，
            由此定义可知，CRT与CRE的原理是一致的。

    目前很多标准规定或推荐采用CRE型力学试验仪。
    """

    def __init__(
        self,
        displacements: NumberArrayLike,
        forces: NumberArrayLike,
        times: Optional[NumberArrayLike] = None,
        *,
        displacement_unit: str = "mm",
        force_unit: str = "cN",
        time_unit: str = "s",
        clamp_distance: Optional[float] = None,
        clamp_distance_unit: str = "mm",
        cross_area: Optional[float] = None,
        cross_area_unit: str = "mm^2",
        speed: Optional[float] = None,
        speed_unit: str = "mm/s",
        sampling_frequency: Optional[float] = None,
        threshold_strain: Optional[float] = None,
        specimen_name: str = "specimen",
        specimen_no: int = 0,
        data_analyzer_name: str = "CreMechDataAnalyzer",
        data_logger_name: str = "CreMechDataAnalyzer_DataLogger",
        **kwargs,
    ):
        """
        类`CreMechDataAnalyzer`的初始化方法。

        :param displacements: 位移数据项。
        :param forces: 力数据项。
        :param times: 时间数据项，默认值为：None。
        :param displacement_unit: 位移数据的单位，缺省值为：mm。
        :param force_unit: 力数据的单位，缺省值为：cN。
        :param time_unit: 时间数据的单位，缺省值为：s。
        :param clamp_distance: 夹持距离，缺省值为：None。
        :param clamp_distance_unit: 夹持距离的单位，缺省值为：mm。
        :param cross_area: 截面积，缺省值为：None。
        :param cross_area_unit: 截面积的单位，缺省值为：mm^2。
        :param speed: 拉伸或压缩速度，缺省值为：None。
        :param speed_unit: 拉伸或压缩速度的单位，缺省值为：mm/s。
        :param sampling_frequency: 采样频率，单位：Hz，即，次/s。
        :param threshold_strain: 阈值应变，理论上，阈值应变后的数据应被丢弃。
        :param specimen_name: 样品名，缺省值为：‘specimen’。
        :param specimen_no: 测试编号，缺省值为：0。
        :param data_analyzer_name:  数据分析器的名称，默认值：'CreMechDataAnalyzer'。
        :param data_logger_name: 数据记录器的名称，默认值：'CreMechDataAnalyzer_DataLogger'。
        :param kwargs: 其他可选关键字参数。
        """
        # 数据初始化 ----------------------------------------------------
        if displacements is None:
            raise ValueError("Expect displacements to be not None.")
        self.__displacements = np.asarray(displacements)
        if forces is None:
            raise ValueError("Expect forces to be not None.")
        self.__forces = np.asarray(forces)
        self.__times = np.asarray(times) if times is not None else None
        # -------------------------------------------------------------

        # 蕴含数据 ------------------------------------------------------
        self.__data_len = self.__displacements.shape[0]

        # 要求各数据项的长度相同。
        if self.__forces.shape[0] != self.__data_len:
            raise ValueError(
                "Expect data items (displacements,forces)" " to be the same length."
            )

        if self.__times is not None and self.__times.shape[0] != self.__data_len:
            raise ValueError(
                "Expect data items (displacements,times)" " to be the same length."
            )

        # 初始化编号数据项。
        self.__data_nos = np.arange(1, self.__data_len + 1)
        # 设置编号数据项为不可变。
        self.__data_nos.setflags(write=False)
        # -------------------------------------------------------------

        # 单位转换 -----------------------------------------------------
        if displacement_unit not in ["m", "dm", "cm", "mm"]:
            raise ValueError(
                "Expect displacement_unit to be 'm' or 'dm' or 'cm' or 'mm'."
            )
        self.__displacements = length_unit_to_mm(
            self.__displacements, displacement_unit
        )
        self.__displacements.setflags(write=False)
        self.__displacement_unit = "mm"

        if force_unit not in ["N", "cN"]:
            raise ValueError("Expect force_unit to be 'N', 'cN'.")
        self.__forces = force_unit_to_cn(self.__forces, force_unit)
        self.__forces.setflags(write=False)
        self.__force_unit = "cN"

        if time_unit not in ["h", "min", "s"]:
            raise ValueError("Expect time_unit to be 'h' or 'min' or 's'.")
        if self.__times is not None:
            self.__times = time_unit_to_s(self.__times, time_unit)
            self.__times.setflags(write=False)
        self.__time_unit = "s"
        # 初始化其他参数 --------------------------------------------------
        if clamp_distance is not None and clamp_distance <= 0:
            raise ValueError("Expect clamp_distance to be greater than 0.")
        else:
            self.__clamp_distance = clamp_distance

        if clamp_distance_unit not in ["m", "dm", "cm", "mm"]:
            raise ValueError(
                "Expect clamp_distance_unit to be 'm' or 'dm' or 'cm' or 'mm'."
            )
        if self.__clamp_distance is not None:
            self.__clamp_distance = length_unit_to_mm(
                self.__clamp_distance, clamp_distance_unit
            )
        self.__clamp_distance_unit = "mm"

        if cross_area is not None and cross_area <= 0:
            raise ValueError("Expect cross_area to be greater than 0.")
        else:
            self.__cross_area = cross_area

        if cross_area_unit not in ["m^2", "dm^2", "cm^2", "mm^2"]:
            raise ValueError(
                "Expect cross_area_unit to be 'm^2' or 'dm^2' or 'cm^2' or 'mm^2'."
            )
        if self.__cross_area is not None:
            self.__cross_area = area_unit_to_mm2(self.__cross_area, cross_area_unit)
        self.__cross_area_unit = "mm^2"

        if speed is not None and speed <= 0:
            raise ValueError("Expect speed to be greater than 0.")
        else:
            self.__speed = speed

        if speed_unit not in [
            "m/h",
            "dm/h",
            "cm/h",
            "mm/h",
            "m/min",
            "dm/min",
            "cm/min",
            "mm/min",
            "m/s",
            "dm/s",
            "cm/s",
            "mm/s",
        ]:
            raise ValueError(
                "Expect speed_unit to be "
                "'m/h' or 'dm/h' or 'cm/h' or 'mm/h' or "
                "'m/min' or 'dm/min' or 'cm/min' or 'mm/min' or "
                "'m/s' or 'dm/s' or 'cm/s' or 'mm/s'."
            )

        if self.__speed is not None:
            self.__speed = speed_unit_to_mms(self.__speed, speed_unit)
        self.__speed_unit = "mm/s"

        if sampling_frequency is not None and sampling_frequency <= 0:
            raise ValueError("Expect sampling_frequency to be greater than 0.")
        else:
            self.__sampling_frequency = sampling_frequency
        # 采样频率的单位只支持Hz，即：次/每秒。
        self.__sampling_frequency_unit = "Hz"

        # 阈值应变没有单位，其值实质上是：位移量/夹持距离 中的一个点。
        if threshold_strain is not None and threshold_strain <= 0:
            raise ValueError("Expect threshold_strain to be greater than 0.")
        else:
            self.__threshold_strain = threshold_strain

        # 初始化父类 ------------------------------------------------------
        super(CreMechDataAnalyzer, self).__init__(
            specimen_name=specimen_name,
            specimen_no=specimen_no,
            data_analyzer_name=data_analyzer_name,
            data_logger_owner=None,
            data_logger_name=data_logger_name,
            **kwargs,
        )
        # 记录数据 -------------------------------------------------------
        self.data_logger.log(self.__displacements, "displacements")
        self.data_logger.log(self.__displacement_unit, "displacement_unit")
        self.data_logger.log(self.__forces, "forces")
        self.data_logger.log(self.__force_unit, "force_unit")
        self.data_logger.log(self.__times, "times")
        self.data_logger.log(self.__time_unit, "time_unit")
        self.data_logger.log(self.__data_nos, "data_nos")
        self.data_logger.log(self.__data_len, "data_len")

        self.data_logger.log(self.__clamp_distance, "clamp_distance")
        self.data_logger.log(self.__clamp_distance_unit, "clamp_distance_unit")
        self.data_logger.log(self.__cross_area, "cross_area")
        self.data_logger.log(self.__cross_area_unit, "cross_area_unit")

        self.data_logger.log(self.__speed, "speed")
        self.data_logger.log(self.__speed_unit, "speed_unit")
        self.data_logger.log(self.__sampling_frequency, "sampling_frequency")
        self.data_logger.log(self.__sampling_frequency_unit, "sampling_frequency_unit")
        self.data_logger.log(self.__threshold_strain, "threshold_strain")
        # init 结束 ------------------------------------------------------------

    # ===================================================================
    @property
    def displacements(self) -> npt.NDArray[np.float64]:
        """
        获取位移数据项。

        :return: 位移数据项。
        """
        return self.__displacements

    @property
    def displacement_unit(self) -> str:
        """
        获取位移数据项的单位。

            位移数据项的单位必须为：`mm`。

        :return: 位移数据项的单位。
        """
        return self.__displacement_unit

    @property
    def forces(self) -> npt.NDArray[np.float64]:
        """
        获取力数据项。

        :return: 力数据项。
        """
        return self.__forces

    @property
    def force_unit(self) -> str:
        """
        获取力数据项的单位。

            力数据项的单位必须为：`cN`。

        :return: 力数据项的单位。
        """
        return self.__force_unit

    @property
    def times(self) -> Optional[npt.NDArray[np.float64]]:
        """
        获取时间数据项。

        :return: 时间数据项。
        """
        return self.__times

    @property
    def time_unit(self) -> Optional[str]:
        """
        获取时间数据项的单位。

            时间数据项的单位必须为：`s`。

        :return: 时间数据项的单位。
        """
        return self.__time_unit

    def set_times(self, times: NumberArrayLike, unit: str = "s"):
        """
        设置时间数据项。

        :param times: 时间数据项的数据。
        :param unit: 时间数据项的单位。
        :return: None
        """
        self.__times = time_unit_to_s(np.asarray(times), unit)
        self.__times.setflags(write=False)
        self.__time_unit = "s"
        self.data_logger.log(self.__times, "times")
        self.data_logger.log(self.__time_unit, "time_unit")

    @property
    def data_len(self) -> int:
        """
        获取数据长度。

        :return: 数据长度。
        """
        return self.__data_len

    @property
    def data_nos(self) -> npt.NDArray[np.float64]:
        """
        获取编号数据项。

        :return: 编号数据项。
        """
        return self.__data_nos

    @property
    def clamp_distance(self) -> Optional[float]:
        """
        获取夹持距离。

        :return: 夹持距离。
        """
        return self.__clamp_distance

    @property
    def clamp_distance_unit(self) -> Optional[str]:
        """
        获取夹持距离的单位。

        :return: 夹持距离的单位。
        """
        return self.__clamp_distance_unit

    def set_clamp_distance(self, clamp_distance: float, unit: str = "mm"):
        """
        设置夹持距离。

        :param clamp_distance: 夹持距离的值。
        :param unit: 夹持距离的单位。
        """
        if clamp_distance is None or clamp_distance <= 0:
            raise ValueError("Expect clamp_distance to be not None and greater than 0.")
        self.__clamp_distance = length_unit_to_mm(clamp_distance, unit)
        self.__clamp_distance_unit = "mm"
        self.data_logger.log(self.__clamp_distance, "clamp_distance")
        self.data_logger.log(self.__clamp_distance_unit, "clamp_distance_unit")

    @property
    def cross_area(self) -> Optional[float]:
        """
        获取横截面积。

        :return: 横截面积。
        """
        return self.__cross_area

    @property
    def cross_area_unit(self) -> Optional[str]:
        """
        获取横截面积的单位。

        :return: 横截面积的单位。
        """
        return self.__cross_area_unit

    def set_cross_area(self, cross_area: float, unit: str = "mm^2"):
        """
        设置横截面积。

        :param cross_area: 横截面积。
        :param unit: 横截面积的单位。
        """
        if cross_area is None or cross_area <= 0:
            raise ValueError("Expect cross_area to be not None and greater than 0.")
        self.__cross_area = area_unit_to_mm2(cross_area, unit)
        self.__cross_area_unit = "mm^2"
        self.data_logger.log(self.__cross_area, "cross_area")
        self.data_logger.log(self.__cross_area_unit, "cross_area_unit")

    @property
    def speed(self) -> Optional[float]:
        """
        获取拉伸或压缩速度。

        :return: 拉伸或压缩速度。
        """
        return self.__speed

    @property
    def speed_unit(self) -> Optional[str]:
        """
        获取拉伸或压缩速度单位。

        :return: 拉伸或压缩速度单位。
        """
        return self.__speed_unit

    def set_speed(self, speed: float, unit: str = "mm/s"):
        """
        设置拉伸或压缩速度及其单位。

        :param speed: 拉伸或压缩的速度。
        :param unit:  拉伸或压缩速度的单位。
        """
        if speed is None or speed <= 0:
            raise ValueError("Expect speed to be not None and greater than 0.")
        self.__speed = speed_unit_to_mms(speed, unit)
        self.__speed_unit = "mm/s"
        self.data_logger.log(self.__speed, "speed")
        self.data_logger.log(self.__speed_unit, "speed_unit")

    @property
    def sampling_frequency(self) -> Optional[float]:
        """
        获取信号采集的频率。

        :return: 信号采集的频率。
        """
        return self.__sampling_frequency

    @property
    def sampling_frequency_unit(self) -> Optional[str]:
        """
        获取信号采集频率的单位。

        :return: 信号采集频率的单位。
        """
        return self.__sampling_frequency_unit

    def set_sampling_frequency(self, sampling_frequency: float, unit: str = "Hz"):
        """
        设置信号采集的频率。
        :param sampling_frequency: 信号采集的频率值。
        :param unit: 信号采集频率的单位。
        """
        if unit not in ["Hz", "times/s"]:
            raise ValueError("Expect sampling_frequency to be 'Hz' or 'times/s'.")
        if sampling_frequency is None or sampling_frequency <= 0:
            raise ValueError(
                "Expect sampling_frequency to be not None and greater than 0."
            )
        self.__sampling_frequency = sampling_frequency
        self.__sampling_frequency_unit = "Hz"
        self.data_logger.log(self.__sampling_frequency, "sampling_frequency")
        self.data_logger.log(self.__sampling_frequency_unit, "sampling_frequency_unit")

    @property
    def threshold_strain(self) -> Optional[float]:
        """
        获取阈值应变。

        :return: 阈值应变。
        """
        return self.__threshold_strain

    def set_threshold_strain(self, threshold_strain: float):
        """
        设置阈值应变。

        :param threshold_strain: 阈值应变。
        """
        if threshold_strain is None or threshold_strain <= 0:
            raise ValueError(
                "Expect threshold_strain to be not None and greater than 0."
            )
        self.__threshold_strain = threshold_strain
        self.data_logger.log(self.__threshold_strain, "threshold_strain")

    # 计算属性 -----------------------------------------------------------
    @property
    def sampling_interval(self) -> Optional[float]:
        """
        获取信号采集时间间隔。

        :return: 信号采集时间间隔。
        """
        if self.sampling_frequency is not None:
            return 1.0 / self.sampling_frequency
        return None

    @property
    def sampling_interval_unit(self) -> str:
        """
        获取信号采集时间间隔的单位。

        :return: 信号采集时间间隔的单位。
        """
        return "s"

    @property
    def theoretical_strain_rate(self):
        """
        获取理论应变率。

        :return: 理论应变率。
        """
        if self.speed is not None and self.clamp_distance is not None:
            return self.speed / self.clamp_distance
        return None

    @property
    def theoretical_times(self) -> Optional[npt.NDArray[np.float64]]:
        """
        获取理论时间数据项。

        :return: 理论时间数据项。
        """
        if self.sampling_interval is not None:
            return self.data_nos * self.sampling_interval
        return None

    # 原始数据处理 -----------------------------------------------------------
    # noinspection PyUnresolvedReferences,PyUnusedLocal
    def calibrate_times(self, **kwargs):
        """
        校准时间数据。

            要求：`self.times is not None`

            新增对象属性：

            1. times_calibrated：校准后得到的时间数据。

            2. real_signal_interval: 实际信号采集时间间隔。

            3. real_signal_frequency: 实际信号采集的频率。

        :param kwargs: 校准数据所需的可选关键字参数。
        :return: 校准后的时间数据，拟合结果。
        """
        # -----------------------------------------
        if self.times is None:
            raise ValueError("Expect times to be specified.")
        # -----------------------------------------
        _, _, _, res = interactive_linear_fitting_sm(
            self.times, self.data_nos, title=f"Calibrate Times [{self.sample_name}]"
        )
        slope = res.params[1]
        real_signal_interval = slope
        real_signal_frequency = 1.0 / real_signal_interval
        times_calibrated = self.data_nos * slope
        setattr(self, "times_calibrated", times_calibrated)
        setattr(self, "real_signal_interval", real_signal_interval)
        setattr(self, "real_signal_frequency", real_signal_frequency)
        self.data_logger.log(self.times_calibrated, "times_calibrated")
        self.data_logger.log(self.real_signal_interval, "real_signal_interval")
        self.data_logger.log(self.real_signal_frequency, "real_signal_frequency")
        return times_calibrated, res

    def calibrate_displacements(self, **kwargs):
        """
        校准位移数据。

            可选关键字参数：

                1. using_data_nos: 指示是否采用编号数据进行校准，默认值为：False。

            新增对象属性：

                1. displacements_calibrated：校准后的位移数据。

                2. real_displacement_rate：真实的位移速率，如果使用时间数据对位移数据校准，
                                          则新增此对象属性。

                3.real_speed：真实的拉伸速度，如果使用时间数据对位移数据校准，
                                          则新增此对象属性。

                4. real_strain_rate：真实应变率，如果使用时间数据对位移数据校准，
                                    且夹持距离不为None，则新增此对象属性。

                5.real_strain_percentage：真实应变百分比率，如果使用时间数据对位移数据校准，
                                         且夹持距离不为None，则新增此对象属性。

        :param kwargs: 校准数据所需的可选关键字参数。
        :return: 校准后的位移数据，拟合结果。
        """
        # -----------------------------------
        using_data_nos = kwargs.pop("using_data_nos", False)
        # -----------------------------------
        if using_data_nos:
            _, _, _, res = interactive_linear_fitting_sm(
                self.displacements, self.data_nos
            )
            slope = res.params[1]
            displacement_calibrated = self.data_nos * slope
            setattr(self, "displacements_calibrated", displacement_calibrated)
            # noinspection PyUnresolvedReferences
            self.data_logger.log(
                self.displacements_calibrated, "displacements_calibrated"
            )
            return displacement_calibrated, res
        else:
            if hasattr(self, "times_calibrated"):
                times = self.times_calibrated
            elif self.times is not None:
                times, _ = self.calibrate_times()
            elif self.theoretical_times is not None:
                times = self.theoretical_times
            else:
                raise ValueError("Expect times or signal_frequency to be specified.")

            _, _, _, res = interactive_linear_fitting_sm(
                self.displacements,
                times,
                title=f"Calibrate Displacements [{self.sample_name}]",
            )
            slope = res.params[1]
            real_displacement_rate = slope
            displacement_calibrated = times * real_displacement_rate
            setattr(self, "displacements_calibrated", displacement_calibrated)
            setattr(self, "real_displacement_rate", real_displacement_rate)
            setattr(self, "real_speed", real_displacement_rate)
            # noinspection PyUnresolvedReferences
            self.data_logger.log(
                self.displacements_calibrated, "displacements_calibrated"
            )
            # noinspection PyUnresolvedReferences
            self.data_logger.log(self.real_displacement_rate, "real_displacement_rate")
            # noinspection PyUnresolvedReferences
            self.data_logger.log(self.real_speed, "real_speed")
            if self.clamp_distance is not None:
                real_strain_rate = real_displacement_rate / self.clamp_distance
                real_strain_percentage = real_strain_rate * 100
                setattr(self, "real_strain_rate", real_strain_rate)
                setattr(self, "real_strain_percentage", real_strain_percentage)
                # noinspection PyUnresolvedReferences
                self.data_logger.log(self.real_strain_rate, "real_strain_rate")
                # noinspection PyUnresolvedReferences
                self.data_logger.log(
                    self.real_strain_percentage, "real_strain_percentage"
                )
            return displacement_calibrated, res

    # noinspection PyUnusedLocal
    def calibrate_forces(self, **kwargs):
        """
        校准力数据。

        :param kwargs: 校准数据所需的可选关键字参数。
        :return: 校准后的力数据。
        """
        if hasattr(self, "displacements_calibrated"):
            displacements = self.displacements_calibrated
        else:
            displacements, _ = self.calibrate_displacements()

        forces_filter = Data2dRegionSavgolFilter(self.forces, displacements)
        forces_calibrated = forces_filter.interactive_smooth(
            interactive_mode="simple", title=f"Calibrate Forces [{self.sample_name}]"
        )
        # 零值对齐。
        forces_calibrated = forces_calibrated - forces_calibrated[0]
        setattr(self, "forces_calibrated", forces_calibrated)
        # noinspection PyUnresolvedReferences
        self.data_logger.log(self.forces_calibrated, "forces_calibrated")
        displacements_calibrated = displacements[
            forces_filter.region_start : forces_filter.region_start
            + forces_filter.region_length
        ]
        # 零值对齐
        displacements_calibrated = (
            displacements_calibrated - displacements_calibrated[0]
        )
        setattr(self, "displacements_calibrated", displacements_calibrated)
        # noinspection PyUnresolvedReferences
        self.data_logger.log(self.displacements_calibrated, "displacements_calibrated")
        if hasattr(self, "times_calibrated"):
            times_calibrated = self.times_calibrated[
                forces_filter.region_start : forces_filter.region_start
                + forces_filter.region_length
            ]
            # 零值对齐
            times_calibrated = times_calibrated - times_calibrated[0]
            setattr(self, "times_calibrated", times_calibrated)
            # noinspection PyUnresolvedReferences
            self.data_logger.log(self.times_calibrated, "times_calibrated")
        return forces_calibrated

    # 数据转换 --------------------------------------------------------------
    # noinspection PyUnresolvedReferences
    @property
    def strains(self) -> Optional[npt.NDArray[np.float64]]:
        """
        计算应变数据。

        :return: 应变数据。
        """
        if self.clamp_distance is None:
            return None
        if hasattr(self, "displacements_calibrated"):
            return self.displacements_calibrated / self.clamp_distance
        elif hasattr(self, "strain_rate"):
            return self.data_nos * self.strain_rate
        else:
            return self.displacements / self.clamp_distance

    @property
    def strain_percentages(self) -> Optional[npt.NDArray[np.float64]]:
        """
        计算应变百分比数据。

        :return: 应变百分比数据。
        """
        if self.strains is None:
            return None
        return self.strains * 100

    @property
    def stress(self) -> Optional[npt.NDArray[np.float64]]:
        """
        计算应力数据。

        :return: 应力数据。
        """
        if self.cross_area is None:
            return None
        if hasattr(self, "forces_calibrated"):
            return (self.forces_calibrated / self.cross_area) * 0.01
        else:
            return (self.forces / self.cross_area) * 0.01

    @property
    def stress_unit(self):
        """
        获取应力的单位。

        :return: 应力的单位。
        """
        return "MPa"

    # 数据裁取 --------------------------------------------------------------
    # noinspection PyUnresolvedReferences
    def data_trimmed(self, **kwargs):
        """
        数据裁取。

            新增对象属性：

            1. times_trimmed: 裁取得到的时间数据。

            2. strains_trimmed: 裁取得到的应变数据。

            3. strain_percentages: 裁取得到的应变百分比数据。

            4. stress_trimmed: 裁取得到的应力数据。

        :param kwargs: 裁取数据所需的可选关键字参数。
        """
        # ------------------------------------------------------------
        from matplotlib.widgets import SpanSelector

        # ------------------------------------------------------------
        if self.strains is None:
            raise ValueError("Strains can not be None.")
        if self.stress is None:
            raise ValueError("Stress can not be None.")
        # ------------------------------------------------------------
        label = "Raw"
        title = kwargs.pop(
            "title",
            f"Press left mouse button and drag"
            f" to select a region in the top"
            f" graph [{self.sample_name}]",
        )
        # ------------------------------------------------------------
        fig, (ax1, ax2) = plt.subplots(2, figsize=(8, 6))
        ax1.plot(self.strains, self.stress, label=label, **kwargs)
        ax1.set_title(title)
        ax1.set_xlabel("Strain")
        ax1.set_ylabel(f"Stress {self.stress_unit}")
        ax1.legend(loc="best")

        select_strains = self.strains
        select_stress = self.stress
        indmin_strains, indmax_strains = (0, len(self.strains) - 1)
        if self.threshold_strain is not None:
            indmin_strains, indmax_strains = np.searchsorted(
                self.strains, (min(self.strains), self.threshold_strain)
            )
            indmax_strains = min(len(self.strains) - 1, indmax_strains)
            select_strains = self.strains[indmin_strains : indmax_strains + 1]
            select_stress = self.stress[indmin_strains : indmax_strains + 1]
        (line2,) = ax2.plot(
            select_strains,
            select_stress,
            color="blue",
            label=f"Trimmed {self.threshold_strain}",
        )
        ax2.set_xlabel("Strain")
        ax2.set_ylabel(f"Stress {self.stress_unit}")
        ax2.legend(loc="best")

        # noinspection PyUnresolvedReferences
        def onselect(xmin, xmax):
            nonlocal select_strains, select_stress
            nonlocal indmin_strains, indmax_strains
            nonlocal line2
            indmin_strains, indmax_strains = np.searchsorted(self.strains, (xmin, xmax))
            indmax_strains = min(len(self.strains) - 1, indmax_strains)
            select_strains = self.strains[indmin_strains : indmax_strains + 1]
            select_stress = self.stress[indmin_strains : indmax_strains + 1]

            if len(select_strains) >= 2:
                line2.set_data(select_strains, select_stress)
                line2.set_color("red")
                # ax2.set_xlim(select_x[0], select_x[-1])
                # ax2.set_ylim(select_y.min(), select_y.max())
                fig.canvas.draw_idle()

        # noinspection PyUnusedLocal
        span = SpanSelector(
            ax1,
            onselect,
            "horizontal",
            useblit=True,
            props=dict(alpha=0.5, facecolor="tab:blue"),
            interactive=True,
            drag_from_anywhere=True,
        )
        # Set useblit=True on most backends for enhanced performance.
        plt.show()
        strains_trimmed = self.strains[indmin_strains : indmax_strains + 1]
        strains_trimmed = strains_trimmed - strains_trimmed[0]
        stress_trimmed = self.stress[indmin_strains : indmax_strains + 1]
        stress_trimmed = stress_trimmed - strains_trimmed[0]
        setattr(self, "strains_trimmed", strains_trimmed)
        setattr(self, "stress_trimmed", stress_trimmed)
        setattr(self, "strain_percentages_trimmed", strains_trimmed * 100)
        self.data_logger.log(strains_trimmed, "strains_trimmed")
        self.data_logger.log(stress_trimmed, "stress_trimmed")
        self.data_logger.log(
            self.strain_percentages_trimmed, "strain_percentages_trimmed"
        )
        if self.times is not None:
            times_trimmed = self.times[indmin_strains : indmax_strains + 1]
            times_trimmed = times_trimmed - times_trimmed[0]
            setattr(self, "times_trimmed", times_trimmed)
            self.data_logger.log(times_trimmed, "times_trimmed")
            return strains_trimmed, stress_trimmed, times_trimmed
        return strains_trimmed, stress_trimmed

    # ------------------------------------------------------------
    # noinspection PyUnusedLocal
    def calibrate_initial_modulus_region(self, **kwargs):
        """
        获取初始模量区。

        :return: 初始模量区。
        """
        if hasattr(self, "initial_modulus_region"):
            return getattr(self, "initial_modulus_region")
        else:
            if not hasattr(self, "stress_trimmed") or not hasattr(
                self, "strains_trimmed"
            ):
                self.data_trimmed()
            # noinspection PyUnresolvedReferences
            region = InitialModulusRegion(self.stress_trimmed, self.strains_trimmed)
            region.interactive_smooth(
                title=f"Calibrate Initial Modulus Region [{self.sample_name}]"
            )
            setattr(self, "initial_modulus_region", region)
            return region

    # noinspection PyStatementEffect
    @property
    def initial_modulus(self):
        """
        获取初始模量。
        """
        region = self.calibrate_initial_modulus_region()
        # noinspection PyUnresolvedReferences
        initial_modulus = region.fitting_result.params[1]
        return initial_modulus

    @property
    def initial_modulus_unit(self):
        """
        获取应力的单位。

        :return: 应力的单位。
        """
        return "MPa"

    # noinspection PyUnusedLocal
    def calibrate_yield_region(self, **kwargs):
        """
        获取屈服区域。

        :return: 屈服区。
        """
        if hasattr(self, "yield_region"):
            return getattr(self, "yield_region")
        else:
            if not hasattr(self, "stress_trimmed") or not hasattr(
                self, "strains_trimmed"
            ):
                self.data_trimmed()
            # noinspection PyUnresolvedReferences
            region = YieldRegion(self.stress_trimmed, self.strains_trimmed)
            region.interactive_smooth(
                title=f"Calibrate Yield Region [{self.sample_name}]"
            )
            setattr(self, "yield_region", region)
            return region

    # 分析数据 -------------------------------------------------------------
    # noinspection PyUnresolvedReferences
    @property
    def breaking_strength(self):
        """
        计算断裂强度。

        :return: 断裂强度。
        """
        if not hasattr(self, "stress_trimmed"):
            raise ValueError("Please calibrate the stress data and trim it.")
        return self.stress_trimmed[-1]

    @property
    def breaking_strength_unit(self):
        """
        返回断裂强度的单位。

        :return: 断裂强度的单位。
        """
        return "MPa"

    # noinspection PyUnresolvedReferences
    @property
    def breaking_elongation(self):
        """
        计算断裂伸长率。

        :return: 断裂伸长率。
        """
        if not hasattr(self, "stress_trimmed"):
            raise ValueError("Please calibrate the strains data and trim it.")
        return self.strains_trimmed[-1]

    @property
    def breaking_elongation_unit(self):
        """
        返回断裂伸长的单位。
        """
        return "None"

    # noinspection PyUnresolvedReferences
    @property
    def toughness(self):
        """
        获取韧性。

        :return: 韧性。
        """
        if not hasattr(self, "stress_trimmed") or not hasattr(self, "strains_trimmed"):
            raise ValueError("Please calibrate the strain and stress data and trim it.")
        return trapz(self.stress_trimmed, self.strains_trimmed)

    @property
    def toughness_unit(self):
        """
        获得韧性的单位。

        韧性的单位："J/m^3"或“MPa.m”

        :return: 韧性的单位。
        """
        return "J/m^3"

    @property
    def initial_volume(self):
        """
        获取测试样品的初始体积。

        :return: 测试样品的初始体积。
        """
        if self.cross_area is not None and self.clamp_distance is not None:
            return self.cross_area * self.clamp_distance
        else:
            return None

    @property
    def initial_volume_unit(self):
        """
        获取测试样品的初始体积的单位。

        :return: 测试样品的初始体积的单位。
        """
        return "mm^3"

    @property
    def breaking_work(self):
        """
        获取断裂功。

        :return: 断裂功。
        """
        if self.initial_volume is not None:
            return self.toughness * self.initial_volume * 1e-6

    @property
    def breaking_work_unit(self):
        """
        获取断裂功的单位。

        :return: 断裂功的单位。
        """
        return "J"

    # noinspection PyUnresolvedReferences
    def calibrate_yield_point(self, **kwargs):
        """
        计算屈服点。

        :param kwargs: 用到的关键字参数。
        :return: 屈服点。
        """
        is_plot = kwargs.pop("is_plot", False)
        modulus_line_stop = kwargs.pop("modulus_line_stop", None)
        yield_line_start = kwargs.pop("yield_line_start", None)
        yield_line_stop = kwargs.pop("yield_line_stop", None)
        strain_stress_line_color = kwargs.pop("strain_stress_line_color", "blue")
        modulus_line_line_color = kwargs.pop("modulus_line_line_color", "green")
        yield_line_line_color = kwargs.pop("yield_line_line_color", "orange")
        yield_point_color = kwargs.pop("hardening_point_color", "red")
        # -----------------------------------------
        initial_modulus_region = self.calibrate_initial_modulus_region()
        yield_region = self.calibrate_yield_region()
        initial_modulus_region_fit_res = initial_modulus_region.fitting_result
        yield_region_fit_res = yield_region.fitting_result
        b1, m1 = initial_modulus_region_fit_res.params
        b2, m2 = yield_region_fit_res.params
        x = (b2 - b1) / (m1 - m2)
        setattr(self, "yield_point_x", x)
        x_index = find_crossing_index(self.strains_trimmed, x)
        if x_index is None:
            raise ValueError("Can not find the yield point.")
        y = self.stress_trimmed[x_index]
        setattr(self, "yield_point_y", y)
        self.data_logger.log((x, y), "yield_point")
        # -----------------------------------------
        if is_plot:

            if modulus_line_stop is None:
                modulus_line_stop = (
                    yield_region.region_start + yield_region.region_length // 2
                )
            modulus_line_x = self.strains_trimmed[:modulus_line_stop]
            modulus_line_y = modulus_line_x * m1 + b1

            if yield_line_start is None:
                yield_line_start = (
                    initial_modulus_region.region_start
                    + initial_modulus_region.region_length // 2
                )
            if yield_line_stop is None:
                yield_line_stop = (
                    yield_region.region_start
                    + yield_region.region_length
                    + (
                        yield_region.data_len
                        - yield_region.region_start
                        - yield_region.region_length
                    )
                    // 2
                )
            yield_line_x = self.strains_trimmed[yield_line_start:yield_line_stop]
            yield_line_y = yield_line_x * m2 + b2
            plt.plot(
                self.strains_trimmed,
                self.stress_trimmed,
                color=strain_stress_line_color,
                label="Strain~Stress",
            )
            plt.plot(
                modulus_line_x,
                modulus_line_y,
                color=modulus_line_line_color,
                label="Modulus Line",
            )
            plt.plot(
                yield_line_x,
                yield_line_y,
                color=yield_line_line_color,
                label="Yield Line",
            )
            plt.scatter(x, y, color=yield_point_color, label="Yield Point")
            plt.suptitle(f"Calibrate Yield Point [{self.sample_name}]")
            plt.xlabel("Strain")
            plt.ylabel(f"Stress {self.stress_unit}")
            plt.legend(loc="best")
            plt.show()
        return x, y

    # noinspection PyUnresolvedReferences
    def calibrate_hardening_point(self, **kwargs):
        """
        计算硬化点。

        :param kwargs: 用到的关键字参数。
        :return: 硬化点。
        """
        is_plot = kwargs.pop("is_plot", False)
        yield_line_stop = kwargs.pop("yield_line_stop", None)
        strain_stress_line_color = kwargs.pop("strain_stress_line_color", "blue")
        yield_line_line_color = kwargs.pop("yield_line_line_color", "orange")
        hardening_point_color = kwargs.pop("hardening_point_color", "red")
        # -----------------------------------------
        yield_region = self.calibrate_yield_region()
        hardening_point_x = yield_region.region_data_x[-1]
        hardening_point_y = yield_region.region_data_y[-1]
        # -----------------------------------------
        setattr(self, "hardening_point_x", hardening_point_x)
        setattr(self, "hardening_point_y", hardening_point_y)
        self.data_logger.log((hardening_point_x, hardening_point_y), "hardening_point")
        # -----------------------------------------
        if is_plot:
            # 绘图时显示中文。
            plt.rcParams["font.family"] = "SimHei"
            plt.rcParams["axes.unicode_minus"] = False
            yield_region_fit_res = yield_region.fitting_result
            b2, m2 = yield_region_fit_res.params
            yield_line_start = yield_region.region_start
            if yield_line_stop is None:
                yield_line_stop = (
                    yield_region.region_start
                    + yield_region.region_length
                    + (
                        yield_region.data_len
                        - yield_region.region_start
                        - yield_region.region_length
                    )
                    // 2
                )
            yield_line_x = self.strains_trimmed[yield_line_start:yield_line_stop]
            yield_line_y = yield_line_x * m2 + b2
            plt.plot(
                self.strains_trimmed,
                self.stress_trimmed,
                color=strain_stress_line_color,
                label="Strain~Stress",
            )
            plt.plot(
                yield_line_x,
                yield_line_y,
                color=yield_line_line_color,
                label="Yield Line",
            )
            plt.scatter(
                hardening_point_x,
                hardening_point_y,
                color=hardening_point_color,
                label="Hardening Point",
            )
            plt.suptitle(f"Calibrate Hardening Point [{self.sample_name}]")
            plt.xlabel("Strain")
            plt.ylabel(f"Stress {self.stress_unit}")
            plt.legend(loc="best")
            plt.show()
        return hardening_point_x, hardening_point_y

    # 记录计算得到的数据 -----------------------------------------------------
    def logs_properties_computed(self, *property_names):
        """
        将所有计算属性更新至数据记录器。

        :param property_names: 要记录的计算属性的名字。
        """
        if not property_names:
            property_names = (
                "sampling_interval",
                "sampling_interval_unit",
                "theoretical_strain_rate",
                "theoretical_times",
                "initial_modulus",
                "initial_modulus_unit",
                "breaking_strength",
                "breaking_strength_unit",
                "breaking_elongation",
                "breaking_elongation_unit",
                "toughness",
                "toughness_unit",
                "initial_volume",
                "initial_volume_unit",
                "breaking_work",
                "breaking_work_unit",
            )
        if "sampling_interval" in property_names:
            self.data_logger.log(self.sampling_interval, "sampling_interval")
        if "sampling_interval_unit" in property_names:
            self.data_logger.log(self.sampling_interval_unit, "sampling_interval_unit")
        if "theoretical_strain_rate" in property_names:
            self.data_logger.log(
                self.theoretical_strain_rate, "theoretical_strain_rate"
            )
        if "theoretical_times" in property_names:
            self.data_logger.log(self.theoretical_times, "theoretical_times")
        if "initial_modulus" in property_names:
            self.data_logger.log(self.initial_modulus, "initial_modulus")
        if "initial_modulus_unit" in property_names:
            self.data_logger.log(self.initial_modulus_unit, "initial_modulus_unit")
        if "breaking_strength" in property_names:
            self.data_logger.log(self.breaking_strength, "breaking_strength")
        if "breaking_strength_unit" in property_names:
            self.data_logger.log(self.breaking_strength_unit, "breaking_strength_unit")
        if "breaking_elongation" in property_names:
            self.data_logger.log(self.breaking_elongation, "breaking_elongation")
        if "breaking_elongation_unit" in property_names:
            self.data_logger.log(
                self.breaking_elongation_unit, "breaking_elongation_unit"
            )
        if "toughness" in property_names:
            self.data_logger.log(self.toughness, "toughness")
        if "toughness_unit" in property_names:
            self.data_logger.log(self.toughness_unit, "toughness_unit")
        if "initial_volume" in property_names:
            self.data_logger.log(self.initial_volume, "initial_volume")
        if "initial_volume_unit" in property_names:
            self.data_logger.log(self.initial_volume_unit, "initial_volume_unit")
        if "breaking_work" in property_names:
            self.data_logger.log(self.breaking_work, "breaking_work")
        if "breaking_work_unit" in property_names:
            self.data_logger.log(self.breaking_work_unit, "breaking_work_unit")

    # ----------------------------------------------------------------------
    def summary_analysis(self, file: str):
        """
        构建数据。
        """
        self.calibrate_times()
        self.calibrate_displacements()
        self.calibrate_forces()
        self.data_trimmed()
        self.calibrate_initial_modulus_region()
        self.calibrate_yield_region()
        self.calibrate_yield_point(is_plot=True)
        self.calibrate_hardening_point(is_plot=True)
        self.logs_properties_computed()
        self.data_logger.to_excel(file)


# ==========================================================================
