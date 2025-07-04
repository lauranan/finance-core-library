import sys
import argparse
import math
from collections import namedtuple
from scipy.stats import norm
import numpy as np
from matplotlib import pyplot as plt

#helper type and struct
def comma_separated_list(arg: str) -> list[str]:
    return [item.strip() for item in arg.split(',')]
greeks = namedtuple("greeks", ["price", "delta", "gamma", "vega", "theta"])


##TODO: write input check function

#Greek calculation
def black_scholes_greeks(s, k, t, sigma, r, option_type):
    #Calculate square root t
    sqrtT = math.sqrt(t)
    #Calculate d1
    d1 = (math.log(s/k) + ((r + 1/2 * sigma**2) * t))/(sigma * sqrtT)
    #Calculate d2
    d2 = d1 - sigma * sqrtT
    #Calculate Norm & Phi
    norm_d1 = norm.cdf(d1)
    norm_d2 = norm.cdf(d2)
    phi_d1 = norm.pdf(d1)

    if option_type == "call":
        price = s * norm_d1 - k * np.exp(-r * t) * norm_d2
        delta = norm_d1
        theta = -(s * phi_d1 * sigma) / (2 * sqrtT) - r * k * np.exp(-r * t) * norm_d2
    else:  # put
        price = k * np.exp(-r * t) * norm.cdf(-d2) - s * norm.cdf(-d1)
        delta = norm_d1 - 1
        theta = -(s * phi_d1 * sigma) / (2 * sqrtT) + r * k * np.exp(-r * t) * norm.cdf(-d2)

    gamma = phi_d1 / (s * sigma * sqrtT)
    vega  = s * phi_d1 * sqrtT

    return greeks(
        price=price,
        delta=delta,
        gamma=gamma,
        vega=vega,
        theta=theta
    )

#Plot curve
def plot_curve(args):

    #get plot spts
    center = args.S
    span = 0.5 * max(args.K, args.S)
    s_min = max(0, center - span)
    s_max = center + span
    spots = np.arange(s_min, s_max + args.step, args.step)

    dataset = []

    for spot in spots:
        result = black_scholes_greeks(s=spot, 
                                k=args.K, 
                                t=args.t, 
                                sigma=args.sigma, 
                                r=args.r, 
                                option_type=args.type)
        dataset.append(result)

    price = [data.price for data in dataset]
    delta = [data.delta for data in dataset]
    gamma = [data.gamma for data in dataset]
    vega = [data.vega for data in dataset]
    theta = [data.theta for data in dataset]

    fig, ax_price = plt.subplots()
    ax_price.set_xlabel("Spot price")
    ax_price.set_title(f"{args.type.capitalize()} option (K={args.K}, T={args.t}y, σ={args.sigma}, r={args.r})")
    
    #plot price
    ax_price.plot(spots, price, label="Price", color="black")
    ax_price.set_ylabel("Option price", color="black")


    #plot greeks
    greek_map = {
        "delta": (delta, "blue"),
        "gamma": (gamma, "green"),
        "vega":  (vega,  "red"),
        "theta": (theta, "purple"),
    }
    for greek_name in args.plot:
        if greek_name == "price":
            continue
        data, col = greek_map[greek_name]
        ax_greek = ax_price.twinx()
        ax_greek.plot(spots, data, label=greek_name.capitalize(), color=col, linestyle="--")
        ax_greek.set_ylabel(greek_name.capitalize(), color=col)
        ax_greek.tick_params(axis='y', labelcolor=col)
        ax_greek.spines.right.set_position(("axes", 1 + 0.08 * (args.plot.index(greek_name)-1)))
    if args.save_path:
        try:
            plt.savefig(args.save_path)
        except:
            print(f"the path: {args.save_path} is invalid, unable to save, please recheck.")
        plt.close()
    else:
        plt.show()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="parser for greek calculator"
    )

    #required argument
    parser.add_argument("-S", type=float, required=True, help="Spot price")
    parser.add_argument("-K", type=float, required=True, help="Strike")

    #optional argument
    parser.add_argument("-t", type=float, default=1.0, help="time to expiry in year, default to 1 year")
    parser.add_argument("-sigma", type=float, default=0.2, help="volatility, default to 0.2")
    parser.add_argument("-r", type=float, default=0, help="risk-free rate, default to 0")
    parser.add_argument("--type", type=str, default="call", choices=["call", "put"], help="call/put, default to call") #can I restrict --type to take only "call" or "put"
    parser.add_argument("--plot", type=comma_separated_list, default=['delta','price'], help="list of greeks to plot, separated with ',")

    #optional plot argument
    parser.add_argument("--step", type=float, default=1.0, help="spot-grid step size (default 1)")
    parser.add_argument("--save_path", type=str, default=None, help="save the plot to path, default None")

    args = parser.parse_args()

    result = black_scholes_greeks(s=args.S, 
                                k=args.K, 
                                t=args.t, 
                                sigma=args.sigma, 
                                r=args.r, 
                                option_type=args.type)
    print(f"Price : {result.price:.4e}")
    print(f"Delta : {result.delta:.4e}")
    print(f"Gamma : {result.gamma:.4e}")
    print(f"Vega  : {result.vega:.4e}")
    print(f"Theta : {result.theta/365:.4e}  per DAY")
    print(f"Theta : {result.theta:.4e}  per YEAR")
    plot_curve(args)