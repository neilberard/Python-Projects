# Imports
# from PySide2 import QtCore, QtWidgets, QtGui
from PySide2 import QtCore, QtWidgets
from python.qt.Qt import loadUiType
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import os
import logging
import pymel.core as pymel

# Libs
from python.interop.utils import attr_utils
from python.libs import build_ctrls, joint_utils
from python.ui import ctrl_builder_window

reload(ctrl_builder_window)
reload(attr_utils)
reload(build_ctrls)
reload(joint_utils)


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
        attr_utils.unlock_attributes(nodes=pymel.selected())

    @QtCore.Slot()
    def on_btn_fk_ctrls_clicked(self):
        builder_window = ctrl_builder_window.showUI()

    @QtCore.Slot()
    def on_btn_rename_clicked(self):
        from python.HacknSlash.python.ui import rename_tools_window
        rename_tools_window.showUI()

    @QtCore.Slot()
    def on_btn_build_ikfk_clicked(self):
        with pymel.UndoChunk():
            joint_utils.build_ik_fk_joints(joints=pymel.selected())

    @QtCore.Slot()
    def on_btn_offset_transforms_clicked(self):
        with pymel.UndoChunk():
            joint_utils.create_offset_groups(objects=pymel.selected())

    @QtCore.Slot()
    def on_btn_delete_controls_clicked(self):
        pass
        # hs_clean.cleanup()

    @QtCore.Slot()
    def on_btn_make_switch_clicked(self):
        with pymel.UndoChunk():
            HS_IK.make_switch_utility(pymel.selected()[0])



def showUI():
    for widget in QtWidgets.QApplication.allWidgets():
        if type(widget).__name__ == ToolsWindow.__name__:
            try:
                widget.close()
            except:
                pass
    rename_tools_window = ToolsWindow()
    rename_tools_window.show()


"""test Code"""
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


