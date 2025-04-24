# Finance Core Library

This is a lightweight core finance library for computing common financial metrics like Net Present Value (NPV) and Internal Rate of Return (IRR). The goal is to build a solid foundation for financial computation with test coverage, modularity, and educational clarity.

## Features

- `getNPV(cashflows, discount_rate)`: Computes Net Present Value.
- `getIRR(cashflows)`: Estimates Internal Rate of Return using numerical methods.
- Modular design with testable components.

## Structure

- `finance-core/`: Core logic for IRR, NPV, and more
  - `irr.py`: defines internal rate of return methods, one via numpy_finance, one via bisection. 
  - `npv.py`: defines net present value methods, one via formula calculation, one via numpy_finance.
- `tests/`: Unit tests for validating financial functions
  - `irr_test.py`: unittest for irr.py
  - `npv_test.py`: unittest for npv.py
- `docs/`: Project documentation and finance notes
  - `README.md`: this file.


## Getting Started
To run tests, use:
python -m unittest tests/test_<module>.py
To run functions, use:
python -m finance_core.<module> <input>

## Author

Laura Nan - Work in Progress. This repository accompanies a structured learning journey toward mastering Quantitative Finance.
