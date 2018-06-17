import pandas
import numpy
import matplotlib.pyplot as plt
from Program.Common import *
import matplotlib.dates as mdates
import mpl_finance
import matplotlib.ticker as ticker

from CommonDef.DefStr import *
from numpy import NaN
from Statistics_TechIndicators.CalcTechIndictors import *

from pandas.tests.frame.test_validate import dataframe


def PlotStockData(Symbol, df_data, PlotType, TechIndicators, size_factor):

    fig = plt.figure()
    fig.canvas.set_window_title('Wanna join the Axis Cult?')
    fig.suptitle('Stock: {0} ({1} ~ {2})'.format(Symbol, df_data.index.min().strftime('%Y-%m-%d'), df_data.index.max().strftime('%Y-%m-%d')), y = 1, fontsize = 14)

    DefaultSize = fig.get_size_inches()
    fig.set_size_inches((DefaultSize[0] * size_factor, DefaultSize[1] * size_factor))

    row_size = 3
    row_index = [0]
    for indicator in TechIndicators:
        IndicatorName = indicator[strName]
        if TechIndicatorPlotMode[IndicatorName][strPlotInAxPrice] == False:
            row_size += 1

    ax_price = plt.subplot2grid((row_size, 1), (0, 0), rowspan = 2)
    row_index[0] = 2
    ax_volume = plt.subplot2grid((row_size, 1), (row_size - 1, 0), sharex = ax_price)

    # for using mpl_finance
    df_data = df_data.reset_index()
    df_data.columns = [strDate, strOpen, strHigh, strLow, strClose, strVolume]
    df_data[strDate] = df_data[strDate].map(mdates.date2num)

    DateSize = len(df_data[strDate])
    date_indices = numpy.arange(DateSize)

    df_data_Date = df_data[strDate]
    df_data[strDate] = date_indices

    def format_date(x, pos):
        this_index = numpy.clip(int(x + 0.5), 0, DateSize - 1)
        return mdates.num2date(df_data_Date[this_index]).strftime('%m/%d/%y')

    if PlotType == strCandle:
        lines, patches = mpl_finance.candlestick_ohlc(ax_price, df_data.values, width = 1, colorup = 'r', colordown = 'g')
        for line, patch in zip(lines, patches):
            patch.set_edgecolor("k")
            patch.set_linewidth(0.72)
            patch.set_antialiased(False)
            line.set_color("k")
            line.set_zorder(0)  # make lines appear behind the patches
            line.set_visible(True)  # make them invisible
    elif PlotType == strBasic:
        df_data[strClose].plot(ax = ax_price, kind = 'line', color = 'g')

    mpl_finance.volume_overlay(ax_volume, df_data[strOpen], df_data[strClose], df_data[strVolume], colorup = 'r', colordown = 'g', width = 1)

    def GetMondayList(df_data_Date):
        MondayList = []
        for index in range(len(df_data_Date)):
            if mdates.num2date(df_data_Date[index]).weekday() == 0:
                MondayList.append(index)

        return MondayList

    plt.xlabel("Date")
    ax_price.set_ylabel("Price")
    ax_volume.set_ylabel('Volume')

    for label in ax_volume.xaxis.get_ticklabels():
        label.set_rotation(45)

    for indicator in TechIndicators:
        TechIndicatorName = indicator[strName]
        TechIndicatorFuncDict[TechIndicatorName][strFuncName](indicator[strParam], df_data, ax_price, row_size, row_index)

    plt.setp(ax_price.get_xticklabels(), visible = False)

    ax_price.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    ax_volume.grid(color = 'grey', linestyle = '--', linewidth = 0.5)

    ax_volume.xaxis.set_major_locator(ticker.FixedLocator(GetMondayList(df_data_Date)))
    ax_volume.xaxis.set_minor_locator(ticker.MultipleLocator(1))

    ax_volume.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))


    plt.tight_layout()
    return fig


