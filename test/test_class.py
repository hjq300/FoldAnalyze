# content for test_class.py

import sys
sys.path.append('..')

from FoldAnalyze import FoldAnalyze

class TestClass:
    def test_01(self):
        x = 'test'
        assert 't' in x
    def test_02(self):
        a = FoldAnalyze.FoldAnalyze()
        assert 'Bytes' in a.humanSizeString(2)
