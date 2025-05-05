import unittest
from finance_core.irr import getIRR
from finance_core.plot_npv import plot_npv_curve

class TestPlotNpv(unittest.TestCase):
    def test1(self):
        trueIRR = getIRR([-100, 20, 50, 40, -10, 5])
        testIRR, _ = plot_npv_curve(cashflows=[-100, 20, 50, 40, -10, 5], return_irr=True)
        self.assertAlmostEqual(trueIRR, testIRR, places=2)
    def test_no_irr(self):
        result, _ = plot_npv_curve([-100, -50, -30, -10], return_irr=True)
        self.assertIsNone(result)
    def test_irr_is_zero(self):
        result1, _ = plot_npv_curve([-100, 50, 50], return_irr=True)
        self.assertIsNotNone(result1, "IRR returned None when it should be 0.")