def PlotSMA(param, df_data, target_ax, row_size, row_index):
    Indicator = GetRollingMean(df_data[strClose], int(param[strWindow]))
    PlotIndicator(Indicator, target_ax = target_ax, color = param[strColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))

def PlotEMA(param, df_data, target_ax, row_size, row_index):
    Indicator = GetEMA(df_data[strClose], int(param[strWindow]))
    PlotIndicator(Indicator, target_ax = target_ax, color = param[strColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))

def PlotSMMA(param, df_data, target_ax, row_size, row_index):
    Indicator = GetSMMA(df_data[strClose], int(param[strWindow]))
    PlotIndicator(Indicator, target_ax = target_ax, color = param[strColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))

def PlotDMA(param, df_data, target_ax, row_size, row_index):
    ax = plt.subplot2grid((row_size, 1), (row_index[0], 0), sharex = target_ax)
    row_index[0] += 1
    dma = GetDMA(df_data[strClose], short_window=int(param[strShortWindow]), long_window=int(param[strLongWindow]))
    PlotIndicator(dma, target_ax = ax, color = param[strColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))

    plt.setp(ax.get_xticklabels(), visible = False)
    ax.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    ax.set_ylabel(TechIndicatorPlotMode[strDMA][strYlabel])

def PlotMSTD(param, df_data, target_ax, row_size, row_index):
    ax = plt.subplot2grid((row_size, 1), (row_index[0], 0), sharex = target_ax)
    row_index[0] += 1
    mstd = GetRollingStd(df_data[strClose], int(param[strWindow]))
    PlotIndicator(mstd, target_ax = ax, color = param[strColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))

    plt.setp(ax.get_xticklabels(), visible = False)
    ax.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    ax.set_ylabel(TechIndicatorPlotMode[strMSTD][strYlabel])

def PlotMVAR(param, df_data, target_ax, row_size, row_index):
    ax = plt.subplot2grid((row_size, 1), (row_index[0], 0), sharex = target_ax)
    row_index[0] += 1
    mvar = GetRollingVar(df_data[strClose], int(param[strWindow]))
    PlotIndicator(mvar, target_ax = ax, color = param[strColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))

    plt.setp(ax.get_xticklabels(), visible = False)
    ax.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    ax.set_ylabel(TechIndicatorPlotMode[strMVAR][strYlabel])

def PlotRSI(param, df_data, target_ax, row_size, row_index):
    ax = plt.subplot2grid((row_size, 1), (row_index[0], 0), sharex = target_ax)
    row_index[0] += 1
    rsi = GetRSI(df_data[strClose], int(param[strWindow]))
    PlotIndicator(rsi, target_ax = ax, color = param[strColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))

    plt.setp(ax.get_xticklabels(), visible = False)
    ax.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    ax.set_ylabel(TechIndicatorPlotMode[strRSI][strYlabel])

def PlotMACD(param, df_data, target_ax, row_size, row_index):
    ax = plt.subplot2grid((row_size, 1), (row_index[0], 0), sharex = target_ax)
    row_index[0] += 1
    DIF, DEM, OSC = GetMACD(df_data[strClose], int(param[strFastWindow]), int(param[strSlowWindow]), int(param[strSignalWindow]))  
    PlotIndicator(DIF, target_ax = ax, color = param[strMACDColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))
    PlotIndicator(DEM, target_ax = ax, color = param[strSignalColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))

    OSC_prev = OSC.shift(1)
    OSC_trend = OSC > OSC_prev
    
    OSC.plot(ax = ax, width = 0.8, alpha = float(param[strAlpha]), kind='bar', color=OSC_trend.map({True: param[strBarIncColor], False: param[strBarDecColor]}))
    
    plt.setp(ax.get_xticklabels(), visible = False)
    ax.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    ax.set_ylabel(TechIndicatorPlotMode[strMACD][strYlabel])

