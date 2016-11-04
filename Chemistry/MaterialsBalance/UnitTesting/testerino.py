import unittest

import unittest
import sympy as sp
from Chemistry.MaterialsBalance import ControlVolume as cv
from Chemistry.MaterialsBalance import DegreesOfFreedom as dof
from Chemistry.MaterialsBalance import BalanceEquations as eqs


class UT(unittest.TestCase):
    CV_list = [[{'w': 0.0400000000000000, 'Direction': 1, 'da': 0.960000000000000, 'Total': sp.S('n1')},
                {'w': 1, 'Direction': -1, 'da': 0, 'Total': sp.S('n3')},
                {'w': 0.0170000000000000, 'Direction': -1, 'da': 0.983000000000000, 'Total': 100}],
               [{'w': 0.0400000000000000, 'Direction': 1, 'da': 0.960000000000000, 'Total': sp.S('n1')},
                {'w': 0.0170000000000000, 'Direction': 1, 'da': 0.983000000000000, 'Total': sp.S('n6')},
                {'w': 0.0230000000000000, 'Direction': -1, 'da': 0.977000000000000, 'Total': sp.S('n2')}],
               [{'w': 0.0230000000000000, 'Direction': 1, 'da': 0.977000000000000, 'Total': sp.S('n2')},
                {'w': 1, 'Direction': -1, 'da': 0, 'Total': sp.S('n3')},
                {'w': 0.0170000000000000, 'Direction': -1, 'da': 0.983000000000000, 'Total': sp.S('n4')}],
               [{'w': 0.0170000000000000, 'Direction': 1, 'da': 0.983000000000000, 'Total': sp.S('n4')},
                {'w': 0.0170000000000000, 'Direction': -1, 'da': 0.983000000000000, 'Total': sp.S('n6')},
                {'w': 0.0170000000000000, 'Direction': -1, 'da': 0.983000000000000, 'Total': 100}]]

    unknown_total = 5
    total_unknowns_list = [sp.S('n1'), sp.S('n2'), sp.S('n3'), sp.S('n4'), sp.S('n6')]

    def test_dof(self):
        dof_checker = []
        for cv_count in UT.CV_list:
            dof_checker.append(dof.count_unknowns(cv_count))

        self.assertEqual(dof_checker, [2, 3, 3, 2])

    def test_analysis(self):
        dof_checker = [2, 3, 3, 2]
        analysis_checker = []
        for cv_count in range(len(UT.CV_list)):
            analysis_checker.append(dof.analysis(UT.CV_list[cv_count], dof_checker[cv_count], 0))

        self.assertTrue(analysis_checker, [0, 1, 1, 0])

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
