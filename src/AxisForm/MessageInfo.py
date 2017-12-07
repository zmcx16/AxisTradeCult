from PyQt5.QtWidgets import *

def showdialog(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    
    msg.setText(message['setText'])
    msg.setWindowTitle(message['setWindowTitle'])
    
    if message['setInformativeText'] is not 'None': 
        msg.setInformativeText(message['setInformativeText'])
    
    if message['setDetailedText'] is not 'None':
        msg.setDetailedText(message['setDetailedText'])
        
    msg.setStandardButtons(QMessageBox.Ok)
        
    return  msg.exec_()


Str_setText = 'setText'
Str_setInformativeText = 'setInformativeText'
Str_setWindowTitle = 'setWindowTitle'
Str_setDetailedText = 'setDetailedText'

AddStockAlreadySymbolMessage = {
    Str_setText:                'The {0} already exist this stock: {1}',
    Str_setInformativeText:     'None',
    Str_setWindowTitle:         'Warning!!',
    Str_setDetailedText:        'None'
}

AddStockDownloadFailMessage = {
    Str_setText:                'Download Stock {0} fail in Quandl',
    Str_setInformativeText:     'None',
    Str_setWindowTitle:         'Warning!!',
    Str_setDetailedText:        'None'
}

