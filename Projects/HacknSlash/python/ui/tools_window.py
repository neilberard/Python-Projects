# Imports
# from PySide2 import QtCore, QtWidgets, QtGui
from Interop.pyside.core.qt import QtCore, QtWidgets, QtGui, loadUiType
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import os
import logging

from Projects.HacknSlash.python.ui import rename_tools_window
from Projects.HacknSlash.python.project.libs import build_fk_ctrls


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Load UI File
ui_path = ui_file_name = os.path.dirname(__file__) + r'\nb_tools.ui'
FormClass, BaseClass = loadUiType(ui_file_name)


class ToolsWindow(QtWidgets.QMainWindow, FormClass):
    def __init__(self):
        maya_main = wrapInstance(long(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)  # GET MAIN MAYA WINDOW
        super(ToolsWindow, self).__init__(maya_main)  # PARENT WINDOW
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)  # DELETE WINDOW ON CLOSE
        log.info(self.__class__.__name__)
        self.setupUi(self)

    # @QtCore.Slot(): Decorator based on widget name that connects QT signal.
    @QtCore.Slot()
    def on_btn_unlock_attr_clicked(self):
        log.info('on_btn_unlock_attr_clicked, CLICKED')

    @QtCore.Slot()
    def on_btn_rename_clicked(self):
        rename_tools_window.showUI()
        log.info('on_btn_unlock_attr_clicked, CLICKED')


def showUI():
    for widget in QtWidgets.QApplication.allWidgets():
        if type(widget).__name__ == ToolsWindow.__name__:
            try:
                widget.close()
            except:
                pass
    rename_tools_window = ToolsWindow()
    rename_tools_window.show()


"""Test Code"""
# if __name__ == '__main__':
#     app = QtWidgets.QApplication([])
#     win = ToolsWindow()
#     win.show()
#     app.exec_()

#C:\Program Files\Autodesk\Maya2017\bin\mayapy E:\Python_Projects\Projects\HacknSlash\python\ui\tools_window.py

# from Projects.HacknSlash.python.ui import tools_window
# tools_window.showUI()

# reload(tools_window_ui)
# win = tools_window_ui.ToolsWindow()
# win.show()