def PlotWR(param, df_data, target_ax, row_size, row_index):
    ax = plt.subplot2grid((row_size, 1), (row_index[0], 0), sharex = target_ax)
    row_index[0] += 1
    WR = GetWR(df_data[strClose], df_data[strHigh], df_data[strLow], int(param[strWindow]))
    
    PlotIndicator(WR, target_ax = ax, color = param[strColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))
    
    basic_array1 = numpy.ones(len(df_data[strClose]))
    Upper = pandas.Series(basic_array1 * -20)
    Lower = pandas.Series(basic_array1 * -80)
    PlotIndicator(Upper, target_ax = ax, color = 'grey', linewidth = 0.8, alpha = 0.8)
    PlotIndicator(Lower, target_ax = ax, color = 'grey', linewidth = 0.8, alpha = 0.8)
    
    ax.fill_between(df_data[strDate], WR, Upper, where = Upper<=WR, interpolate = True, color = param[strOverBColor] , alpha = float(param[strAreaAlpha]))
    ax.fill_between(df_data[strDate], WR, Lower, where = Lower>=WR, interpolate = True, color = param[strOverSColor] , alpha = float(param[strAreaAlpha]))

    plt.setp(ax.get_xticklabels(), visible = False)
    ax.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    ax.set_ylabel(TechIndicatorPlotMode[strWR][strYlabel])

def PlotCCI(param, df_data, target_ax, row_size, row_index):
    ax = plt.subplot2grid((row_size, 1), (row_index[0], 0), sharex = target_ax)
    row_index[0] += 1
    CCI = GetCCI(df_data[strClose], df_data[strHigh], df_data[strLow], int(param[strWindow]))
    
    PlotIndicator(CCI, target_ax = ax, color = param[strColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))
    
    basic_array1 = numpy.ones(len(df_data[strClose]))
    Upper = pandas.Series(basic_array1 * 100)
    Lower = pandas.Series(basic_array1 *-100)
    PlotIndicator(Upper, target_ax = ax, color = 'grey', linewidth = 0.8, alpha = 0.8)
    PlotIndicator(Lower, target_ax = ax, color = 'grey', linewidth = 0.8, alpha = 0.8)
    
    ax.fill_between(df_data[strDate], CCI, Upper, where = Upper<=CCI, interpolate = True, color = param[strOverBColor] , alpha = float(param[strAreaAlpha]))
    ax.fill_between(df_data[strDate], CCI, Lower, where = Lower>=CCI, interpolate = True, color = param[strOverSColor] , alpha = float(param[strAreaAlpha]))

    plt.setp(ax.get_xticklabels(), visible = False)
    ax.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    ax.set_ylabel(TechIndicatorPlotMode[strCCI][strYlabel])

def PlotTR(param, df_data, target_ax, row_size, row_index):
    ax = plt.subplot2grid((row_size, 1), (row_index[0], 0), sharex = target_ax)
    row_index[0] += 1
    tr = GetTR(df_data[strClose], df_data[strHigh], df_data[strLow])
    print(type(tr))
    PlotIndicator(tr, target_ax = ax, color = param[strColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))

    plt.setp(ax.get_xticklabels(), visible = False)
    ax.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    ax.set_ylabel(TechIndicatorPlotMode[strTR][strYlabel])

def PlotATR(param, df_data, target_ax, row_size, row_index):
    ax = plt.subplot2grid((row_size, 1), (row_index[0], 0), sharex = target_ax)
    row_index[0] += 1
    atr = GetATR(df_data[strClose], df_data[strHigh], df_data[strLow], int(param[strWindow]))
    PlotIndicator(atr, target_ax = ax, color = param[strColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))

    plt.setp(ax.get_xticklabels(), visible = False)
    ax.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    ax.set_ylabel(TechIndicatorPlotMode[strATR][strYlabel])

