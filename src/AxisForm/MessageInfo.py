from PyQt5.QtWidgets import *

dialog_return = ""


def BaseMessageBox(msg, message):
    msg.setText(message['setText'])
    msg.setWindowTitle(message['setWindowTitle'])

    if message['setInformativeText'] is not 'None':
        msg.setInformativeText(message['setInformativeText'])

    if message['setDetailedText'] is not 'None':
        msg.setDetailedText(message['setDetailedText'])


def ShowInfoDialog(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setStandardButtons(QMessageBox.Ok)

    BaseMessageBox(msg, message)

    msg.buttonClicked.connect(msgbtn)
    msg.exec_()
    return  dialog_return


def ShowWarningDialog(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    BaseMessageBox(msg, message)

    msg.buttonClicked.connect(msgbtn)
    msg.exec_()
    return  dialog_return


def msgbtn(i):
    global dialog_return
    dialog_return = i.text()


Str_setText = 'setText'
Str_setInformativeText = 'setInformativeText'
Str_setWindowTitle = 'setWindowTitle'
Str_setDetailedText = 'setDetailedText'

AddStockAlreadySymbolMessage = {
    Str_setText:                'The {0} already exist this stock: {1}',
    Str_setInformativeText:     'None',
    Str_setWindowTitle:         'Info',
    Str_setDetailedText:        'None'
}

AddStockDownloadFailMessage = {
    Str_setText:                'Download Stock {0} fail in Quandl',
    Str_setInformativeText:     'None',
    Str_setWindowTitle:         'Info',
    Str_setDetailedText:        'None'
}

DeleteGroupWarningMessage = {
    Str_setText:                'Warning!! Are you sure you want to delete "{0}" Group?',
    Str_setInformativeText:     'None',
    Str_setWindowTitle:         'Warning!!',
    Str_setDetailedText:        'Include below :\n{0}'
}
