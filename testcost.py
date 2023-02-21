import unittest
from costapp import find_row_and_column

class TestFind(unittest.TestCase):
    
    def test_find_row_and_column(self):
        # call the function with the desired input values
        row, col, cost = find_row_and_column(1150, 2.5)
        
        # check the results

        print(f"Row: {row}")
        print(f"Col: {col}")
        print(f"Cost: {cost}")
        self.assertIsNotNone(row)
        self.assertIsNotNone(col)
        self.assertIsNotNone(cost)
        
        self.assertEqual(row, 3)
        self.assertEqual(col, '1100-1199')
        
        self.assertAlmostEqual(cost, 257565.5, delta=1e-2)

if __name__ == '__main__':
    unittest.main()
