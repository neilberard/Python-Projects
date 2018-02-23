# Imports
from Interop.pyside.core.qt import QtCore, QtWidgets, QtGui, loadUiType
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
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
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)  # DELETE WINDOW ON CLOSE
        self.setupUi(self)
        self.setWindowTitle(type(self).__name__)
        self.resize(self.vlayout.sizeHint())  # Resize to widgets

        # Ctrl_builder class
        self.ctrl_builder = build_fk_ctrls.ControlBuilder(pymel.selected())

        self.ctrl_builder.set_ctrl_type(self.cb_shape.currentText())
        self.ctrl_builder.create_ctrls()
        self.ctrl_builder.set_ctrl_size(self.sldr.value())


    # @QtCore.Slot(): Decorator based on widget name that connects QT signal.

    @QtCore.Slot()
    def on_sldr_valueChanged(self):
        print self.sldr.value()
        self.ctrl_builder.set_ctrl_size(self.sldr.value())


    @QtCore.Slot()
    def on_cb_shape_currentIndexChanged(self):
        self.ctrl_builder.delete_ctrls()

        self.ctrl_builder.joints = pymel.selected()  # Set the joint selection and build the ctrl and joint dicts.
        self.ctrl_builder.set_ctrl_type(self.cb_shape.currentText())
        self.ctrl_builder.set_ctrl_matrix()

        self.ctrl_builder.create_ctrls()

        self.ctrl_builder.set_ctrl_size(self.sldr.value())


        log.info('on_cb_shape_currentIndexChange')

    @QtCore.Slot()
    def on_btn_cancel_clicked(self):
        self.ctrl_builder.delete_ctrls()

    @QtCore.Slot()
    def focusOutEvent(self, *args):
        print 'lost_focus'


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

