from enum import Enum
from CommonDef.DefStr import *
import Program.GlobalVar as gv

import matplotlib.pyplot as plt

class Backtest(object):
    
    def __init__(self, Cash, ConsiderWorst,params):
        self.Position = 0
        self.Cash = Cash
        self.WorstTrading = ConsiderWorst
        self.StrategyParams = params[BacktestParam.strStrategyParams]
        
        self.TradeList = []
        
    def RunStrategy(self, BuyOrSellSignal, Strategy, params):
        
        if Strategy == BacktestParam.EasyStrategy:
            self.DoEasyStrategy(BuyOrSellSignal, params)
    
    def DoEasyStrategy(self, BuyOrSellSignal, params):
        
        BaseShare = self.StrategyParams[BacktestParam.perShareSize]
        
        if BuyOrSellSignal == BacktestParam.BuySignal:
            if self.WorstTrading == True:
                Price = params[strHigh]
            else:
                Price = params[strClose]
            
            if self.StrategyParams[BacktestParam.strBuyStrategy] == BacktestParam.BuyAll:
                Share = (int)(self.Cash / Price / BaseShare) * BaseShare
            elif self.StrategyParams[BacktestParam.strBuyStrategy] == BacktestParam.BuyFixed:
                Share = BaseShare
                
            cost = Price * Share
            if self.Cash > cost:                
                self.Cash -= cost
                self.Position += Share
                self.PushTradeList(BacktestParam.BuySignal, Share, params[strDate], Price)
        
        elif BuyOrSellSignal == BacktestParam.SellSignal:
            if self.WorstTrading == True:
                Price = params[strLow]
            else:
                Price = params[strClose]
                        
            if self.StrategyParams[BacktestParam.strSellStrategy] == BacktestParam.SellAll:
                Share = self.Position
            elif self.StrategyParams[BacktestParam.strBuyStrategy] == BacktestParam.SellFixed:
                Share = BaseShare
            
            if Share != 0:
                self.Cash += Share * Price
                self.Position -= Share
                self.PushTradeList(BacktestParam.SellSignal, Share, params[strDate], Price)

    def PushTradeList(self, signal, share, date, price):
        self.TradeList.append({BacktestParam.strSignal: signal, strShare: share, strDate: date, strPrice: price})
    
    def PrintTradeList(self):
        for trade_info in self.TradeList:
            if trade_info[BacktestParam.strSignal] == BacktestParam.BuySignal:
                print("Buy {0} share: {1}: {2}".format(trade_info[strShare], trade_info[strDate], trade_info[strPrice]))
            elif trade_info[BacktestParam.strSignal] == BacktestParam.SellSignal:
                print("Sell {0} share: {1}: {2}".format(trade_info[strShare], trade_info[strDate], trade_info[strPrice]))
    
    def PlotTradeChart(self, df_data):
        
        fig = plt.figure()
        fig.canvas.set_window_title('Wanna join the Axis Cult?')
        fig.suptitle('{0} ~ {1}'.format(df_data.index.min().strftime('%Y-%m-%d'), df_data.index.max().strftime('%Y-%m-%d')), y = 1, fontsize = 14)
    
        DefaultSize = fig.get_size_inches()
        fig.set_size_inches((DefaultSize[0] * gv.SettingArgs[StrChartSizeFactor], DefaultSize[1] * gv.SettingArgs[StrChartSizeFactor]))

        
        df_data[strClose].plot(kind = 'line', color = 'blue', linewidth = 0.5)
        
        for trade_info in self.TradeList:        
            if trade_info[BacktestParam.strSignal] == BacktestParam.BuySignal:
                plt.scatter(trade_info[strDate], trade_info[strPrice], marker='^', c='green')
                plt.annotate('  {0}'.format(trade_info[strShare]), xy=(trade_info[strDate], trade_info[strPrice]), color = 'green', fontsize='x-small')
            elif trade_info[BacktestParam.strSignal] == BacktestParam.SellSignal:
                plt.scatter(trade_info[strDate], trade_info[strPrice], marker='v', c = 'red')
                plt.annotate('  {0}'.format(trade_info[strShare]), xy=(trade_info[strDate], trade_info[strPrice]), color = 'red', fontsize='x-small')
        
        plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
        plt.tight_layout()
        plt.show()

class BacktestParam(Enum):
    # Signal:
    # --------------------------------------
    strSignal = 'Signal'
    BuySignal = 1
    SellSignal = 2
    # --------------------------------------
    
    # Options:
    # --------------------------------------
    # --------------------------------------    
    
    # Strategy Type:
    # --------------------------------------
    strStrategy = 'Strategy'
    EasyStrategy = 1
    # --------------------------------------
        
    # Strategy Params:
    # --------------------------------------
    strStrategyParams = 'StrategyParams'
    strBuyStrategy = 'BuyStrategy'
    strSellStrategy = 'SellStrategy'
    
    # EasyStrategy 
    BuyFixed = 1
    BuyAll = 2
    SellFixed = 1
    SellAll = 2
    
    perShareSize = 'perShareSize'
    # --------------------------------------
    