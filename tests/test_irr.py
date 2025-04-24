import unittest
from finance_core.irr import getIRR, irr_bisection, irr_newton_raphson

class TestIRR(unittest.TestCase):
    def test1(self):
        self.assertAlmostEqual(irr_bisection([-1100, 300, 700, -100, 400]), getIRR([-1100, 300, 700, -100, 400]))

    def test2(self):
        self.assertAlmostEqual(irr_bisection([-1000, 300, 700, -100, 400]), getIRR([-1000, 300, 700, -100, 400]))
    
    def test3(self):
        self.assertAlmostEqual(irr_bisection([-1000, -500, 700, -500, 800, -550, 900]), irr_newton_raphson([-1000, -500, 700, -500, 800, -550, 900]))
    def test4(self):
        testcase = [10, -100, 100]
        self.assertAlmostEqual(irr_bisection(testcase), irr_newton_raphson(testcase))
    def test5(self):
        testcase = [100, 100, -100]
        with self.assertRaises(ValueError):  # Catch the actual error your function raises
                irr_newton_raphson(testcase)
            
if __name__ == '__main__':
    unittest.main()