import os
import json

from Program.Resources import *
from Program.Common import *
from Program.DefStr import *

RootPath = os.getcwd()

StockDataPool = 'StockDataPool'
StockDataPoolPath = os.path.join(RootPath, StockDataPool)

ImagePath = os.path.join(os.path.dirname(RootPath), 'Image')
ImgTsubasaPath = os.path.join(ImagePath, imgTsubasa)

# StockGroups -------------------------------------------
StockGroups = {}
# {"List1": ["T", "GOOG", "AAPL"]
#, "List2": ["T", "DPZ", "GOOG", "AMZN", "WDC", "STX"]}
StockGroupsSetting = 'StockGroups.setting'
StockGroupsSettingPath = os.path.join(RootPath, StockGroupsSetting)


def SaveStockGroups():
    with open(StockGroupsSettingPath, 'w') as f:
        json.dump(StockGroups, f)


def ReadStockGroups():
    global StockGroups
    with open(StockGroupsSettingPath, 'r') as f:
        StockGroups = json.load(f)


def AddStockInGroup(GroupName, Symbol):
    global StockGroups
    StockGroups[GroupName].append(Symbol)
    SaveStockGroups()


def ResetStockInGroup(GroupName, NewStockGroups):
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
# {"TechIndicator1": [{"Name": "BollingerBands", "AreaAlpha": "0.3", "AreaColor": "purple", "Alpha": "0.8", "LineWidth": "0.8", "Window": "20", "Color": "lightblue"}, {"Name": "MA", "Alpha": "0.8", "LineWidth": "0.8", "Window": "20", "Color": "violet"}]
#, "TechList2": [{"Name": "MA", "Alpha": "0.8", "LineWidth": "0.8", "Window": "20", "Color": "azure"}]}
TechIndicatorGroupsSetting = 'TechIndicatorGroups.setting'
TechIndicatorGroupsSettingPath = os.path.join(
    RootPath, TechIndicatorGroupsSetting)


def SaveTechIndicatorGroups():
    with open(TechIndicatorGroupsSettingPath, 'w') as f:
        json.dump(TechIndicatorGroups, f)


def ReadTechIndicatorGroups():
    global TechIndicatorGroups
    with open(TechIndicatorGroupsSettingPath, 'r') as f:
        TechIndicatorGroups = json.load(f)


def AddTechIndicatorInGroup(GroupName, Indicator):
    global TechIndicatorGroups
    TechIndicatorGroups[GroupName].append(Indicator)
    SaveTechIndicatorGroups()


def ResetTechIndicatorInGroup(GroupName, NewIndicatorGroups):
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


# GlobalSetting ----------------------------------
SettingArgs = {StrChartSizeFactor: 1.8}
SettingArgsSetting = 'SettingArgs.setting'
SettingArgsSettingPath = os.path.join(RootPath, SettingArgsSetting)


def SaveSettingArgs():
    with open(SettingArgsSettingPath, 'w') as f:
        json.dump(SettingArgs, f)


def ReadSettingArgs():
    global SettingArgs
    with open(SettingArgsSettingPath, 'r') as f:
        SettingArgs = json.load(f)

#-------------------------------------------------------


if os.path.isfile(StockGroupsSettingPath) == False:
    SaveStockGroups()

if os.path.isfile(TechIndicatorGroupsSettingPath) == False:
    SaveTechIndicatorGroups()

if os.path.isfile(SettingArgsSettingPath) == False:
    SaveSettingArgs()
