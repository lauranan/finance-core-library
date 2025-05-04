import sys
import ast
import numpy_financial as npf
import numpy as np
import time
from .npv import getNPV

def test_IRR():
    assert(round(irr_bisection([-1000, 300, 700, -100, 400]), 6) == round(getIRR([-1000, 300, 700, -100, 400]), 6) )
    assert(round(irr_newton_raphson(cash_flows=[-1000, 300, 700, 100, 400], rate=0.193), 6) == round(getIRR([-1000, 300, 700, 100, 400]), 6) )
def getNPVderiv(cashflows:list[float], rate:float):
    """
    Calculate the derivative for NPV against discount rate = rate.

    Parameters:
        cash_flows (list of float): A list of cash flows, starting with the initial investment (usually negative).
        rate: discount rate

    Returns:
        float: Estimated IRR.
    """
    if rate <= -1: # do I need to do this value check? will this scenario ever happen?
        print(f"discount rate {rate} is less than -1.")
        raise(ValueError)
    deriv = 0
    for index, cashflow in enumerate(cashflows[1:]):
        year = index + 1 #the 0th element marks the term of year1, always as 1 to the index for year
        deriv -=  year * cashflow / (1 + rate)**(year + 1) # the derivative of each year's term, summed togather to get NPV'
    return deriv

def irr_newton_raphson(cash_flows: list[float],rate:float=0.1, tol:float=1e-6, max_iter:int=1000):
    #space: O(1) time, O(n⋅k),where k=max number of iterations
    """
    Calculate the Internal Rate of Return (IRR) using Newton-Raphson method.

    Parameters:
        cash_flows (list of float): A list of cash flows, starting with the initial investment (usually negative).
        initial_guess (float): Starting point for IRR iteration.
        tol (float): Tolerance for convergence.
        max_iter (int): Maximum number of iterations.

    Returns:
        float: Estimated IRR.
    """
    start = time.time()
    for i in range(max_iter): #bounding max iteration    
        try:
            NPV = getNPV(cash_flows, rate) 
        except:
            raise ValueError(f"Rate exploded out of bounds: {rate_next}")
        if abs(NPV) < tol: #if NPV deviate from 0 in a tolerable range, return the rate
            end = time.time()
            print(f"time used is {end-start:.8f}")
            return rate
        #if NPV within tolerance, return current rate as IRR.
        NPV_deriv = getNPVderiv(cash_flows, rate) 
        '''
        if NPV_deriv == 0: #if the derivative yields 0, we are falling into a plain or pit, not converging toward either direction
                raise ZeroDivisionError("Derivative is zero. No convergence.")
        '''
        try:
            rate_next = rate - NPV/NPV_deriv #use N-R formula to calculate next rate guess.
        except:
            raise ZeroDivisionError("Derivative is zero. No convergence.")
        print(f"Iteration {i}: rate = {rate:.8f}, NPV = {NPV:.8f}, NPV_deriv = {NPV_deriv:.8f}, next rate = {rate_next:.8f}")
        if abs(rate_next - rate) < tol: #if step is below tolerance, then we met convergence condition
            end = time.time()
            print(f"time used is {end-start:.8f}")
            return rate_next
        '''
        if not -0.99 < rate_next < 1e6:  # avoid divergence
            raise ValueError(f"Rate exploded out of bounds: {rate_next}")
        '''
        rate = rate_next

def irr_bisection(cash_flows, tol=1e-6, max_iter=1000):
    #Space:O(1), time: O(n × log₂((high - low) / tol))
    # cash_flows: list of cash flows starting from time 0
    # tol: acceptable error margin for NPV close to 0 (e.g., $0.000001)
    # max_iter: maximum number of iterations to prevent infinite loops
    low, high = -0.9999, 1.0 
    # Initial bounds for the IRR search. IRR must lie between this value.
    if getNPV(cash_flows, low) * getNPV(cash_flows, high) > 0:
        print(f"low is {getNPV(cash_flows, low):.8f}, hight is {getNPV(cash_flows, high):.8f}")
        raise ValueError("IRR not bracketed in [low, high] — no sign change detected.")
    for i in range(max_iter):
        mid = (low + high)/2
        npv_mid = getNPV(cash_flows, mid)

        if abs(npv_mid) < tol:
            return mid
        elif npv_mid > 0:
            low = mid
        else:
            high = mid 

    raise ValueError("IRR not found within iteration limit")


def getIRR(cash_flows):
    irr = npf.irr(cash_flows)
    if np.isnan(irr):
        raise ValueError("IRR calculation failed: No real solution")
    else: 
        return npf.irr(cash_flows)

def main():
    if len(sys.argv) < 2:
        print("Usage: python irr.py list<cash_flows>")
        sys.exit(1)

    # Parse inputs from command line
    

    #get cash_flows as a list
    try: 
        cash_flows = ast.literal_eval(sys.argv[1])
       
        if not isinstance(cash_flows, list) or not all(isinstance(x, (int, float)) for x in cash_flows):
            raise ValueError
    except Exception:
        print("Format error: cash flows must be a list of numbers, e.g. [100, 200, 300]")
        sys.exit(1)
    
   
    # Call IRR function
    try:
        result = getIRR(cash_flows)
    except ValueError as e:
        print(e)
        sys.exit(1)

    # Print the result
    print(f"IRR: {result:.6f}")

if __name__ == "__main__":
    test_IRR()
    main()