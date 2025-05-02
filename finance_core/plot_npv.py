from matplotlib import pyplot as plt
import numpy as np
from .npv import getNPV
import argparse
import sys

def plot_npv_curve(cashflows:list[float], rate_min:float=-0.5, rate_max:float=0.5, steps=100):
    """
    Plot NPV curve against discount rate using matplotlib.

    Args:
        cashflows (list[float]): Cash flows starting from time 0 (initial investment).
        rate_min (float): Minimum discount rate to plot.
        rate_max (float): Maximum discount rate to plot.
        steps (int): Number of rate points to evaluate. Higher means smoother curve.

    Returns:
        None. Displays a matplotlib plot showing NPV vs. discount rate and highlights approximate IRR.
    """
    rates = np.linspace(rate_min, rate_max, steps)
    npvs = [getNPV(cashflows, rate) for rate in rates]
    irr_ind = np.argmin(np.abs(npvs))
    plt.plot(rates, npvs, label="NPV Curve")
    plt.axhline(0, color='gray', linestyle='--', label=f"IRR approx.: {rates[irr_ind]:.2f}")
    plt.title("NPV vs. Discount Rate")
    plt.xlabel("Discount Rate")
    plt.ylabel("NPV ($)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    if len(sys.argv) < 2:
        print("Usage: python plot_npv.py <cashflows> [--rate_min -0.5] [--rate_max 0.5] [--steps 100]")
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="parser for plot_npv"
    )

    # required argument
    parser.add_argument("cashflows", nargs="+", type=float, help="Cashflows, space-separated (e.g. -100 50 50)")

    #optional argument 
    parser.add_argument("--rate_min", type=float, default=-0.5, help="Minimum rate to depict, default -0.5")
    parser.add_argument("--rate_max", type=float, default=0.5, help="Maximum rate to depict, default 0.5")
    parser.add_argument("--steps", type=float, default=100, help="number of steps to depict, default 100")

    args = parser.parse_args()

    plot_npv_curve(cashflows=args.cashflows, rate_min=args.rate_min, rate_max=args.rate_max, steps=args.steps)


if __name__ == "__main__":
    main()