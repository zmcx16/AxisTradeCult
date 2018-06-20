from enum import Enum
from CommonDef.DefStr import *

class Backtest(object):
    
    # Params Require:Cash, 
    def __init__(self, Cash, ConsiderWorst,params):
        self.Position = 0
        self.Cash = Cash
        self.WorstTrading = ConsiderWorst
        self.StrategyParams = params[BacktestParam.strStrategyParams]
        
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
                print("Buy {0} share: {1}: {2}".format(Share, params[strDate], Price))
        
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
                print("Sell {0} share: {1}: {2}".format(Share, params[strDate], Price))
        
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
    