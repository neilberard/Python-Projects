# Imports
# from PySide2 import QtCore, QtWidgets, QtGui
from Interop.pyside.core.qt import QtCore, QtWidgets, QtGui, loadUiType
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import os
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Load UI File
ui_path = ui_file_name = os.path.dirname(__file__) + r'\rename_tools.ui'
FormClass, BaseClass = loadUiType(ui_file_name)


class RenameToolsWindow(QtWidgets.QMainWindow, FormClass):
    def __init__(self):
        maya_main = wrapInstance(long(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)  # GET MAIN MAYA WINDOW
        super(RenameToolsWindow, self).__init__(maya_main)  # PARENT WINDOW
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)  # DELETE WINDOW ON CLOSE
        self.windowName = 'RenameToolsWindow'
        log.info(self.__class__.__name__)

        self.setupUi(self)


    # @QtCore.Slot(): Decorator based on widget name that connects QT signal.
    @QtCore.Slot()
    def on_btn_unlock_attr_clicked(self):
        log.info('on_btn_unlock_attr_clicked, CLICKED')

    @QtCore.Slot()
    def on_btn_unlock_attr_clicked(self):
        log.info('on_btn_unlock_attr_clicked, CLICKED')


def showUI():
    try:
        rename_tools_window.close()
    except Exception:
        pass

    rename_tools_window = RenameToolsWindow()
    rename_tools_window.show()
    return rename_tools_window



"""Test Code"""
# if __name__ == '__main__':
#     app = QtWidgets.QApplication([])
#     win = ToolsWindow()
#     win.show()
#     app.exec_()

#C:\Program Files\Autodesk\Maya2017\bin\mayapy E:\Python_Projects\Projects\HacknSlash\python\ui\tools_window.py

# from Projects.HacknSlash.python.ui import tools_window_ui
# reload(tools_window_ui)
# win = tools_window_ui.ToolsWindow()
# win.show()
