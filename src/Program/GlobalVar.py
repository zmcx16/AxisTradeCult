import os
import json
import pandas
import numpy

from Program.Common import *
from AxisPlot.Common import TechIndicatorFuncDict

RootPath = os.getcwd()

StockDataPool = 'StockDataPool'
StockDataPoolPath = os.path.join(RootPath,StockDataPool)

# StockGroups -------------------------------------------
StockGroups = {}
StockGroupsSetting = 'StockGroups.setting'
StockGroupsSettingPath = os.path.join(RootPath,StockGroupsSetting)

def SaveStockGroups():
    with open(StockGroupsSettingPath, 'w') as f:
        json.dump(StockGroups, f)   

def ReadStockGroups(): 
    global StockGroups
    with open(StockGroupsSettingPath, 'r') as f:
        StockGroups = json.load(f)    

def AddStockInGroup(GroupName,Symbol):
    global StockGroups    
    StockGroups[GroupName].append(Symbol)
    SaveStockGroups()

def ResetStockInGroup(GroupName,NewStockGroups):
    global StockGroups    
    StockGroups[GroupName] = NewStockGroups
    SaveStockGroups()

def AddStockGroup(GroupName):
    global StockGroups    
    StockGroups[GroupName] = []
    SaveStockGroups()

def DeleteStockGroup(GroupName):
    global StockGroups    
    del StockGroups[GroupName]
    SaveStockGroups()
#-------------------------------------------------------

# TechIndicatorGroups ----------------------------------
TechIndicatorGroups = {}
TechIndicatorGroupsSetting = 'TechIndicatorGroups.setting'
TechIndicatorGroupsSettingPath = os.path.join(RootPath,TechIndicatorGroupsSetting)
    
def SaveTechIndicatorGroups():
    with open(TechIndicatorGroupsSettingPath, 'w') as f:
        json.dump(TechIndicatorGroups, f)   

def ReadTechIndicatorGroups(): 
    global TechIndicatorGroups
    with open(TechIndicatorGroupsSettingPath, 'r') as f:
        TechIndicatorGroups = json.load(f)    

def AddTechIndicatorInGroup(GroupName,Indicator):
    global TechIndicatorGroups    
    TechIndicatorGroups[GroupName].append(Indicator)
    SaveTechIndicatorGroups()

def ResetTechIndicatorInGroup(GroupName,NewIndicatorGroups):
    global TechIndicatorGroups    
    TechIndicatorGroups[GroupName] = NewIndicatorGroups
    SaveTechIndicatorGroups()

def AddTechIndicatorGroup(GroupName):
    global TechIndicatorGroups    
    TechIndicatorGroups[GroupName] = []
    SaveTechIndicatorGroups()

def DeleteTechIndicatorGroup(GroupName):
    global TechIndicatorGroups    
    del TechIndicatorGroups[GroupName]
    SaveTechIndicatorGroups()    
#-------------------------------------------------------

if os.path.isfile(StockGroupsSettingPath) == False:
    SaveStockGroups() 

if os.path.isfile(TechIndicatorGroupsSettingPath) == False:
    SaveTechIndicatorGroups() 
