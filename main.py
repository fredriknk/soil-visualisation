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
               params = "ASI",
               figsize=(20, 15)):

    nPlots = len(df[group1].unique())

    fig, axs = plt.subplots(nrows=len(plotcolumns), ncols=nPlots, figsize=figsize, sharex=True,
                            sharey='row')  # ,sharey=True)

    for i_gas, gas in enumerate(plotcolumns):
        axs[i_gas, 0].set_ylabel(gas)
        for treatment in np.sort(df[group1].unique()):
            dx = df[df[group1] == treatment]

            if "I" in params:
                dx = dx.interpolate()

            if "A" not in params:
                dx.groupby([subgroup])[gas].plot(title=treatment, ax=axs[i_gas, treatment - 1], )
            else:
                dx = dx[gas]
                mean_v = dx.groupby(dx.index.date).mean()
                std_dev = dx.groupby(dx.index.date).std()
                min_v =  dx.groupby(dx.index.date).min()
                max_v = dx.groupby(dx.index.date).max()
                mean_v.plot(title=treatment, ax=axs[i_gas, treatment - 1])
                if "S" in params:
                    axs[i_gas, treatment - 1].fill_between(std_dev.index,mean_v+std_dev,mean_v-std_dev,color='blue',alpha = 0.2)
                else:
                    axs[i_gas, treatment - 1].fill_between(min_v.index, min_v, max_v, color='blue', alpha=0.2)

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.02, hspace=0)
    plt.show()

if __name__ == "__main__":
    filename = "Copy of capture_slopes.xls" #filename for raw data
    date_column = "date"
    plotcolumns = ["N2O_N_mug_m2h", "CO2_C_mug_m2h"] #the collumns in the excel document to be parsed
    group1 = "treatment" # The first group to sort data by
    subgroup = 'nr' # the second group to sort data by
    params = "AI" # A = average, S = stdev, I = Interpolate
    figsize = (20, 15)

    df = toDf(filename,
              date_column)

    matrixplot(df,
               plotcolumns ,
               group1,
               subgroup,
               params,
               figsize)

