import argparse
from matplotlib import pyplot as plt
import numpy as np
from typing import Iterable

def net_call_payoff(strike:float, exp_price:float, premium:float):
    return max(0, exp_price - strike) - premium
def net_put_payoff(strike:float, exp_price:float, premium:float):
    return max(0, strike - exp_price) - premium

###########################
## COMPUTE OPTION PAYOFF ##
###########################
def premium_positive_float(value):
    fval = float(value)
    if fval <= 0:
        raise argparse.ArgumentTypeError("Premium must be a positive number.")
    return fval
def compute_option_payoff(option_type:str, position:str, strike:float, exp_price:float, premium:float=0): 
    pay_off = None
    if option_type == "call":
        pay_off = net_call_payoff(strike, exp_price, premium) if position == "long" else -net_call_payoff(strike, exp_price, premium)
    elif option_type == "put":
        pay_off = net_put_payoff(strike, exp_price, premium) if position == "long" else -net_put_payoff(strike, exp_price, premium)

    if pay_off == 0:
        label = "Break-even"
    elif pay_off > 0:
        label = "Profit"
    else:
        label = "Loss"
    
    return pay_off, label

#############################
## PAYOFF CURVE GENERATION ##
#############################
def generate_payoff_curve(option_type:str, position:str, strike:float, exp_price_range:Iterable[float], premium:float=0)-> None:
    pay_offs = []
    for exp_price in exp_price_range:
        pay_off, _ = compute_option_payoff(option_type=option_type, position=position, strike=strike, exp_price=exp_price, premium=premium)
        pay_offs.append(pay_off)
    plt.plot(exp_price_range, pay_offs, label="Payoff Curve", color="blue")
    plt.title("Payoff vs. End Price")
    plt.xlabel("End Price")
    plt.ylabel("Payoff ($)")
    plt.axvline(x=strike, color='gray', linestyle="--", label=f"Strike = {strike:.1f}")
    plt.axhline(y=0, color='green', linestyle="dashdot", label=f"Break-even")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(
        description = "parser for option-payoff"
    )

    # required arguments
    parser.add_argument("--type", type=str, required=True, choices=["call", "put"], help="type of option, put or call")
    parser.add_argument("--position", type=str, required=True, choices=["long", "short"], help="type of position, short or long")
    parser.add_argument("--strike", type=float, required=True, help="strike price, default None")
    parser.add_argument("--price_at_expiry", type=float, required=True, help="stock price at expiration time, default None")
    
    # optional flags
    parser.add_argument("--premium", type=premium_positive_float, default=None, help="enable for premium inclusion for payoff calculation, input positive number for premium. i.e., --include_premium 5")

    #parse
    args = parser.parse_args()

    #compute payoff and label
    payoff, label = compute_option_payoff(
        option_type=args.type,
        position=args.position,
        strike=args.strike,
        exp_price=args.price_at_expiry,
        premium=args.premium if args.premium is not None else 0
    )
    print(f"[{args.position.capitalize()} {args.type.capitalize()}] Payoff: ${payoff:.2f} → {label}")

if __name__ == "__main__":
    main()