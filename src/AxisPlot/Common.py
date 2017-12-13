import pandas
import numpy
import matplotlib.pyplot as plt
from Program.Common import *
import matplotlib.dates as mdates
import mpl_finance
import matplotlib.ticker as ticker


def PlotStockLinePriceVolumeData(df_data, plotTitle):
    
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


def PlotStockCandlestickPriceVolumeData(df_data, plotTitle):
    
    size_factor = 1.8
    
    fig = plt.figure()
    DefaultSize = fig.get_size_inches()
    fig.set_size_inches( (DefaultSize[0]*size_factor, DefaultSize[1]*size_factor) )
    
    ax1 = plt.subplot2grid((4, 1), (0, 0), rowspan=3)    
    ax2 = plt.subplot2grid((4, 1), (3, 0), sharex=ax1)    
    
    df_data = df_data.reset_index()
    df_data.columns = ["Date","Open","High",'Low',"Close","Volume"]
    
    df_data['Date'] = df_data['Date'].map(mdates.date2num)   
    #ax1.xaxis_date()
    
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)

    DateSize = len(df_data['Date'])
    date_indices = numpy.arange(DateSize)
    
    df_data_Date_copy = df_data['Date']  
    df_data['Date'] = date_indices
    
    print(date_indices)
    def format_date(x, pos):
        this_index = numpy.clip(int(x + 0.5), 0, DateSize - 1)        
        return mdates.num2date(df_data_Date_copy[this_index]).strftime('%Y-%m-%d') 

    plt.xlabel("Date")
    lines, patches = mpl_finance.candlestick_ohlc(ax1,df_data.values,width=1, colorup='r', colordown='g')
    for line, patch in zip(lines, patches):
        patch.set_edgecolor("k")
        patch.set_linewidth(0.72)
        patch.set_antialiased(False)
        line.set_color("k")
        line.set_zorder(0) # make lines appear behind the patches
        line.set_visible(True) # make them invisible
    
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))    
    #fig.autofmt_xdate()
 
    df_data['Volume'].plot(ax=ax2, kind='bar', legend=False, color='grey')
    #ax2.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))   
    #plt.bar(df_data['Date'],df_data['Volume'])
    ax2.set_ylabel('Volume', color='grey')
        
    plt.ylabel("Price")
       
    ax1.grid(color='grey', linestyle='--', linewidth=0.5)
    plt.tight_layout()    
    plt.show()
 