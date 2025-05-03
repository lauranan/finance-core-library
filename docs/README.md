# Finance Core Library

This is a lightweight core finance library for computing common financial metrics like Net Present Value (NPV) and Internal Rate of Return (IRR). The goal is to build a solid foundation for financial computation with test coverage, modularity, and educational clarity.

## Features

- `getNPV(cashflows, discount_rate)`: Computes Net Present Value.
- `getIRR(cashflows)`: Estimates Internal Rate of Return using numerical methods.
- `plot_npv_curve(cashflow, OPTIONAL)`: Plots NPV curve using matplot, optional arguments available.
- Modular design with testable components.

## Structure

- `finance-core/`: Core logic for IRR, NPV, and more
  - `irr.py`: defines internal rate of return methods, one via numpy_finance, one via bisection. 
  - `npv.py`: defines net present value methods, one via formula calculation, one via numpy_finance.
  - `plot_npv.py`: defines npv plotting method.
- `tests/`: Unit tests for validating financial functions
  - `test_irr.py`: unittest for irr.py
  - `test_npv.py`: unittest for npv.py
  - `test_plot_npv.py`: unittest for plot_npv.py
- `docs/`: Project documentation and finance notes
  - `README.md`: this file.


## Getting Started
To set up dependency, use:
pip install -r requirements.txt
To run tests, from root directory finance-core-library use:
python -m unittest tests/test_<module>.py
To run functions, use:
python -m finance_core.<module> <input>

## Author

Laura Nan - Work in Progress. This repository accompanies a structured learning journey toward mastering Quantitative Finance.
