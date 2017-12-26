import pandas
import numpy
import matplotlib.pyplot as plt
from Program.Common import *
import matplotlib.dates as mdates
import mpl_finance
import matplotlib.ticker as ticker

from AxisPlot.DefStr import *
from numpy import NaN
from pandas.tests.frame.test_validate import dataframe

def PlotStockData(Symbol,df_data, PlotType,TechIndicators):
 
    size_factor = 1.8
    
    fig = plt.figure()
    fig.canvas.set_window_title('Wanna join the Axis Cult?')
    fig.suptitle('Stock: {0} ({1} ~ {2})'.format(Symbol,df_data.index.min().strftime('%Y-%m-%d'),df_data.index.max().strftime('%Y-%m-%d')),y=1, fontsize=14)
    
    DefaultSize = fig.get_size_inches()
    fig.set_size_inches( (DefaultSize[0]*size_factor, DefaultSize[1]*size_factor) )

    row_size=3
    row_index=[0]
    for indicator in TechIndicators:
        IndicatorName = indicator[strName]
        if TechIndicatorPlotMode[IndicatorName][strPlotInAxPrice] == False:
            row_size+=1
            
    ax_price = plt.subplot2grid((row_size, 1), (0, 0), rowspan=2)   
    row_index[0] = 2
    ax_volume = plt.subplot2grid((row_size, 1), (row_size-1, 0), sharex=ax_price)    

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
        lines, patches = mpl_finance.candlestick_ohlc(ax_price,df_data.values,width=1, colorup='r', colordown='g')
        for line, patch in zip(lines, patches):
            patch.set_edgecolor("k")
            patch.set_linewidth(0.72)
            patch.set_antialiased(False)
            line.set_color("k")
            line.set_zorder(0) # make lines appear behind the patches
            line.set_visible(True) # make them invisible
    elif PlotType == strBasic:
        df_data[strClose].plot(ax=ax_price,kind='line', color='g')
              
    mpl_finance.volume_overlay(ax_volume, df_data[strOpen], df_data[strClose], df_data[strVolume], colorup='r', colordown='g', width=1)

    def GetMondayList(df_data_Date):
        MondayList = []     
        for index in range(len(df_data_Date)):
            if mdates.num2date(df_data_Date[index]).weekday()==0:
                MondayList.append(index)
        
        return MondayList 

    ax_volume.xaxis.set_major_locator(ticker.FixedLocator(GetMondayList(df_data_Date)))
    ax_volume.xaxis.set_minor_locator(ticker.MultipleLocator(1))     
    
    ax_volume.xaxis.set_major_formatter(ticker.FuncFormatter(format_date)) 

    plt.xlabel("Date")    
    ax_price.set_ylabel("Price")  
    ax_volume.set_ylabel('Volume')     
    
    for label in ax_volume.xaxis.get_ticklabels():
        label.set_rotation(45)
     
    for indicator in TechIndicators:
        TechIndicatorName = indicator[strName]
        TechIndicatorFuncDict[TechIndicatorName][strFuncName](indicator[strParam],df_data,ax_price,row_size,row_index)
    
    #PlotKDJ(df_data, ax_price)
    
    #GetKDJ(df_data[strClose], df_data[strHigh], df_data[strLow], 9)
    
    plt.setp(ax_price.get_xticklabels(), visible=False)
               
    ax_price.grid(color='grey', linestyle='--', linewidth=0.5)
    ax_volume.grid(color='grey', linestyle='--', linewidth=0.5)
    
    plt.tight_layout()    
    plt.show()


def PlotMA(param, df_data, target_ax, row_size, row_index):
    Indicator = GetRollingMean(df_data[strClose], int(param[strWindow]))
    PlotIndicator(Indicator, target_ax = target_ax, color = param[strColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))    

 
def PlotBollingerBands(param, df_data, target_ax, row_size, row_index):
    MA_mean = GetRollingMean(df_data[strClose],int(param[strWindow]))
    MA_std = GetRollingStd(df_data[strClose],int(param[strWindow]))
    IndicatorUpper, IndicatorLower = GetBollingerBands(MA_mean,MA_std)
    PlotIndicator(IndicatorUpper, target_ax = target_ax, color = param[strColor], linewidth =float(param[strLineWidth]), alpha = float(param[strAlpha]))    
    PlotIndicator(IndicatorLower, target_ax = target_ax, color = param[strColor], linewidth =float(param[strLineWidth]), alpha = float(param[strAlpha])) 
    target_ax.fill_between(df_data[strDate],IndicatorUpper,IndicatorLower,interpolate=True,color=param[strAreaColor] ,alpha = float(param[strAreaAlpha]))

