#!/usr/bin/env python3
# --*-- coding: utf-8 --*--
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        bruker_nmr.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      Main Function: 用于处理bruker的NMR数据。
#                   Outer Parameters: xxxxxxx
# Class List:       xxxxxxx
# Function List:    xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
#                   xxx() -- xxxxxxx
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2023/11/05     revise
#       Jiwei Huang        0.0.1         2023/12/17     revise
#       Jiwei Huang        0.0.1         2024/06/11     revise
#       Jiwei Huang        0.0.1         2025/04/21     revise
# ------------------------------------------------------------------
# 导包 ==============================================================
import os.path
import nmrglue as ng
import nmrglue.fileio.fileiobase

# 定义 ============================================================
__version__ = "0.0.1"
__author__ = "Jiwei Huang"
__doc__ = """
Processing the NMR data of the bruker.
"""
__all__ = [
    'read_bruker',
    'read_pdata_bruker',
    'ppm_data_bruker',
    'NmrBruker'
]


# ==================================================================

def read_bruker(data_base_path=".", data_folder="1",
                bin_file=None, acqus_files=None, pprog_file=None,
                shape=None, cplex=None, big=None, isfloat=None,
                read_pulseprogram=True, read_acqus=True,
                procs_files=None, read_procs=True):
    return ng.bruker.read(dir=os.path.join(data_base_path, data_folder),
                          bin_file=bin_file, acqus_files=acqus_files,
                          pprog_file=pprog_file, shape=shape, cplex=cplex,
                          big=big, isfloat=isfloat, read_pulseprogram=read_pulseprogram,
                          read_acqus=read_acqus, procs_files=procs_files,
                          read_procs=read_procs)


def read_pdata_bruker(data_base_path=".", pdata_folder="1\\pdata\\1",
                      bin_files=None, procs_files=None, read_procs=True,
                      acqus_files=None, read_acqus=True, scale_data=True,
                      shape=None, submatrix_shape=None, all_components=False,
                      big=None, isfloat=None):
    return ng.bruker.read_pdata(dir=os.path.join(data_base_path, pdata_folder),
                                bin_files=bin_files, procs_files=procs_files,
                                read_procs=read_procs, acqus_files=acqus_files,
                                read_acqus=read_acqus, scale_data=scale_data,
                                shape=shape, submatrix_shape=submatrix_shape,
                                all_components=all_components,
                                big=big, isfloat=isfloat)


def ppm_data_bruker(data_base_path=".", pdata_folder="1\\pdata\\1",
                    bin_files=None, procs_files=None, read_procs=True,
                    acqus_files=None, read_acqus=True, scale_data=True,
                    shape=None, submatrix_shape=None, all_components=False,
                    big=None, isfloat=None):
    # From pre-proceed data.
    dic, data = read_pdata_bruker(data_base_path=data_base_path, pdata_folder=pdata_folder,
                                  bin_files=bin_files, procs_files=procs_files,
                                  read_procs=read_procs, acqus_files=acqus_files,
                                  read_acqus=read_acqus, scale_data=scale_data,
                                  shape=shape, submatrix_shape=submatrix_shape,
                                  all_components=all_components,
                                  big=big, isfloat=isfloat)
    udic = ng.bruker.guess_udic(dic, data)
    uc = ng.fileio.fileiobase.uc_from_udic(udic)
    ppm_scale = uc.ppm_scale()
    return ppm_scale, data


class NmrBruker(object):
    def __init__(self, data_base_path=".", data_folder="1", pdata_folder="1\\pdata\\1"):
        self.__data_base_path = data_base_path
        self.__data_path = os.path.join(self.__data_base_path, data_folder)
        self.__pdata_path = os.path.join(self.__data_base_path, pdata_folder)

    @property
    def data_base_path(self):
        return self.__data_base_path

    @property
    def data_path(self):
        return self.__data_path

    @property
    def pdata_path(self):
        return self.__pdata_path

    def read_data(self, bin_file=None, acqus_files=None, pprog_file=None,
                  shape=None, cplex=None, big=None, isfloat=None,
                  read_pulseprogram=True, read_acqus=True,
                  procs_files=None, read_procs=True):
        return ng.bruker.read(self.data_path,
                              bin_file=bin_file, acqus_files=acqus_files,
                              pprog_file=pprog_file, shape=shape, cplex=cplex,
                              big=big, isfloat=isfloat,
                              read_pulseprogram=read_pulseprogram,
                              read_acqus=read_acqus, procs_files=procs_files,
                              read_procs=read_procs)

    def read_pdata(self, bin_files=None, procs_files=None, read_procs=True,
                   acqus_files=None, read_acqus=True, scale_data=True,
                   shape=None, submatrix_shape=None, all_components=False,
                   big=None, isfloat=None):
        return ng.bruker.read_pdata(self.pdata_path,
                                    bin_files=bin_files, procs_files=procs_files,
                                    read_procs=read_procs, acqus_files=acqus_files,
                                    read_acqus=read_acqus, scale_data=scale_data,
                                    shape=shape, submatrix_shape=submatrix_shape,
                                    all_components=all_components,
                                    big=big, isfloat=isfloat)

    def ppm_data(self, bin_files=None, procs_files=None, read_procs=True,
                 acqus_files=None, read_acqus=True, scale_data=True,
                 shape=None, submatrix_shape=None, all_components=False,
                 big=None, isfloat=None):
        # From pre-proceed data.
        dic, data = read_pdata_bruker(self.pdata_path,
                                      bin_files=bin_files, procs_files=procs_files,
                                      read_procs=read_procs, acqus_files=acqus_files,
                                      read_acqus=read_acqus, scale_data=scale_data,
                                      shape=shape, submatrix_shape=submatrix_shape,
                                      all_components=all_components,
                                      big=big, isfloat=isfloat)
        udic = ng.bruker.guess_udic(dic, data)
        uc = ng.fileio.fileiobase.uc_from_udic(udic)
        ppm_scale = uc.ppm_scale()
        return ppm_scale, data
