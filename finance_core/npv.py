import sys
import ast
import numpy_financial as npf
import argparse

def test_npv():
    assert round(getNPV([-1000, 400, 500, 600], 0.10), 2) == 227.65
    assert round(getNPV([-1000, 400, 500, 600], 0.15), 2) == 120.41
    assert round(npf_getNPV([-1000, 400, 500, 600], 0.10), 2) == 227.65
    assert round(npf_getNPV([-1000, 400, 500, 600], 0.15), 2) == 120.41

def _getNPV(initial_investment: float, cash_flows: list[float], rate:float) -> float:
    NPV = -initial_investment
    for index, cash_flow in enumerate(cash_flows):
        NPV += cash_flow / (1 + rate) ** (index + 1) # year = index + 1
    return NPV

def getNPV(cash_flows: list[float], rate:float) -> float:
    NPV = 0
    for index, cash_flow in enumerate(cash_flows):
        NPV += cash_flow / (1 + rate) ** index
    return NPV

def npf_getNPV(cash_flows: list[float], rate:float) -> float:
    NPV = npf.npv(rate, cash_flows)
    return NPV


def parse_percentage(percent_str):

    if percent_str.endswith('%'):
        return float(percent_str[:-1])/100
    return float(percent_str) / 100 if float(percent_str) > 1 else float(percent_str)

def main():
    if len(sys.argv) < 2:
        print("Usage: python npv.py <cash_flows_comma_separated> <rate>")
        sys.exit(1)

    
    parser = argparse.ArgumentParser()
    parser.add_argument("cashflows", nargs="+", type=float, help="List of cashflows, e.g. -100 100 200 300")
    parser.add_argument("rate", type=parse_percentage, help="Discount rate as a decimal, e.g. 0.1")

    args = parser.parse_args()


    #get rate
    try:
        rate = parse_percentage(sys.argv[2])
    except Exception:
        print("Format error: rate should be a percentage number, e.g. 15%, 0.15")
        sys.exit(1)
    
    # Call NPV function
    result = getNPV(args.cashflows, args.rate)

    # Print the result
    print(f"NPV: {result:.2f}")

if __name__ == "__main__":
    test_npv()
    main()