#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        __init__.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      gxusthjw.statistics包的__init__.py。
#                   承载“统计学”相关的类和函数。
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/30     revise
#       Jiwei Huang        0.0.1         2024/08/20     revise
#       Jiwei Huang        0.0.1         2024/09/03     revise
#       Jiwei Huang        0.0.1         2024/10/18     revise
# ----------------------------------------------------------------
# 导包 ============================================================
from .residuals_analysis import Residuals
from .fitting_statistics import (
    rsquared,
    chisqr,
    chisqr_p,
    redchi,
    aic,
    bic,
    FittingStatistics
)

from .finite_normal_distribution import (
    finite_norm_pdf,
    finite_norm_cdf_od,
    finite_norm_cdf,
    FiniteNormalDistribution,
    finite_norm
)

# 声明 ============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Assembling classes and functions associated with `statistics`.
"""

__all__ = [
    'Residuals',
    'rsquared',
    'chisqr',
    'chisqr_p',
    'redchi',
    'aic',
    'bic',
    'FittingStatistics',
    'finite_norm_pdf',
    'finite_norm_cdf_od',
    'finite_norm_cdf',
    'FiniteNormalDistribution',
    'finite_norm',
]
# ==================================================================
