import sys
import argparse
import math
from collections import namedtuple
from scipy.stats import norm

#helper type and struct
def comma_separated_list(arg: str) -> list[str]:
    return [item.stripe() for item in arg.split(',')]
greeks = namedtuple("greeks", ["price", "delta", "gamma", "vega", "theta"])


##TODO: write input check function

#Greek calculation
def black_scholes_greeks(s, k, t, sigma, r, option_type):
    #Calculate square root t
    sqrtT = math.sqrt(t)
    #Calculate d1
    d1 = (math.log(s/k) + (r + (1/2 * sigma**2) * t))/(sigma * sqrtT)
    #Calculate d2
    d2 = d1 - sigma * sqrtT
    #Calculate Norm & Phi
    norm_d1 = norm.cdf(d1)
    norm_d2 = norm.cdf(d2)
    phi_d1 = norm.pdf(d1)

    if option_type == "call":
        price = s * norm_d1 - k * math.exp(-r * t) * norm_d2
    else:
        price = s * math.exp(-r * t) * norm.cdf(-d2) - s * norm.cdf(-d1)
    
    if option_type == "call":
        delta = norm_d1
    else:
        delta = norm_d1 - 1

    gamma = phi_d1/(s * sigma * sqrtT)
    vega = s * phi_d1 *sqrtT

    if option_type == "call":
        theta = s * phi_d1 * sigma/ (2 * sqrtT) - r * k * math.exp(-r * t) * norm_d2
    else:
        theta = -s * phi_d1 * sigma / (2 * sqrtT) + r * k * math.exp(-r * t) * norm.cdf(-d2) 

    return greeks(
        price=price,
        delta=delta,
        gamma=gamma,
        vega=vega,
        theta=theta
    )



if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Not valid input") #TODO: FIX THE USAGE MESSAGE
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="parser for greek calculator"
    )

    #required argument
    parser.add_argument("-S", type=float, help="Spot price")
    parser.add_argument("-K", type=float, help="Strike")

    #optional argument
    parser.add_argument("-t", type=float, default=1.0, help="time to expiry in year, default to 1 year")
    parser.add_argument("-sigma", type=float, default=0.2, help="volume, default to 0.2")
    parser.add_argument("-r", type=float, default=0, help="risk-free rate, default to 0")
    parser.add_argument("--type", type=str, default="call", help="call/put, default to call") #can I restrict --type to take only "call" or "put"
    parser.add_argument("--plot", type=comma_separated_list, default=['delta','price'], help="list of greeks to plot, separated with ',")

    args = parser.parse_args()

    result = black_scholes_greeks(s=args.S, 
                                k=args.K, 
                                t=args.t, 
                                sigma=args.sigma, 
                                r=args.r, 
                                option_type=args.type)
    print(result)