# Imports
from Interop.pyside.core.qt import QtCore, QtWidgets, QtGui, loadUiType
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.OpenMaya as OpenMaya
import os
import logging
import pymel.core as pymel
from Projects.HacknSlash.python.project.libs import build_fk_ctrls
reload(build_fk_ctrls)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Load UI File
ui_path = ui_file_name = os.path.dirname(__file__) + r'\make_ctrl.ui'
FormClass, BaseClass = loadUiType(ui_file_name)


class ControlBuilderWindow(QtWidgets.QMainWindow, FormClass):
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

        # Ctrl_builder class
        self.ctrl_builder = build_fk_ctrls.ControlBuilder(pymel.selected())

        self.refresh()
        self.create_callbacks()

    def create_callbacks(self):
        """
        Setup the different maya callbacks that the UI need to be refreshed correctly
        """
        self.remove_callbacks()
        self.callback_events = [
            OpenMaya.MEventMessage.addEventCallback('SelectionChanged', self.refresh)]

    def remove_callbacks(self):
        """
        Remove all callabacks setup by the UI
        """
        for callback_id in self.callback_events:
            OpenMaya.MEventMessage.removeCallback(callback_id)
        self.callback_events = []

    # @QtCore.Slot(): Decorator based on widget name that connects QT signal.
    def refresh(self, *args):
        self.ctrl_builder.delete_ctrls()
        self.ctrl_builder.joints = pymel.selected()  # Set the joint selection and build the ctrl and joint dicts.
        self.ctrl_builder.set_ctrl_types(self.cb_shape.currentText())
        self.ctrl_builder.set_ctrl_matrices()
        self.ctrl_builder.create_ctrls()
        self.ctrl_builder.get_ctrl_distance()
        self.ctrl_builder.set_ctrl_sizes(self.sldr.value())


    @QtCore.Slot()
    def on_sldr_valueChanged(self):
        self.ctrl_builder.set_ctrl_sizes(self.sldr.value())

    @QtCore.Slot()
    def on_cb_shape_currentIndexChanged(self):
        self.remove_callbacks()
        self.refresh()
        self.create_callbacks()

    @QtCore.Slot()
    def on_btn_cancel_clicked(self):
        self.ctrl_builder.delete_ctrls()
        self.close()

    @QtCore.Slot()
    def on_btn_execute_clicked(self):
        log.info('on_btn_execute_clicked')
        self.ctrl_builder.publish_ctls()
        self.remove_callbacks()
        self.close()


    @QtCore.Slot()
    def closeEvent(self, *args):
        log.info('closing')
        self.ctrl_builder.delete_ctrls()
        self.remove_callbacks()

def showUI():
    for widget in QtWidgets.QApplication.allWidgets():
        if type(widget).__name__ == ControlBuilderWindow.__name__:
            try:
                widget.close()
            except:
                pass
    BuilderWindow = ControlBuilderWindow()
    BuilderWindow.show()


"""
Test code.
"""

# from Projects.HacknSlash.python.ui import ctrl_builder_window
# reload(ctrl_builder_window)


# app = QtWidgets.QApplication([])
# win = RenameToolsWindow()
# win.show()
# app.exec_()

