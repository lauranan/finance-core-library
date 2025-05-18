import unittest
import numpy as np
from finance_core.option_payoff import generate_payoff_curve, compute_option_payoff

class TestOptionPayoff(unittest.TestCase):
    def test_curve(self):
        price_range = np.linspace(80, 120, 100)
        generate_payoff_curve(option_type="call", position="long", strike=100, exp_price_range=price_range, premium=10)