def PlotDMI(param, df_data, target_ax, row_size, row_index):
    ax = plt.subplot2grid((row_size, 1), (row_index[0], 0), sharex = target_ax)
    row_index[0] += 1
    pDI, nDI, ADX, ADXR = GetDMI(df_data[strClose], df_data[strHigh], df_data[strLow], int(param[strWindow]))
    
    PlotIndicator(pDI, target_ax = ax, color = param[strpDIColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))
    PlotIndicator(nDI, target_ax = ax, color = param[strnDIColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))
    PlotIndicator(ADX, target_ax = ax, color = param[strADXColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))
    PlotIndicator(ADXR, target_ax = ax, color = param[strADXRColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))

    plt.setp(ax.get_xticklabels(), visible = False)
    ax.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    ax.set_ylabel(TechIndicatorPlotMode[strDMI][strYlabel])

def PlotTEMA(param, df_data, target_ax, row_size, row_index):
    Indicator = GetTEMA(df_data[strClose], int(param[strWindow]))
    PlotIndicator(Indicator, target_ax = target_ax, color = param[strColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))

def PlotVR(param, df_data, target_ax, row_size, row_index):
    ax = plt.subplot2grid((row_size, 1), (row_index[0], 0), sharex = target_ax)
    row_index[0] += 1
    vr = GetVR(df_data[strClose], df_data[strVolume], int(param[strWindow]))
    PlotIndicator(vr, target_ax = ax, color = param[strColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))

    plt.setp(ax.get_xticklabels(), visible = False)
    ax.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    ax.set_ylabel(TechIndicatorPlotMode[strVR][strYlabel])

def PlotBollingerBands(param, df_data, target_ax, row_size, row_index):
    MA_mean = GetRollingMean(df_data[strClose], int(param[strWindow]))
    MA_std = GetRollingStd(df_data[strClose], int(param[strWindow]))
    IndicatorUpper, IndicatorLower = GetBollingerBands(MA_mean, MA_std)
    PlotIndicator(IndicatorUpper, target_ax = target_ax, color = param[strColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))
    PlotIndicator(IndicatorLower, target_ax = target_ax, color = param[strColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))
    target_ax.fill_between(df_data[strDate], IndicatorUpper, IndicatorLower, interpolate = True, color = param[strAreaColor] , alpha = float(param[strAreaAlpha]))


def PlotKDJ(param, df_data, target_ax, row_size, row_index):
    ax = plt.subplot2grid((row_size, 1), (row_index[0], 0), sharex = target_ax)
    row_index[0] += 1
    k, d, j = GetKDJ(df_data[strClose], df_data[strHigh], df_data[strLow], int(param[strWindow]))
    PlotIndicator(k, target_ax = ax, color = param[strKColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))
    PlotIndicator(d, target_ax = ax, color = param[strDColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))
    PlotIndicator(j, target_ax = ax, color = param[strJColor], linewidth = float(param[strLineWidth]), alpha = float(param[strAlpha]))

    basic_array1 = numpy.ones(len(df_data[strClose]))
    PlotIndicator(pandas.Series(basic_array1 * 80), target_ax = ax, color = 'grey', linewidth = 0.8, alpha = 0.8)
    PlotIndicator(pandas.Series(basic_array1 * 20), target_ax = ax, color = 'grey', linewidth = 0.8, alpha = 0.8)

    plt.setp(ax.get_xticklabels(), visible = False)
    ax.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    ax.set_ylabel(TechIndicatorPlotMode[strKDJ][strYlabel])

def PlotIndicator(df_data, target_ax, color, linewidth = 0.8, alpha = 0.8, kind = 'line'):
    df_data.plot(ax = target_ax, color = color, linewidth = linewidth, alpha = alpha, kind = kind)



ColorList = ['aqua', 'aquamarine', 'azure', 'beige', 'black', 'blue', 'brown', 'chartreuse', 'chocolate', 'coral', 'crimson', 'cyan', 'darkblue', 'darkgreen', 'fuchsia', 'gold', 'goldenrod', 'green'
             , 'grey', 'indigo', 'ivory', 'khaki', 'lavender', 'lightblue', 'lightgreen', 'lime', 'magenta', 'maroon', 'navy', 'olive', 'orange', 'orangered', 'orchid', 'pink', 'plum', 'purple', 'red'
             , 'salmon', 'sienna', 'silver', 'tan', 'teal', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'yellow', 'yellowgreen']

