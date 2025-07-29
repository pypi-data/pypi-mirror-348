#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        file_reader.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      定义“读取文件”相关的类和方法。
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2025/05/02     revise
# ------------------------------------------------------------------
# 导包 ==============================================================
from typing import (
    Optional, Mapping, Dict, List, Union
)

import numpy as np
import pandas as pd

from .file_info import (
    FileInfo,
    encoding_of
)

from .data_table import (
    DataTable,
)

# 声明 ==============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Define classes and functions related to "reading files".
"""

__all__ = ['read_txt']


# 定义 ==============================================================
def read_txt(file: Union[str, FileInfo],
             sep: Optional[str] = None,
             skiprows: int = 0,
             cols: Optional[Mapping[int, Optional[str]]] = None,
             res_type: Optional[str] = None,
             encoding: Optional[str] = None):
    """
    基于文本文件对象的readline方法，读取文本文件中的数据。

    :param file: 数据文件的完整路径。
    :param sep: 数据间的分隔符，如果为None，则以空白符为分割符。
    :param skiprows: 跳过的行数，默认为0。
    :param cols: 指定要读取的列。
    :param res_type: 返回值形式，可指定的值分别为：

                     1. 如果为忽略大小写的”dict“，则返回字典对象，其中值为numpy.ndarray，
                        键名与cols指定的相同。

                     2. 如果为忽略大小写的”list“，则返回list对象，其中每列为list对象,
                        列的顺序与cols指定的顺序相同。

                     3. 如果为忽略大小写的”list_numpy“，则返回list对象，其中每列为numpy.ndarray,
                        列的顺序与cols指定的顺序相同。

                    4.如果为忽略大小写的”data_frame“，则返回pandas.DataFrame对象，
                        列名与cols指定的相同。

                     5. 其他值，均返回DataCapsule对象。

    :param encoding: 文件编码，如果文件编码未知，则利用chardet尝试解析，
                        如果未能解析出文件的编码，则以“GBK”读取文件。
    :return: 读取到的值。
    """
    if isinstance(file, FileInfo):
        if encoding is None:
            encoding = file.encoding
        file = file.full_path

    # 尝试解析文件的编码。
    if encoding is None:
        encoding = encoding_of(file)

    # 如果文件编码还是未知，则使用“GBK”。
    if encoding is None:
        encoding = "GBK"

    # 用于存储读取到的数据,每列数由独立的list对象保存，
    # 每列数据均有一个名字，作为字典的键。
    data_dict: Dict[str, List] = {}

    # 要读取数据的列号（列号从0开始）和对应的列名。
    index_col_name_dict: Dict[int, Optional[str]] = {}

    # confirm_on_read表示读取时确定，
    # 用于指示data_dict和index_col_name_dict的构建时机。
    confirm_on_read = False
    if (cols is None) or (len(cols) == 0):
        confirm_on_read = True
    else:
        for col_index in cols.keys():
            col_name = cols[col_index]
            if col_name is not None:
                data_dict["{}".format(col_name)] = list()
            else:
                col_name = "col_{}".format(col_index)
                data_dict[col_name] = list()
            index_col_name_dict[col_index] = col_name

    with open(file, mode='r', encoding=encoding) as f:
        # 跳过指定的行数。
        skiprows = int(skiprows)
        while skiprows != 0:
            f.readline()
            skiprows -= 1
        # 开始读取数据。
        for line in f:

            # 这里的判断是为了防止空行。
            if line.isspace():
                continue

            # 如果不是空行，则将其分割。
            value_str_array = line.strip().split(sep)
            # print(value_str_array)

            # 如果没有指定要读取的列，则读取所有列，列名为：‘col_i’,其中i为列号。
            if confirm_on_read:
                cols_index = range(len(value_str_array))
                # print(cols_index)
                for index in cols_index:
                    col_name = "col_{}".format(index)
                    index_col_name_dict[index] = col_name
                    data_dict[col_name] = list()
                confirm_on_read = False

            # 如果len(value_str_array) <= max(col_index)，则可能抛出异常。
            # 但考虑到效率问题，这里不做检查。
            for col_index in index_col_name_dict.keys():
                # print(value_str_array[col_index])
                value = float(value_str_array[col_index].strip())
                data_dict[index_col_name_dict[col_index]].append(value)

        if isinstance(res_type, str) and res_type.lower() == "dict":
            return data_dict
        elif isinstance(res_type, str) and res_type.lower() == "list":
            res_list = list()
            for col_index in index_col_name_dict.keys():
                res_list.append(data_dict[index_col_name_dict[col_index]])
            return res_list
        elif isinstance(res_type, str) and res_type.lower() == "list_numpy":
            res_list = list()
            for col_index in index_col_name_dict.keys():
                res_list.append(np.array(data_dict[index_col_name_dict[col_index]], copy=True))
            return res_list
        elif isinstance(res_type, str) and res_type.lower() == "data_frame":
            return pd.DataFrame(data_dict)
        else:
            res_list = list()
            for col_index in index_col_name_dict.keys():
                res_list.append(data_dict[index_col_name_dict[col_index]])
            return DataTable(*res_list, col_names=index_col_name_dict)
