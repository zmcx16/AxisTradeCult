import pandas
import numpy
import matplotlib.pyplot as plt
from Program.Common import *
import matplotlib.dates as mdates
import mpl_finance
import matplotlib.ticker as ticker

from AxisPlot.DefStr import *

def PlotStockData(Symbol,df_data, PlotType,TechIndicators):
 
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
    df_data.columns = [strDate,strOpen,strHigh,strLow,strClose,strVolume]
    df_data[strDate] = df_data[strDate].map(mdates.date2num)   

    DateSize = len(df_data[strDate])
    date_indices = numpy.arange(DateSize)
    
    df_data_Date = df_data[strDate]  
    df_data[strDate] = date_indices
    
    def format_date(x, pos):
        this_index = numpy.clip(int(x + 0.5), 0, DateSize - 1)        
        return mdates.num2date(df_data_Date[this_index]).strftime('%m/%d/%y') 
        
    if PlotType == strCandle: 
        lines, patches = mpl_finance.candlestick_ohlc(ax1,df_data.values,width=1, colorup='r', colordown='g')
        for line, patch in zip(lines, patches):
            patch.set_edgecolor("k")
            patch.set_linewidth(0.72)
            patch.set_antialiased(False)
            line.set_color("k")
            line.set_zorder(0) # make lines appear behind the patches
            line.set_visible(True) # make them invisible
    elif PlotType == strBasic:
        df_data[strClose].plot(ax=ax1,kind='line', color='g')
              
    mpl_finance.volume_overlay(ax2, df_data[strOpen], df_data[strClose], df_data[strVolume], colorup='r', colordown='g', width=1)

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
 
    if len(TechIndicators)>0:  
        for indicator in TechIndicators:
            TechIndicatorFuncName = indicator[strTechIndicatorName]
            TechIndicatorFuncDict[TechIndicatorFuncName](indicator,df_data,ax1)
    
    plt.tight_layout()    
    plt.show()

def PlotMA(param, df_data, target_ax):
    Indicator = get_rolling_mean(df_data[strClose], param[strWindow])
    PlotIndicator(Indicator, target_ax = target_ax, color = param[strColor], linewidth =param[strLineWidth], alpha = param[strAlpha])    

def PlotIndicator(df_data,target_ax,color,linewidth=0.8,alpha=0.8):
    df_data.plot(ax=target_ax, color = color, linewidth=linewidth, alpha =alpha)

def get_rolling_mean(values, window):
    return pandas.Series.rolling(values, window=window,center=False).mean()

def get_rolling_std(values, window):
    return pandas.Series.rolling(values, window=window,center=False).std()

def get_bollinger_bands(rm, rstd):
    upper_band = rm+rstd*2
    lower_band = rm-rstd*2
    return upper_band, lower_band


TechIndicatorFuncDict = {
  strMA: PlotMA
  
}
 