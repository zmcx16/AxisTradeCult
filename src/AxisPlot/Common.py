import pandas
import numpy
import matplotlib.pyplot as plt
from Program.Common import *
import matplotlib.dates as mdates
import mpl_finance
import matplotlib.ticker as ticker


def PlotStockLinePriceVolumeData(Symbol,df_data, plotTitle):
    
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


def PlotStockCandlestickPriceVolumeData(Symbol,df_data, plotTitle):
    
    size_factor = 1.8
    
    fig = plt.figure()
    fig.canvas.set_window_title('Wanna join the Axis Cult?')
    fig.suptitle('Stock: {0} ({1} ~ {2})'.format(Symbol,df_data.index.min().strftime('%Y-%m-%d'),df_data.index.max().strftime('%Y-%m-%d')),y=1, fontsize=14)
    
    DefaultSize = fig.get_size_inches()
    fig.set_size_inches( (DefaultSize[0]*size_factor, DefaultSize[1]*size_factor) )
    
    ax1 = plt.subplot2grid((4, 1), (0, 0), rowspan=3)    
    ax2 = plt.subplot2grid((4, 1), (3, 0), sharex=ax1)    
    
    #for using mpl_finance
    df_data = df_data.reset_index()
    df_data.columns = ["Date","Open","High",'Low',"Close","Volume"]
    df_data['Date'] = df_data['Date'].map(mdates.date2num)   

    DateSize = len(df_data['Date'])
    date_indices = numpy.arange(DateSize)
    
    df_data_Date = df_data['Date']  
    df_data['Date'] = date_indices
    
    def format_date(x, pos):
        this_index = numpy.clip(int(x + 0.5), 0, DateSize - 1)        
        return mdates.num2date(df_data_Date[this_index]).strftime('%m/%d/%y') 

    lines, patches = mpl_finance.candlestick_ohlc(ax1,df_data.values,width=1, colorup='r', colordown='g')
    for line, patch in zip(lines, patches):
        patch.set_edgecolor("k")
        patch.set_linewidth(0.72)
        patch.set_antialiased(False)
        line.set_color("k")
        line.set_zorder(0) # make lines appear behind the patches
        line.set_visible(True) # make them invisible


    mpl_finance.volume_overlay(ax2, df_data['Open'], df_data['Close'], df_data['Volume'], colorup='r', colordown='g', width=1)

    def GetMondayList(df_data_Date):
        MondayList = []     
        for index in range(len(df_data_Date)):
            if mdates.num2date(df_data_Date[index]).weekday()==0:
                MondayList.append(index)
        
        return MondayList 

    ax2.xaxis.set_major_locator(ticker.FixedLocator(GetMondayList(df_data_Date)))
    ax2.xaxis.set_minor_locator(ticker.MultipleLocator(1))     
    
    ax2.xaxis.set_major_formatter(ticker.FuncFormatter(format_date)) 

    plt.xlabel("Date")    
    ax1.set_ylabel("Price")  
    ax2.set_ylabel('Volume')     
    
    for label in ax2.xaxis.get_ticklabels():
        label.set_rotation(45)
    
    plt.setp(ax1.get_xticklabels(), visible=False)
               
    ax1.grid(color='grey', linestyle='--', linewidth=0.5)
    ax2.grid(color='grey', linestyle='--', linewidth=0.5)
    
    plt.tight_layout()    
    plt.show()
 