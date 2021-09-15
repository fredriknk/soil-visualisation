import pandas as pd
import matplotlib
matplotlib.use('TkAgg') # plot as external window
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt,floor,ceil


def toDf(filename="capture_slopes.xls",date_column = "date"):
    df = pd.read_excel(filename)
    df[date_column] = pd.to_datetime(df[date_column])
    df=df.set_index([date_column])
    return df

def matrixplot(df,
               plotcolumns = ["N2O_N_mug_m2h", "CO2_C_mug_m2h"],
               group1 ="treatment",
               subgroup ='nr',
               avg_plots = "false",
               figsize=(20, 15)):

    nPlots = len(df[group1].unique())

    fig, axs = plt.subplots(nrows=len(plotcolumns), ncols=nPlots, figsize=figsize, sharex=True,
                            sharey='row')  # ,sharey=True)

    for i_gas, gas in enumerate(plotcolumns):
        axs[i_gas, 0].set_ylabel(gas)
        for treatment in np.sort(df[group1].unique()):
            if avg_plots:
                df[(df[group1] == treatment)].groupby([subgroup])[gas].plot(title=treatment, ax=axs[i_gas, treatment - 1], )

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.02, hspace=0)
    plt.show()

if __name__ == "__main__":
    df = toDf("Copy of capture_slopes.xls",
              date_column = "date")

    matrixplot(df,
               plotcolumns = ["N2O_N_mug_m2h", "CO2_C_mug_m2h"],
               group1 ="treatment",
               subgroup ='nr',
               avg_plots = "false",
               figsize=(20, 15))