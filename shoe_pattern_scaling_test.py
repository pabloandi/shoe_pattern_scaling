#!/usr/bin/env python
# coding=utf-8
"""
Test elements extra logic from svg xml lxml custom classes.
"""

from inkex.tester import TestCase
from inkex.tester.inx import InxMixin

from shoe_pattern_scaling import ShoePatternScalingExtension

import sys
sys.path.insert(0, '.')

class ShoePatternScalingTestCase(InxMixin, TestCase):
    """Test INX files and other things"""
    def test_inx_file(self):
        """Get all inx files and test each of them"""
        self.assertInxIsGood("shoe_pattern_scaling.inx")

    def test_other_things(self):
        """Things work out"""
        pass

class ShoePatternScalingComparisonsTestCase(ComparisonMixin, TestCase):
    """Test input and output variations"""
    effect_class = ShoePatternScalingExtension()
    comparisons = [
        ('--my_option=True',),
        ('--my_option=False',),
    ]
