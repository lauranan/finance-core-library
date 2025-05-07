import unittest
from finance_core.irr import getIRR
from finance_core.plot_npv import plot_npv_curve

class TestPlotNpv(unittest.TestCase):
    def test1(self):
        trueIRR = getIRR([-100, 20, 50, 40, -10, 5])
        result = plot_npv_curve(cashflows=[-100, 20, 50, 40, -10, 5])
        self.assertAlmostEqual(trueIRR, result.irr, places=2)
    def test_no_irr(self):
        result = plot_npv_curve([-100, -50, -30, -10])
        self.assertIsNone(result.irr)
    def test_irr_is_zero(self):
        result = plot_npv_curve([-100, 50, 50])
        self.assertIsNotNone(result.irr, "IRR returned None when it should be 0.")