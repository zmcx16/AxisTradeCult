import pandas
import numpy
import matplotlib.pyplot as plt
from Program.Common import *


def PlotStockPriceVolumeData(df_data, plotTitle):
    
    size_factor = 1.8
    
    fig = plt.figure()
    DefaultSize = fig.get_size_inches()
    fig.set_size_inches( (DefaultSize[0]*size_factor, DefaultSize[1]*size_factor) )
    
    ax1 = plt.subplot2grid((4, 1), (0, 0), rowspan=3)
    ax2 = plt.subplot2grid((4, 1), (3, 0), sharex=ax1)
    
    #ax2 = ax1.twinx()
    df_data['Adj. Close'].plot(ax=ax1,kind='line', color='g')
    df_data['Adj. Volume'].plot(ax=ax2, kind='area', legend=False, color='grey')
    
    ax1.set_ylabel('Adj. Close', color='g')
    ax2.set_ylabel('Adj. Volume', color='grey')
    
    ax1.grid(color='grey', linestyle='--', linewidth=0.5)
    
    plt.tight_layout()
    plt.show()
    
 