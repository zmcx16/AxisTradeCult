import os
import json
import pandas
import numpy

from Program.Common import *

RootPath = os.getcwd()
StockGroups = {}
StockGroupsSetting = 'StockGroups.setting'
StockGroupsSettingPath = os.path.join(RootPath,StockGroupsSetting)

StockDataPool = 'StockDataPool'
StockDataPoolPath = os.path.join(RootPath,StockDataPool)
    
def SaveStockGroups():
    with open(StockGroupsSettingPath, 'w') as f:
        json.dump(StockGroups, f)   

def ReadStockGroups(): 
    global StockGroups
    with open(StockGroupsSettingPath, 'r') as f:
        StockGroups = json.load(f)    
  
        
if os.path.isfile(StockGroupsSettingPath) == False:
    SaveStockGroups() 
