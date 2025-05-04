from matplotlib import pyplot as plt
import numpy as np
from .npv import getNPV
from .irr import getIRR
import argparse
import sys

def plot_npv_curve(cashflows:list[float], rate_min:float=-0.5, rate_max:float=0.5, steps:int=100, return_irr:bool=False, save_path:str=None):
    """
    Plot NPV curve against discount rate using matplotlib.

    Args:
        cashflows (list[float]): Cash flows starting from time 0 (initial investment).
        rate_min (float): Minimum discount rate to plot.
        rate_max (float): Maximum discount rate to plot.
        steps (int): Number of rate points to evaluate. Higher means smoother curve.

    Returns:
        float | None: returns IRR value if return_irr is true, return None otherwise.
        Displays a matplotlib plot showing NPV vs. discount rate and highlights approximate IRR.
        Saves the matplotlib plot silently if save_path indicated.
    """

    #gets the dataset, handle irr non-existent exception
    rates = np.linspace(rate_min, rate_max, steps)
    npvs = [getNPV(cashflows, rate) for rate in rates]
    try:
        irr = getIRR(cashflows)
    except ValueError:
        irr = None

    #plots dataset
    plt.plot(rates, npvs, label="NPV Curve")
    if irr:
        plt.axhline(0, color='gray', linestyle='--', label=f"IRR approx.: {irr:.2f} ")
    else:
        plt.plot([], [], ' ', label="No IRR found")
    plt.title("NPV vs. Discount Rate")
    plt.xlabel("Discount Rate")
    plt.ylabel("NPV ($)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    #save image
    if save_path:
        try:
            plt.savefig(save_path)
        except:
            print(f"the path: {save_path} is invalid, unable to save, please recheck.")
        plt.close()
    else:
        plt.show()

    #return irr
    if return_irr == True:
        return irr
    

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
    parser.add_argument("--return_irr", action='store_true', help="return irr value, default false")
    parser.add_argument("--save_path", type=str, default=None, help="save the plot to path, default None")
    args = parser.parse_args()

    irr = plot_npv_curve(cashflows=args.cashflows, 
                   rate_min=args.rate_min, 
                   rate_max=args.rate_max, 
                   steps=args.steps,
                   return_irr=args.return_irr,
                   save_path=args.save_path)
    if args.return_irr:
        print(f"IRR: {irr:.3f}")

if __name__ == "__main__":
    main()