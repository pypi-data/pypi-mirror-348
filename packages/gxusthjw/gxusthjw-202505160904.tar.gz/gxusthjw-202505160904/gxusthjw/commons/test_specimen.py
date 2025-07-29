#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from __future__ import absolute_import, print_function, division
# ------------------------------------------------------------------
# File Name:        test_specimen.py
# Author:           Jiwei Huang
# Version:          0.0.1
# Created:          2012/01/01
# Description:      测试test_specimen.py。
# History:
#        <author>        <version>        <time>        <desc>
#       Jiwei Huang        0.0.1         2012/01/01     create
#       Jiwei Huang        0.0.1         2024/10/17     finish
# -----------------------------------------------------------------
# 导包 =============================================================
import unittest
import numpy as np
import pandas as pd

from .specimen import Specimen


# 定义 =============================================================
class SpecimenImpl(Specimen):
    """
    处于测试目的，对Specimen进行简单的继承，并实现其抽象方法。
    """

    def __init__(self, **kwargs):
        super(SpecimenImpl, self).__init__(**kwargs)

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def to_dataframe(self, **kwargs):
        x = np.arange(1000)
        y = np.sin(x) + x * np.cos(x)
        z = (x + y) ** 2
        return pd.DataFrame({'x': x, 'y': y, 'z': z})


class TestSpecimen(unittest.TestCase):
    """
    测试specimen.py。
    """

    # ==============================================================
    def setUp(self):
        """
        Hook method for setting up the test fixture before exercising it.
        """
        print("\n\n-----------------------------------------------------")

    def tearDown(self):
        """
        Hook method for deconstructing the test fixture after testing it.
        """
        print("-----------------------------------------------------")

    @classmethod
    def setUpClass(cls):
        """
        Hook method for setting up class fixture before running tests in the class.
        """
        print("\n\n=======================================================")

    @classmethod
    def tearDownClass(cls):
        """
        Hook method for deconstructing the class fixture after running all tests in the class.
        """
        print("=======================================================")

    # ==============================================================

    # noinspection DuplicatedCode,PyUnresolvedReferences
    def test_init(self):
        td = SpecimenImpl()
        self.assertEqual('specimen', td.specimen_name)
        self.assertEqual(0, td.specimen_no)
        self.assertEqual('specimen_0', td.sample_name)

        td1 = SpecimenImpl(specimen_name='a')
        self.assertEqual('a', td1.specimen_name)
        self.assertEqual(0, td1.specimen_no)
        self.assertEqual('a_0', td1.sample_name)

        td2 = SpecimenImpl(specimen_no=2)
        self.assertEqual('specimen', td2.specimen_name)
        self.assertEqual(2, td2.specimen_no)
        self.assertEqual('specimen_2', td2.sample_name)

        td3 = SpecimenImpl(specimen_name='c', specimen_no=5)
        self.assertEqual('c', td3.specimen_name)
        self.assertEqual(5, td3.specimen_no)
        self.assertEqual('c_5', td3.sample_name)

        td4 = SpecimenImpl(aa=10)
        self.assertEqual(10, td4.aa)
        self.assertEqual('specimen', td4.specimen_name)
        self.assertEqual(0, td4.specimen_no)
        self.assertEqual('specimen_0', td4.sample_name)

        td5 = SpecimenImpl(specimen_name='a', aa=10)
        self.assertEqual(10, td5.aa)
        self.assertEqual('a', td5.specimen_name)
        self.assertEqual(0, td5.specimen_no)
        self.assertEqual('a_0', td5.sample_name)

        td6 = SpecimenImpl(specimen_no=2, aa=10)
        self.assertEqual(10, td6.aa)
        self.assertEqual('specimen', td6.specimen_name)
        self.assertEqual(2, td6.specimen_no)
        self.assertEqual('specimen_2', td6.sample_name)

        td7 = SpecimenImpl(specimen_name='c', specimen_no=5, aa=10)
        self.assertEqual(10, td7.aa)
        self.assertEqual('c', td7.specimen_name)
        self.assertEqual(5, td7.specimen_no)
        self.assertEqual('c_5', td7.sample_name)


if __name__ == '__main__':
    unittest.main()
