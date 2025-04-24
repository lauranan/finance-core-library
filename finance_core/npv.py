import sys
import ast
import numpy_financial as npf

def test_npv():
    assert round(getNPV([-1000, 400, 500, 600], 0.10), 2) == 227.65
    assert round(getNPV([-1000, 400, 500, 600], 0.15), 2) == 120.41
    assert round(npf_getNPV(1000, [400, 500, 600], 0.10), 2) == 227.65
    assert round(npf_getNPV(1000, [400, 500, 600], 0.15), 2) == 120.41

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

def npf_getNPV(initial_investment: float, cash_flows: list[float], rate:float) -> float:
    NPV = npf.npv(rate, [-initial_investment] + cash_flows)
    return NPV


def parse_percentage(percent_str):

    if percent_str.endswith('%'):
        return float(percent_str[:-1])/100
    return float(percent_str) / 100 if float(percent_str) > 1 else float(percent_str)

def main():
    if len(sys.argv) < 4:
        print("Usage: python npv_calculator.py <initial_investment> <cash_flows_comma_separated> <rate>")
        sys.exit(1)

    # Parse inputs from command line
    
    try:
        initial_investment = float(sys.argv[1])
    except Exception:
        print("format error: initial investment must be a number.")
        sys.exit(1)

    #get cash_flows as a list
    try:
        cash_flows = ast.literal_eval(sys.argv[2])
        if not isinstance(cash_flows, list) or not all(isinstance(x, (int, float)) for x in cash_flows):
            raise ValueError
    except Exception:
        print("Format error: cash flows must be a list of numbers, e.g. [100, 200, 300]")
        sys.exit(1)
    
    #get rate
    try:
        rate = parse_percentage(sys.argv[3])
    except Exception:
        print("Format error: rate should be a percentage number, e.g. 15%, 0.15")
        sys.exit(1)
    
    # Call NPV function
    result = getNPV([-initial_investment] + cash_flows, rate)

    # Print the result
    print(f"NPV: {result:.2f}")

if __name__ == "__main__":
    test_npv()
    main()