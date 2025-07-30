'''
Goal: unit test for static_graph.py
'''

import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import static_graph as SG

class TestStaticGraph(unittest.TestCase):
    def setUp(self) -> None:
        self.tst = SG.StaticGraph(filename="tgraph/tests/tiny03_loop.csv")
        self.df = self.tst.df_nodes
        self.df.set_index( SG.NODE_ID, inplace=True)

    def test_shape(self):
        n_rows = self.df.shape[0]
        n_columns = self.df.shape[1]
        self.assertEqual( n_rows, 3, "wrong # of rows")
        self.assertEqual( n_columns, 6, "wrong # of columns")

    def test_mary(self):
        mary_row = list( self.df.loc["mary"])
        self.assertEqual(mary_row, [1, 1, 2, 1, 33, 34], 'wrong Mary\'s information')

    def test_peter(self):
        peter_row = list( self.df.loc["peter"])
        self.assertEqual(peter_row, [1, 1, 2, 33, 2, 35], 'wrong Peter\'s information')

    def test_tom(self):
        tom_row = list( self.df.loc["tom"])
        self.assertEqual(tom_row, [1, 1, 2, 2, 1, 3], 'wrong Tom\'s information')


if __name__ == '__main__':

    # unittest.main()
    # the above is fine, but will give low verbosity

    # to control verbosity:
    t = unittest.TestLoader().loadTestsFromTestCase(TestStaticGraph)
    unittest.TextTestRunner(verbosity=2).run(t)