def PlotKDJ(param, df_data, target_ax, row_size, row_index):
    ax = plt.subplot2grid((row_size, 1), (row_index[0], 0), sharex=target_ax) 
    row_index[0]+=1
    k,d,j = GetKDJ(df_data[strClose], df_data[strHigh], df_data[strLow], int(param[strWindow]))
    PlotIndicator(k, target_ax = ax, color = param[strKColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))    
    PlotIndicator(d, target_ax = ax, color = param[strDColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))
    PlotIndicator(j, target_ax = ax, color = param[strJColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))    
    
    basic_array1 = numpy.ones(len(df_data[strClose]))
    PlotIndicator(pandas.Series(basic_array1*80), target_ax = ax, color = 'grey', linewidth = 1.5, alpha = 1)    
    PlotIndicator(pandas.Series(basic_array1*20), target_ax = ax, color = 'grey', linewidth = 1.5, alpha = 1)    
    
    plt.setp(ax.get_xticklabels(), visible=False)
    ax.grid(color='grey', linestyle='--', linewidth=0.5)
    
    
def PlotIndicator(df_data,target_ax,color,linewidth=0.8,alpha=0.8):
    df_data.plot(ax=target_ax, color = color, linewidth=linewidth, alpha =alpha)

def GetRollingMean(values, window):
    return pandas.Series.rolling(values, window=window,center=False).mean()

def GetRollingStd(values, window):
    return pandas.Series.rolling(values, window=window,center=False).std()

def GetBollingerBands(rm, rstd):
    upper_band = rm+rstd*2
    lower_band = rm-rstd*2
    return upper_band, lower_band

def GetKDJ(close_values, high_values, low_values, period):
    rsv = GetRSV(close_values, high_values, low_values, period)   
    k = pandas.Series(_calc_kd(rsv))   
    d = pandas.Series(_calc_kd(k))   
    j = 3*d-2*k
    
    return k,d,j
    
def _calc_kd(val,weight = 1/3.0):
    """
    k[0]=50
    for i in range(1,len(val)):     
        if pandas.isnull(val[i]):
            k[i] = 50
        else:
            k[i] = 2/3.0*k[i-1]+1/3.0*val[i]
    
    return k    
    """
    k = 50.0
    for i in weight * val:
        if pandas.isnull(i):
            yield k
        else:
            k = (1-weight) * k + i
            yield k


def GetRSV(close_values, high_values, low_values, period):
    hight_max = pandas.Series.rolling(high_values, window=period,center=False).max()
    low_min = pandas.Series.rolling(low_values, window=period,center=False).min()
    return (close_values-low_min)/(hight_max-low_min)*100

ColorList = ['aqua','aquamarine','azure','beige','black','blue','brown','chartreuse','chocolate','coral','crimson','cyan','darkblue','darkgreen','fuchsia','gold','goldenrod','green'
             ,'grey','indigo','ivory','khaki','lavender','lightblue','lightgreen','lime','magenta','maroon','navy','olive','orange','orangered','orchid','pink','plum','purple','red'
             ,'salmon','sienna','silver','tan','teal','tomato','turquoise','violet','wheat','white','yellow','yellowgreen']


TechIndicatorFuncDict = {
  strMA:                {strFuncName: PlotMA,                strParam:{strColor:'red', strWindow: 20, strLineWidth: 0.8, strAlpha: 0.8}},
  strBollingerBands:    {strFuncName: PlotBollingerBands,    strParam:{strColor:'grey', strWindow: 20, strLineWidth: 0.8, strAlpha: 0.8, strAreaColor: 'gold', strAreaAlpha:0.3}},
  strKDJ:               {strFuncName: PlotKDJ,               strParam:{strKColor:'red', strDColor:'black', strJColor:'gold', strWindow: 9, strLineWidth: 0.8, strAlpha: 0.8}}
}

TechIndicatorPlotMode = {
  strMA:                {strPlotInAxPrice: True,     strYlabel:   None},
  strBollingerBands:    {strPlotInAxPrice: True,     strYlabel:   None},
  strKDJ:               {strPlotInAxPrice: False,    strYlabel:   strKDJ},  
}

TechIndicatorWidgetParam = {
  strMA:                {strColor:  {strType:strComboBox,  strValue:'red', strComboList: ColorList}, strWindow: {strType:strLineEdit,  strValue:20},  strLineWidth: {strType:strLineEdit,  strValue:0.8}, strAlpha: {strType:strLineEdit,  strValue:0.8}},
  strBollingerBands:    {strColor:  {strType:strComboBox,  strValue:'grey', strComboList: ColorList}, strWindow: {strType:strLineEdit,  strValue:20},  strLineWidth: {strType:strLineEdit,  strValue:0.8}, strAlpha: {strType:strLineEdit,  strValue:0.8}, strAreaColor:  {strType:strComboBox,  strValue:'gold', strComboList: ColorList}, strAreaAlpha: {strType:strLineEdit,  strValue:0.3}},
  strKDJ:               {strKColor: {strType:strComboBox,  strValue:'red', strComboList: ColorList}, strDColor: {strType:strComboBox,  strValue:'black', strComboList: ColorList}, strJColor: {strType:strComboBox,  strValue:'gold', strComboList: ColorList}, strWindow: {strType:strLineEdit,  strValue:9},  strLineWidth: {strType:strLineEdit,  strValue:1}, strAlpha: {strType:strLineEdit,  strValue:1}}
}
