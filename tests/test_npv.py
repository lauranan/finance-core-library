import unittest
from finance_core.npv import _getNPV as getNPV

class TestDCF(unittest.TestCase):
    def test1(self):
        initial_investment = 1000
        cash_flows = [400, 500, 600]
        discount_rate = 0.10
        result = getNPV(initial_investment, cash_flows, discount_rate)
        expected = -initial_investment + sum([cf / (1 + discount_rate)**i for i, cf in enumerate(cash_flows, start=1)])
        self.assertAlmostEqual(result, expected, places=2)
    def test2(self):
        initial_investment = 2000
        cash_flows = [800, 900, 1000]
        discount_rate = 0.12
        result = getNPV(initial_investment, cash_flows, discount_rate)
        expected = -initial_investment + sum([cf / (1 + discount_rate)**i for i, cf in enumerate(cash_flows, start=1)])
        self.assertAlmostEqual(result, expected, places=2)
if __name__ == '__main__':
    unittest.main()