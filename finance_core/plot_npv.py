from matplotlib import pyplot as plt
from collections import namedtuple
import numpy as np
from .npv import getNPV
from .irr import getIRR
import argparse
import json
import sys

PlotResult = namedtuple("PlotResult", ["irr", "irr2", "npvs", "npvs2", "rates", "json_dict"])

def plot_npv_curve(cashflows:list[float], 
                   rate_min:float=-0.5, 
                   rate_max:float=0.5, 
                   steps:int=100, 
                   save_path:str=None, 
                   cashflows2:list[float]=None,
                   return_json:str=None
                   ):
    """
    Plot NPV curve against discount rate using matplotlib.

    Args:
        cashflows (list[float]): Cash flows starting from time 0 (initial investment).
        rate_min (float): Minimum discount rate to plot.
        rate_max (float): Maximum discount rate to plot.
        steps (int): Number of rate points to evaluate. Higher means smoother curve.
        return_irr (bool): Control whether to return irr.
        save_path (str): If specified, save plot to this path
        cashflows2 (list[float]): If specified, plot this alongside the major cashflows.

    Returns:
        float | None: returns IRR value if return_irr is true, return None otherwise.
        Displays a matplotlib plot showing NPV vs. discount rate and highlights approximate IRR.
        Saves the matplotlib plot silently if save_path indicated.
    """

    #gets the dataset for major cashflow, handle irr non-existent exception
    rates = np.linspace(rate_min, rate_max, steps)
    npvs = [getNPV(cashflows, rate) for rate in rates]
    try:
        irr = getIRR(cashflows)
    except ValueError:
        irr = None

    
    #plots dataset
    plt.plot(rates, npvs, label="Primary NPV", color='blue')
    if irr is not None:
        plt.axhline(0, color='gray', linestyle='--', label=f"IRR approx.: {irr:.2f} ")
    else:
        plt.plot([], [], ' ', label="No primary IRR found")
    plt.title("NPV vs. Discount Rate")
    plt.xlabel("Discount Rate")
    plt.ylabel("NPV ($)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    #gets the dataset for secondary cashflow, handle irr non-existent exception
    if cashflows2:
        npvs2 = [getNPV(cashflows2, rate) for rate in rates]
        try:
            irr2 = getIRR(cashflows2)
        except ValueError:
            irr2 = None
        plt.plot(rates, npvs2, label="Compare NPV", color='orange')
        if irr2 is not None:
            plt.axhline(0, color='grey', linestyle='--', label=f"IRR2 approx.: {irr2:.2f} ")
        else:
            plt.plot([], [], ' ', label="No compare IRR found")
        plt.legend()


    #save image
    if save_path:
        try:
            plt.savefig(save_path)
        except:
            print(f"the path: {save_path} is invalid, unable to save, please recheck.")
        plt.close()
    else:
        plt.show()
    
    if return_json:
        json_dict = {
            "irr": irr,
            "rates": rates.tolist(),
            "npv1": npvs,
            "irr2": irr2,
            "rates": rates.tolist(),
            "npv2": npvs2
        }
    else: json_dict = None

    return PlotResult(
    irr=irr,
    irr2=irr2 if cashflows2 else None,
    npvs=npvs,
    npvs2=npvs2 if cashflows2 else None,
    rates=rates,
    json_dict=json_dict
)
    

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
    parser.add_argument("--compare", nargs="+", type=float, help="Cashflows to compare with, space-separated (e.g. -100 50 50)" )
    parser.add_argument("--save_json", type=str, default=None, help="save curve data to path, default None")
    args = parser.parse_args()

    result = plot_npv_curve(cashflows=args.cashflows, 
                   rate_min=args.rate_min, 
                   rate_max=args.rate_max, 
                   steps=args.steps,
                   save_path=args.save_path,
                   cashflows2=args.compare,
                   return_json=args.save_json is not None)
    if args.return_irr:
        print(f"IRR: {result.irr:.3f}") if result.irr is not None else print("No primary IRR found.")
        if args.compare:
            print(f"IRR2: {result.irr2:.3f}") if result.irr2 is not None else print("No compare IRR found.")
    
    if args.save_json is not None:
        with open(args.save_json, "w") as f:
            json.dump(result.json_dict, f, indent=2)

if __name__ == "__main__":
    main()