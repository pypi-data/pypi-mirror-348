#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        __init__.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      gxusthjw.findpeaks包的__init__.py。
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/10/30     revise
#       Jiwei Huang        0.0.1         2024/06/28     finish
# ----------------------------------------------------------------
# 导包 ==============================================================
from .ampd_algorithm import ampd

# ===================================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Automatic multiscale-based peak detection (AMPD) algorithm.
"""

__all__ = [
    'ampd',
]
# ==================================================================
