#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from __future__ import absolute_import, print_function, division
# ----------------------------------------------------------------
# File Name:        __init__.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      gxusthjw.commons包的__init__.py。
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2025/05/02     revise
# ----------------------------------------------------------------
# 导包 ============================================================
from .arrays import (
    is_sorted_ascending_np,
    is_sorted_descending_np,
    is_sorted_np,
    is_sorted,
    is_sorted_ascending,
    is_sorted_descending,
    reverse,
    Ordering,
    is_equals_of,
    sort,
    find_closest_index,
    find_crossing_index,
    find_index_range,
)

from .data_2d import (
    Data2d
)

from .data_2d_region import (
    Data2dRegion
)

from .data_analyzer import (
    DataAnalyzer
)

from .data_logger import (
    DataLogger
)

from .data_logger_file import (
    DataLoggerFile
)

from .data_logger_group import (
    DataLoggerGroup
)

from .data_table import (
    DataTable
)

from .dataframes import (
    create_df_from_dict,
    create_df_from_item,
    merge_df,
    merge_dfs,
    update_df,
    updates_df,
)

from .dicts import (
    dict_to_str,
)

from .file_info import (
    encoding_of, FileInfo, info_of, module_info_of
)

from .file_object import (
    FileObject
)

from .specimen import (
    Specimen
)

from .file_path import (
    sep_file_path,
    join_file_path,
    list_files_with_suffix,
    print_files_and_folders,
    list_files_and_folders,
    get_this_path,
    get_project_path,
    get_root_path
)

from .file_reader import (
    read_txt,
)
from .typings import (
    Number,
    NumberArrayLike,
    NumberSequence,
    Numbers,
    Numeric,
    NumberNDArray,
    is_number,
    is_number_array_like,
    is_number_sequence,
    is_numbers,
    is_numeric,
    is_number_ndarray,
    is_number_1darray,
)

from .unique_object import (
    UniqueIdentifierObject,
    unique_string,
    random_string,
    date_string,
)

# 声明 ============================================================
__version__ = "0.0.1"

__author__ = "Jiwei Huang"

__doc__ = """
Assembling the common classes and functions 
of the `gxusthjw` python packages.
"""

__all__ = [
    # ----------------------------------------------------------
    'is_sorted_ascending_np',
    'is_sorted_descending_np',
    'is_sorted_np',
    'is_sorted',
    'is_sorted_ascending',
    'is_sorted_descending',
    'reverse',
    'is_equals_of',
    'Ordering',
    'sort',
    'find_closest_index',
    'find_crossing_index',
    'find_index_range',
    # ----------------------------------------------------------
    'Data2d',
    # ----------------------------------------------------------
    'Data2dRegion',
    # ----------------------------------------------------------
    'DataAnalyzer',
    # ----------------------------------------------------------
    'DataLogger',
    # ----------------------------------------------------------
    'DataLoggerFile',
    # ----------------------------------------------------------
    'DataLoggerGroup',
    # ----------------------------------------------------------
    'DataTable',
    # ----------------------------------------------------------
    'create_df_from_dict',
    'create_df_from_item',
    'merge_df',
    'merge_dfs',
    'update_df',
    'updates_df',
    # ----------------------------------------------------------
    'dict_to_str',
    # ----------------------------------------------------------
    'encoding_of',
    'FileInfo',
    'info_of',
    'module_info_of',
    # ----------------------------------------------------------
    'FileObject',
    # ----------------------------------------------------------
    'Specimen',
    # ----------------------------------------------------------
    'sep_file_path',
    'join_file_path',
    'list_files_and_folders',
    'print_files_and_folders',
    'list_files_with_suffix',
    'get_root_path',
    'get_project_path',
    'get_this_path',
    # ----------------------------------------------------------
    'read_txt',
    # ----------------------------------------------------------
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
    # ----------------------------------------------------------
    'random_string',
    'unique_string',
    'date_string',
    'UniqueIdentifierObject',
    # ----------------------------------------------------------

]
# 定义 ============================================================