TechIndicatorFuncDict = {
    strATR:             {strFuncName: PlotATR, strParam:{strColor:'red', strWindow: 14, strLineWidth: 0.8, strAlpha: 0.8}},        
    strBollingerBands:  {strFuncName: PlotBollingerBands, strParam:{strColor:'grey', strWindow: 20, strLineWidth: 0.8, strAlpha: 0.8, strAreaColor: 'gold', strAreaAlpha:0.3}},
    strCCI:             {strFuncName: PlotCCI, strParam:{strColor:'blue', strOverBColor:'green',strOverSColor:'red', strWindow: 20, strLineWidth: 0.8, strAlpha: 0.8, strAreaAlpha:0.3}},    
    strDMA:             {strFuncName: PlotDMA, strParam:{strColor:'red', strShortWindow: 10, strLongWindow: 50, strLineWidth: 0.8, strAlpha: 0.8}},
    strDMI:             {strFuncName: PlotDMI, strParam:{strpDIColor:'green', strnDIColor:'red', strADXColor:'blue', strADXRColor:'lightgreen', strWindow: 14, strLineWidth: 0.8, strAlpha: 0.8}},        
    strEMA:             {strFuncName: PlotEMA, strParam:{strColor:'red', strWindow: 20, strLineWidth: 0.8, strAlpha: 0.8}},
    strKDJ:             {strFuncName: PlotKDJ, strParam:{strKColor:'red', strDColor:'black', strJColor:'gold', strWindow: 9, strLineWidth: 0.8, strAlpha: 0.8}},
    strMACD:            {strFuncName: PlotMACD, strParam:{strMACDColor:'red', strSignalColor:'purple', strBarIncColor:'green', strBarDecColor:'red', strWindow: 9, strLineWidth: 0.8, strAlpha: 0.8}},
    strMSTD:            {strFuncName: PlotMSTD, strParam:{strColor:'red', strWindow: 12, strLineWidth: 0.8, strAlpha: 0.8}},    
    strMVAR:            {strFuncName: PlotMVAR, strParam:{strColor:'red', strWindow: 12, strLineWidth: 0.8, strAlpha: 0.8}},    
    strRSI:             {strFuncName: PlotRSI, strParam:{strColor:'red', strWindow: 14, strLineWidth: 0.8, strAlpha: 0.8}},    
    strSMA:             {strFuncName: PlotSMA, strParam:{strColor:'red', strWindow: 20, strLineWidth: 0.8, strAlpha: 0.8}},
    strSMMA:            {strFuncName: PlotSMMA, strParam:{strColor:'red', strWindow: 20, strLineWidth: 0.8, strAlpha: 0.8}},
    strTEMA:            {strFuncName: PlotTEMA, strParam:{strColor:'red', strWindow: 9, strLineWidth: 0.8, strAlpha: 0.8}},        
    strTR:              {strFuncName: PlotTR, strParam:{strColor:'red', strLineWidth: 0.8, strAlpha: 0.8}},      
    strVR:              {strFuncName: PlotVR, strParam:{strColor:'red', strWindow: 26, strLineWidth: 0.8, strAlpha: 0.8}},        
    strWR:              {strFuncName: PlotWR, strParam:{strColor:'blue', strOverBColor:'green',strOverSColor:'red', strWindow: 14, strLineWidth: 0.8, strAlpha: 0.8, strAreaAlpha:0.3}},
}

