import pandas
import numpy
import matplotlib.pyplot as plt
from Program.Common import *


def PlotStockPriceVolumeData(df_data, plotTitle):

    fig = plt.figure()
    ax1 = fig.add_subplot(111)   
    ax2 = ax1.twinx()
    df_data['Adj. Close'].plot(ax=ax1,kind='line')
    df_data['Adj. Volume'].plot(ax=ax2, kind='area', legend=False, color='b')
    ax1.set_ylabel('Adj. Close', color='g')
    ax2.set_ylabel('Adj. Volume', color='b')
    plt.show()
    
 