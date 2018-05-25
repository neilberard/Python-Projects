# Imports
# from PySide2 import QtCore, QtWidgets, QtGui
from PySide2 import QtCore, QtWidgets, QtGui
from python.qt.Qt import loadUiType
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import os
import logging
import pymel.core as pymel

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Load UI File
ui_path = ui_file_name = os.path.dirname(__file__) + r'\rename_tools.ui'
FormClass, BaseClass = loadUiType(ui_file_name)


class RenameToolsWindow(QtWidgets.QMainWindow, FormClass):
    def __init__(self):
        maya_main = None
        try:
            maya_main = wrapInstance(long(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)  # GET MAIN MAYA WINDOW
        except:
            pass
        super(RenameToolsWindow, self).__init__(maya_main)  # PARENT WINDOW
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)  # DELETE WINDOW ON CLOSE
        self.setupUi(self)
        self.setWindowTitle(type(self).__name__)
        self.btn_execute.setText('Replace')

        self.resize(self.vlayout.sizeHint())

    # @QtCore.Slot(): Decorator based on widget name that connects QT signal.
    @QtCore.Slot()
    def on_cb_mode_currentIndexChanged(self):
        # Replace
        if self.cb_mode.currentText() == 'Replace':
            self.ln_find.show()
            self.lbl_find.show()
            self.ln_replace.show()
            self.lbl_replace.show()
            self.lbl_replace.setText('Replace')
            self.btn_execute.setText('Replace')

        #  Rename
        if self.cb_mode.currentText() == 'Rename':
            self.ln_find.hide()
            self.lbl_find.hide()
            self.ln_replace.show()
            self.lbl_replace.hide()
            self.btn_execute.setText('Rename')

        #  Add Prefix
        if self.cb_mode.currentText() == 'Add Prefix':
            self.ln_find.hide()
            self.lbl_find.hide()
            self.ln_replace.show()
            self.lbl_replace.hide()
            self.lbl_replace.setText('Prefix')
            self.btn_execute.setText('Add Prefix')

        #  Add Suffix
        if self.cb_mode.currentText() == 'Add Suffix':
            self.ln_find.hide()
            self.lbl_find.hide()
            self.ln_replace.show()
            self.lbl_replace.hide()
            self.lbl_replace.setText('Suffix')
            self.btn_execute.setText('Add Suffix')

        # Resize the window match shown child widgets.
        self.resize(self.width(), self.vlayout.sizeHint().height())

    @QtCore.Slot()
    def on_btn_execute_clicked(self):
        self.rename(selection=pymel.selected())

    @QtCore.Slot()
    def on_btn_cancel_clicked(self):
        self.close()

    def rename(self, selection=None):
        if self.cb_mode.currentText() == 'Replace':
            for item in selection:
                item.rename(item.name().replace(self.ln_find.text(), self.ln_replace.text()))

        if self.cb_mode.currentText() == 'Rename':
            for item in selection:
                item.rename(self.ln_replace.text())

        if self.cb_mode.currentText() == 'Add Prefix':
            for item in selection:
                item.rename(self.ln_replace.text() + item.name())

        if self.cb_mode.currentText() == 'Add Suffix':
            for item in selection:
                item.rename(item.name() + self.ln_replace.text())


def showUI():
    for widget in QtWidgets.QApplication.allWidgets():
        if type(widget).__name__ == RenameToolsWindow.__name__:
            try:
                widget.close()
            except:
                pass
    rename_tools_window = RenameToolsWindow()
    rename_tools_window.show()


showUI()


"""
test code.
"""
# app = QtWidgets.QApplication([])
# win = RenameToolsWindow()
# win.show()
# app.exec_()


# C:\Program Files\Autodesk\Maya2017\bin\mayapy E:\Python_Projects\Projects\AutoRig\python\ui\rename_tools_window.py

# from Projects.AutoRig.python.ui import rename_tools_window
# reload(rename_tools_window)
# win = rename_tools_window.ToolsWindow()
# win.show()