TechIndicatorPlotMode = {
    strATR:             {strPlotInAxPrice: False, strYlabel:   strATR},    
    strBollingerBands:  {strPlotInAxPrice: True, strYlabel:   None},
    strCCI:             {strPlotInAxPrice: False, strYlabel:   strCCI},
    strDMA:             {strPlotInAxPrice: False, strYlabel:   strDMA},
    strDMI:             {strPlotInAxPrice: False, strYlabel:   strDMI},
    strEMA:             {strPlotInAxPrice: True, strYlabel:   None},
    strKDJ:             {strPlotInAxPrice: False, strYlabel:   strKDJ},
    strMACD:            {strPlotInAxPrice: False, strYlabel:   strMACD},
    strMSTD:            {strPlotInAxPrice: False, strYlabel:   strMSTD},
    strMVAR:            {strPlotInAxPrice: False, strYlabel:   strMVAR},
    strRSI:             {strPlotInAxPrice: False, strYlabel:   strRSI},
    strSMA:             {strPlotInAxPrice: True, strYlabel:   None},
    strSMMA:            {strPlotInAxPrice: True, strYlabel:   None},
    strTEMA:            {strPlotInAxPrice: True, strYlabel:   None},
    strTR:              {strPlotInAxPrice: False, strYlabel:   strTR},
    strVR:              {strPlotInAxPrice: False, strYlabel:   strVR},    
    strWR:              {strPlotInAxPrice: False, strYlabel:   strWR},
}

