import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import os
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

from Interop.pyside.core.qt import QtCore, QtWidgets, loadUiType


ui_file_name = os.path.dirname(__file__) + r'\duplicator.ui'
FormClass, BaseClass = loadUiType(ui_file_name)


class Base(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Base, self).__init__(parent)


class MainWindow2(Base, FormClass):
    def __init__(self):
        maya_main = wrapInstance(long(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)  # GET MAIN MAYA WINDOW
        super(MainWindow2, self).__init__(maya_main)
        self.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)  # DELETE WINDOW ON CLOSE
        self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center())  # CENTER

    @QtCore.Slot()
    def on_clickMe_clicked(self):
        print 'CLICKED'

    def eventFilter(self, obj, event):
        log.info(event)




