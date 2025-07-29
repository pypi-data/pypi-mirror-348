#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        cre_datalyzer_result_group.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 定义“表征`恒（常）应变速率力学数据
#                                  分析结果组`”的类。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2024/10/28     revise
# ------------------------------------------------------------------
# 导包 ==============================================================
from typing import Optional

import pandas as pd
from ..commons import list_files_with_suffix
from ..commons import DataLoggerGroup

# 声明 ==============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Defines a class that represents `the result group of 
mechanical data analyzer of constant strain rate`.
"""

__all__ = ["CreMechDataAnalysisResultGroup"]
# 定义 ==============================================================


class CreMechDataAnalysisResultGroup(DataLoggerGroup):
    """
    类`CreMechDataAnalysisResultGroup`表征"恒（常）应变速率力学数据分析结果组"。
    """

    def __init__(self, group_name: str):
        """
        类`CreMechDataAnalysisResultGroup`的初始化方法。

        :param group_name: 结果组的名称。
        """
        super(CreMechDataAnalysisResultGroup, self).__init__(group_name)

    def load(
        self,
        res_dir: str,
        file_type: Optional[str] = None,
        encoding: Optional[str] = None,
        **kwargs,
    ):
        """
        从指定目录加载数据。
        """
        if file_type is None:
            file_type = ".xlsx"
        files = list_files_with_suffix(
            suffix=file_type, path=res_dir, include_subdirs=True
        )
        for file in files:
            self.add_from_file(file, encoding=encoding, **kwargs)

    def strains_stress(self, **kwargs):
        """
        返回所有样本的应变-应力数据。

        :param kwargs: 所需的关键字参数。
        :return:所有样本的应变-应力数据。
        """
        ss_data = {}
        for result_key in self.results().keys():
            result = self.results()[result_key]
            sample_name = result.sample_name
            ss_data[sample_name + "_strain"] = result["strains_trimmed"].dropna()
            ss_data[sample_name + "_stress"] = result["stress_trimmed"].dropna()
        df = pd.DataFrame(ss_data)
        # -----------------------------------
        if kwargs.pop("is_print", False):
            print(df)

        if kwargs.pop("is_save", False):
            df.to_csv(kwargs.pop("save_file", "strains_stress.csv"))
        # ------------------------------------
        return df

    def performance_indicators(self, **kwargs):
        """
        返回所有样本的性能指标数据。

        :param kwargs: 所需的关键字参数。
        :return: 所有样本的性能指标数据。
        """
        # -----------------------------
        breaking_elongation = []
        breaking_strength = []
        breaking_work = []
        initial_modulus = []
        toughness = []
        yield_point_x = []
        yield_point_y = []
        harden_point_x = []
        harden_point_y = []
        # -----------------------------
        breaking_elongation_index = []
        breaking_strength_index = []
        breaking_work_index = []
        initial_modulus_index = []
        toughness_index = []
        yield_point_x_index = []
        yield_point_y_index = []
        harden_point_x_index = []
        harden_point_y_index = []
        # -----------------------------
        for result_key in self.results().keys():
            result = self.results()[result_key]
            sample_name = result.sample_name
            # -----------------------------
            breaking_elongation.append(result["breaking_elongation"].dropna().item())
            breaking_elongation_index.append(
                sample_name + f"({result["breaking_elongation_unit"].dropna().item()})"
            )
            # -----------------------------
            breaking_strength.append(result["breaking_strength"].dropna().item())
            breaking_strength_index.append(
                sample_name + f"({result["breaking_strength_unit"].dropna().item()})"
            )
            # -----------------------------
            breaking_work.append(result["breaking_work"].dropna().item())
            breaking_work_index.append(
                sample_name + f"({result["breaking_work_unit"].dropna().item()})"
            )
            # -----------------------------
            initial_modulus.append(result["initial_modulus"].dropna().item())
            initial_modulus_index.append(
                sample_name + f"({result["initial_modulus_unit"].dropna().item()})"
            )
            # -----------------------------
            toughness.append(result["toughness"].dropna().item())
            toughness_index.append(
                sample_name + f"({result["toughness_unit"].dropna().item()})"
            )
            # -----------------------------
            yield_point = result["yield_point"].dropna()
            yield_point_x.append(yield_point[0])
            yield_point_x_index.append(sample_name)
            yield_point_y.append(yield_point[1])
            yield_point_y_index.append(sample_name)
            # -----------------------------
            harden_point = result["hardening_point"].dropna()
            harden_point_x.append(harden_point[0])
            harden_point_x_index.append(sample_name)
            harden_point_y.append(harden_point[1])
            harden_point_y_index.append(sample_name)
            # -----------------------------
        breaking_elongation_series = pd.Series(
            breaking_elongation, index=breaking_elongation_index
        )
        breaking_strength_series = pd.Series(
            breaking_strength, index=breaking_strength_index
        )
        breaking_work_series = pd.Series(breaking_work, index=breaking_work_index)
        initial_modulus_series = pd.Series(initial_modulus, index=initial_modulus_index)
        toughness_series = pd.Series(toughness, index=toughness_index)
        yield_point_x_series = pd.Series(yield_point_x, index=yield_point_x_index)
        yield_point_y_series = pd.Series(yield_point_y, index=yield_point_y_index)
        harden_point_x_series = pd.Series(harden_point_x, index=harden_point_x_index)
        harden_point_y_series = pd.Series(harden_point_y, index=harden_point_y_index)

        df = pd.concat(
            [
                breaking_elongation_series,
                breaking_strength_series,
                breaking_work_series,
                initial_modulus_series,
                toughness_series,
                yield_point_x_series,
                yield_point_y_series,
                harden_point_x_series,
                harden_point_y_series,
            ]
        )
        # 重命名列
        df.columns = [
            "breaking_elongation",
            "breaking_strength",
            "breaking_work",
            "initial_modulus",
            "toughness",
            "yield_point_x",
            "yield_point_y",
            "harden_point_x",
            "harden_point_y",
        ]

        # -----------------------------------
        if kwargs.pop("is_print", False):
            print(df)

        if kwargs.pop("is_save", False):
            df.to_excel(kwargs.pop("save_file", "performance_indicators.csv"))
        # ------------------------------------
        return df
