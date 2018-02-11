from PySide2 import QtUiTools
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import os

from Interop.pyside.core.qt import QtCore, QtWidgets, loadUiType
from Interop.pyside.core import ui_loader


ui_file_name = os.path.dirname(__file__) + r'\duplicator.ui'

def maya_main_window():
    """
    :return: Pointer to Maya Main Window. This is in order to Parent Widgets to .
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


def loadUiWidget(uifilename, parent=None):
    loader = QtUiTools.QUiLoader()
    uifile = QtCore.QFile(uifilename)
    uifile.open(QtCore.QFile.ReadOnly)
    ui = loader.load(uifile, parent)
    uifile.close()
    return ui


class UiLoader(QtUiTools.QUiLoader):
    _baseinstance = None

    def createWidget(self, classname, parent=None, name=''):
        if parent is None and self._baseinstance is not None:
            widget = self._baseinstance
        else:
            widget = super(UiLoader, self).createWidget(classname, parent, name)
            if self._baseinstance is not None:
                setattr(self._baseinstance, name, widget)
        return widget

    def loadUi(self, uifile, baseinstance=None):
        self._baseinstance = baseinstance
        widget = self.load(uifile)
        QtCore.QMetaObject.connectSlotsByName(widget)
        return widget


class MainWindowUIC(QtWidgets.QMainWindow):
    def __init__(self):
        MayaMain = wrapInstance(long(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
        super(MainWindowUIC, self).__init__(MayaMain)
        UiLoader().loadUi(ui_file_name, self)
        # self.listWidget.addItems(['Item {0}'.format(x) for x in range(100)])


class MainWindow_UI_LOADER(QtWidgets.QMainWindow):
    """Using Pyside Built-in UI loader"""

    def __init__(self):
        # mainUI = SCRIPT_LOC + "/templateUI/demoOne.ui"
        MayaMain = wrapInstance(long(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
        super(MainWindow_UI_LOADER, self).__init__(MayaMain)

        # main window load / settings
        self.MainWindowUI = loadUiWidget(ui_file_name, MayaMain)
        self.MainWindowUI.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        print type(self.MainWindowUI)


class MainWindow(QtWidgets.QMainWindow):  # USING PYSIDE_DYNAMIC
    def __init__(self):
        maya_main = wrapInstance(long(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)  # GET MAIN MAYA WINDOW
        super(MainWindow, self).__init__(maya_main)  # PARENT INSTANCE TO MAYA WINDOW
        self.ui = ui_loader.loadUi(ui_file_name, baseinstance=self)  # LOAD UI AND PARENT UI TO THIS INSTANCE
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)  # DELETE WINDOW ON CLOSE

    # @QtCore.Slot()
    # def on_clickMe_clicked(self):
    #     print 'CLICKED'


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