TechIndicatorWidgetParam = {
    strATR:             {strColor:  {strType:strComboBox, strValue:'red', strComboList: ColorList}, strWindow: {strType:strLineEdit, strValue:14}, strLineWidth: {strType:strLineEdit, strValue:0.8}, strAlpha: {strType:strLineEdit, strValue:0.8}},    
    strBollingerBands:  {strColor:  {strType:strComboBox, strValue:'grey', strComboList: ColorList}, strWindow: {strType:strLineEdit, strValue:20}, strLineWidth: {strType:strLineEdit, strValue:0.8}, strAlpha: {strType:strLineEdit, strValue:0.8}, strAreaColor:  {strType:strComboBox, strValue:'gold', strComboList: ColorList}, strAreaAlpha: {strType:strLineEdit, strValue:0.3}},
    strCCI:             {strColor:  {strType:strComboBox, strValue:'red', strComboList: ColorList}, strOverBColor:  {strType:strComboBox, strValue:'green', strComboList: ColorList}, strOverSColor:  {strType:strComboBox, strValue:'red', strComboList: ColorList}, strWindow: {strType:strLineEdit, strValue:20}, strLineWidth: {strType:strLineEdit, strValue:0.8}, strAlpha: {strType:strLineEdit, strValue:0.8}, strAreaAlpha: {strType:strLineEdit, strValue:0.3}},    
    strDMA:             {strColor:  {strType:strComboBox, strValue:'red', strComboList: ColorList}, strShortWindow: {strType:strLineEdit, strValue:10}, strLongWindow: {strType:strLineEdit, strValue:50}, strLineWidth: {strType:strLineEdit, strValue:0.8}, strAlpha: {strType:strLineEdit, strValue:0.8}},
    strDMI:             {strpDIColor:  {strType:strComboBox, strValue:'green', strComboList: ColorList}, strnDIColor:  {strType:strComboBox, strValue:'red', strComboList: ColorList}, strADXColor:  {strType:strComboBox, strValue:'blue', strComboList: ColorList}, strADXRColor:  {strType:strComboBox, strValue:'lightblue', strComboList: ColorList}, strWindow: {strType:strLineEdit, strValue:14}, strLineWidth: {strType:strLineEdit, strValue:0.8}, strAlpha: {strType:strLineEdit, strValue:0.8}},    
    strEMA:             {strColor:  {strType:strComboBox, strValue:'red', strComboList: ColorList}, strWindow: {strType:strLineEdit, strValue:20}, strLineWidth: {strType:strLineEdit, strValue:0.8}, strAlpha: {strType:strLineEdit, strValue:0.8}},
    strKDJ:             {strKColor: {strType:strComboBox, strValue:'red', strComboList: ColorList}, strDColor: {strType:strComboBox, strValue:'black', strComboList: ColorList}, strJColor: {strType:strComboBox, strValue:'gold', strComboList: ColorList}, strWindow: {strType:strLineEdit, strValue:9}, strLineWidth: {strType:strLineEdit, strValue:1}, strAlpha: {strType:strLineEdit, strValue:1}},
    strMACD:            {strMACDColor:   {strType:strComboBox, strValue:'red', strComboList: ColorList}, strSignalColor: {strType:strComboBox, strValue:'purple', strComboList: ColorList}, strBarIncColor:   {strType:strComboBox, strValue:'green', strComboList: ColorList}, strBarDecColor:   {strType:strComboBox, strValue:'red', strComboList: ColorList}, strFastWindow: {strType:strLineEdit, strValue:12}, strSlowWindow: {strType:strLineEdit, strValue:26}, strSignalWindow: {strType:strLineEdit, strValue:9}, strLineWidth: {strType:strLineEdit, strValue:1}, strAlpha: {strType:strLineEdit, strValue:1}},
    strMSTD:            {strColor:  {strType:strComboBox, strValue:'red', strComboList: ColorList}, strWindow: {strType:strLineEdit, strValue:20}, strLineWidth: {strType:strLineEdit, strValue:0.8}, strAlpha: {strType:strLineEdit, strValue:0.8}},
    strMVAR:            {strColor:  {strType:strComboBox, strValue:'red', strComboList: ColorList}, strWindow: {strType:strLineEdit, strValue:20}, strLineWidth: {strType:strLineEdit, strValue:0.8}, strAlpha: {strType:strLineEdit, strValue:0.8}},
    strRSI:             {strColor:  {strType:strComboBox, strValue:'red', strComboList: ColorList}, strWindow: {strType:strLineEdit, strValue:20}, strLineWidth: {strType:strLineEdit, strValue:0.8}, strAlpha: {strType:strLineEdit, strValue:0.8}},
    strSMA:             {strColor:  {strType:strComboBox, strValue:'red', strComboList: ColorList}, strWindow: {strType:strLineEdit, strValue:20}, strLineWidth: {strType:strLineEdit, strValue:0.8}, strAlpha: {strType:strLineEdit, strValue:0.8}},
    strSMMA:            {strColor:  {strType:strComboBox, strValue:'red', strComboList: ColorList}, strWindow: {strType:strLineEdit, strValue:20}, strLineWidth: {strType:strLineEdit, strValue:0.8}, strAlpha: {strType:strLineEdit, strValue:0.8}},
    strTEMA:            {strColor:  {strType:strComboBox, strValue:'red', strComboList: ColorList}, strWindow: {strType:strLineEdit, strValue:9}, strLineWidth: {strType:strLineEdit, strValue:0.8}, strAlpha: {strType:strLineEdit, strValue:0.8}},    
    strTR:              {strColor:  {strType:strComboBox, strValue:'red', strComboList: ColorList}, strLineWidth: {strType:strLineEdit, strValue:0.8}, strAlpha: {strType:strLineEdit, strValue:0.8}},    
    strVR:              {strColor:  {strType:strComboBox, strValue:'red', strComboList: ColorList}, strWindow: {strType:strLineEdit, strValue:26}, strLineWidth: {strType:strLineEdit, strValue:0.8}, strAlpha: {strType:strLineEdit, strValue:0.8}},    
    strWR:              {strColor:  {strType:strComboBox, strValue:'red', strComboList: ColorList}, strOverBColor:  {strType:strComboBox, strValue:'green', strComboList: ColorList}, strOverSColor:  {strType:strComboBox, strValue:'red', strComboList: ColorList}, strWindow: {strType:strLineEdit, strValue:14}, strLineWidth: {strType:strLineEdit, strValue:0.8}, strAlpha: {strType:strLineEdit, strValue:0.8}, strAreaAlpha: {strType:strLineEdit, strValue:0.3}},
}
