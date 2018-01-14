from PySide2 import QtCore, QtGui, QtWidgets, QtUiTools
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import os

uifilename = os.path.dirname(__file__) + r'\basic_window.ui'


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


def loadUiWidget(uifilename, parent=None):
    loader = QtUiTools.QUiLoader()
    uifile = QtCore.QFile(uifilename)
    uifile.open(QtCore.QFile.ReadOnly)
    ui = loader.load(uifile, parent)
    uifile.close()
    return ui


class templateUiDemo(QtWidgets.QMainWindow):
    """A bare minimum UI class - showing a .ui file inside Maya 2016"""

    def __init__(self):
        # mainUI = SCRIPT_LOC + "/templateUI/demoOne.ui"
        MayaMain = wrapInstance(long(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
        super(templateUiDemo, self).__init__(MayaMain)

        # main window load / settings
        self.MainWindowUI = loadUiWidget(uifilename, MayaMain)
        self.MainWindowUI.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)




