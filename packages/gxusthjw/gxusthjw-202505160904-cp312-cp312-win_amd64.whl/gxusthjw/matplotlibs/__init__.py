#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        __init__.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: gxusthjw.matplotlibs包的__init__.py。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2024/09/08     revise
#       Jiwei Huang        0.0.1         2024/09/10     revise
#       Jiwei Huang        0.0.1         2024/10/15     revise
# ----------------------------------------------------------------
# 导包 ============================================================
from .custom_slider import SliderTextBox
from .matplotlib_utils import (
    import_mpl,
    create_mpl_ax,
    create_mpl_fig
)

# 声明 ============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Assembling the classes and functions associated with `matplotlib`.
"""

__all__ = [
    'SliderTextBox',
    'import_mpl',
    'create_mpl_ax',
    'create_mpl_fig',
]
# 定义 ============================================================
