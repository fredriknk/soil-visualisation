import pandas as pd
import matplotlib
matplotlib.use('TkAgg') # plot as external window
import matplotlib.pyplot as plt
plt.ioff()
import numpy as np
from multiprocessing import Pool
from scipy import interpolate
from math import sqrt,floor,ceil


def toDf(filename="capture_slopes.xls",date_column = "date"):
    df = pd.read_excel(filename)
    df[date_column] = pd.to_datetime(df[date_column])
    df=df.set_index([date_column])
    return df

def plotDF(dt,group1,gas,treatment,params,ax):

    if "I" in params:  # Interpolate missing values
        dt = dt.interpolate()

    if "A" in params:  # average and get info (std_div, min values, max values
        dx = dt[gas]

        mean_v = dx.groupby(dx.index.date).mean()  # .interpolate(method="spline")
        std_dev = dx.groupby(dx.index.date).std()
        min_v = dx.groupby(dx.index.date).min()
        max_v = dx.groupby(dx.index.date).max()

        if i_gas == 0:
            title = treatment
        else:
            title = ""

        mean_v.plot(title=title, ax=axs[i_gas, treatment - 1])
        color = "blue"
        if "S" in params:
            ax.fill_between(std_dev.index, mean_v + std_dev, mean_v - std_dev, color=color,
                                                   alpha=0.2)
            color = "red"
        if "X" in params:
            ax.fill_between(min_v.index, min_v, max_v, color=color, alpha=0.2)
            color = "green"
    if "R" in params:  # If not average, just print all plots individually
        dt.groupby([subgroup])[gas].plot(title=treatment, ax=ax )

    return ax

def matrixplot(df,
               plotcolumns = ["N2O_N_mug_m2h", "CO2_C_mug_m2h"],
               group1 ="treatment",
               subgroup ='nr',
               params = "ASI",
               figsize=(20, 15)):

    nPlots = len(df[group1].unique())

    fig, axs = plt.subplots(nrows=len(plotcolumns), ncols=nPlots, figsize=figsize, sharex=True,
                            sharey='row')  # ,sharey=True)
    pool = Pool(4)
    for i_gas, gas in enumerate(plotcolumns):
        axs[i_gas, 0].set_ylabel(gas)

        for treatment in np.sort(df[group1].unique()):
            dt = df[df[group1] == treatment]
            axs[i_gas, treatment - 1] = plotDF(dt,group1,gas,treatment,params,axs[i_gas, treatment - 1])


    fig.autofmt_xdate(rotation=70)
    plt.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.show()

if __name__ == "__main__":
    filename = "data/Copy of capture_slopes.xls" #filename for raw data
    date_column = "date"
    plotcolumns = ["N2O_N_mug_m2h", "CO2_C_mug_m2h"] #the collumns in the excel document to be parsed
    group1 = "treatment" # The first group to sort data by
    subgroup = 'nr' # the second group to sort data by
    params = "RI" # A = Average, S = Stdev, I = Interpolate, R = Regular (all graphs superimposed) X = Minmax
    figsize = (20, 15)

    df = toDf(filename,
              date_column)

    matrixplot(df,
               plotcolumns ,
               group1,
               subgroup,
               params,
               figsize)

