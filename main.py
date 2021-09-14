import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt,floor,ceil


def toDf(filename="capture_slopes.xls"):
    df = pd.read_excel(filename)
    df['date'] = pd.to_datetime(df['date'])
    df=df.set_index(['date'])
    return df

if __name__ == "__main__":
    df = toDf("capture_slopes.xls")
    nPlots = len(df["treatment"].unique())
    plotgas = ["N2O_N_mug_m2h","CO2_C_mug_m2h"]

    fig, axs = plt.subplots(nrows=len(plotgas), ncols=nPlots,figsize=(20,15),sharex=True,sharey='row')#,sharey=True)

    for i_gas,gas in enumerate(plotgas):
        axs[i_gas,0].set_ylabel(gas)
        for treatment in np.sort(df["treatment"].unique()):
                df[df["treatment"]== treatment].groupby(['nr'])[gas].plot(title = treatment, ax = axs[ i_gas,treatment-1],)

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.02, hspace=0)
    plt.show()