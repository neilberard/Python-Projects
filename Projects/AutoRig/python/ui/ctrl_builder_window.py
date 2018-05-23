# Imports
from PySide2 import QtCore, QtWidgets
from python.qt.Qt import loadUiType
from python.qt.Qt import QtCore, QtWidgets

from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.OpenMaya as OpenMaya
import os
import logging
import pymel.core as pymel
from python.libs import build_ctrls, shapes

reload(build_ctrls)
reload(shapes)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Load UI File
ui_path = ui_file_name = os.path.dirname(__file__) + r'\make_ctrl.ui'
FormClass, BaseClass = loadUiType(ui_file_name)


class ControlBuilderWindow(QtWidgets.QMainWindow, FormClass):
    """
    Note: Remove callbacks whenever executing code that changes the selection.
    """

    def __init__(self):
        maya_main = None
        try:
            maya_main = wrapInstance(long(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)  # GET MAIN MAYA WINDOW
        except:
            pass
        super(ControlBuilderWindow, self).__init__(maya_main)  # PARENT WINDOW
        self.callback_events = []
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)  # DELETE WINDOW ON CLOSE
        self.setupUi(self)
        self.setWindowTitle(type(self).__name__)
        self.resize(self.vlayout.sizeHint())  # Resize to widgets
        # Get shape list
        self.shape_list = shapes.remove_file_extension()
        self.cb_shape.blockSignals(True)  # Block combobox from sending signals when updating index.
        self.cb_shape.insertItems(0, self.shape_list)
        self.cb_shape.blockSignals(False)

        self.axis = 'x'  # Orientation of the controller
        self.refresh()

    # @QtCore.Slot(): Decorator based on widget name that connects QT signal.
    def refresh(self, *args):
        # Ctrl_builder class
        self.ctrl_builder = build_ctrls.ControlBuilder(pymel.selected())
        self.ctrl_builder.set_ctrl_types(self.cb_shape.currentText())
        self.ctrl_builder.set_ctrl_matrices()
        self.ctrl_builder.set_ctrl_axis(self.axis)
        self.ctrl_builder.set_ctrl_sizes(self.sldr.value() * .01)
    @QtCore.Slot()
    def on_chk_parent_constraint_stateChanged(self):
        if self.chk_parent_constraint.checkState() == QtCore.Qt.CheckState.Checked:
            self.ctrl_builder.parent_constraint = True
        else:
            self.ctrl_builder.parent_constraint = False

    @QtCore.Slot()
    def on_btn_axis_x_clicked(self):
        self.axis = 'x'
        self.ctrl_builder.set_ctrl_axis(self.axis) 

    @QtCore.Slot()
    def on_btn_axis_y_clicked(self):
        self.axis = 'y'
        self.ctrl_builder.set_ctrl_axis(self.axis)

    @QtCore.Slot()
    def on_btn_axis_z_clicked(self):
        self.axis = 'z'
        self.ctrl_builder.set_ctrl_axis(self.axis)

    @QtCore.Slot()
    def on_sldr_valueChanged(self):
        self.ctrl_builder.set_ctrl_sizes(self.sldr.value() * .01)

    @QtCore.Slot()
    def on_cb_shape_currentIndexChanged(self):
        self.ctrl_builder.set_ctrl_types(self.cb_shape.currentText())

    @QtCore.Slot()
    def on_btn_cancel_clicked(self):
        self.ctrl_builder.delete_ctrls()
        self.close()

    @QtCore.Slot()
    def on_btn_execute_clicked(self):
        log.info('on_btn_execute_clicked')
        self.ctrl_builder.ctrls = []
        self.close()

    @QtCore.Slot()
    def closeEvent(self, *args):
        log.info('closing')
        self.ctrl_builder.delete_ctrls()


def showUI():
    for widget in QtWidgets.QApplication.allWidgets():
        if type(widget).__name__ == ControlBuilderWindow.__name__:
            try:
                widget.close()
            except:
                pass
    BuilderWindow = ControlBuilderWindow()
    BuilderWindow.show()
    return BuilderWindow


"""
test code.
"""

# from Projects.AutoRig.python.ui import ct
# rl_builder_window
# reload(ctrl_builder_window)


# app = QtWidgets.QApplication([])
# win = RenameToolsWindow()
# win.show()
# app.exec_()

