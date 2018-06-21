import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import os
import logging
import pymel.core as pymel

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

from PySide2 import QtCore, QtWidgets  # So pycharm with reconize QT symbols
from Interop.pyside.core.qt import QtCore, QtWidgets, loadUiType

from libs import make_planer
reload(make_planer)

ui_file_name = os.path.dirname(__file__) + r'\make_planer.ui'
FormClass, BaseClass = loadUiType(ui_file_name)


class Base(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Base, self).__init__(parent)


class Make_Planer_Window(Base, FormClass):
    def __init__(self):
        maya_main = wrapInstance(long(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)  # GET MAIN MAYA WINDOW
        super(Make_Planer_Window, self).__init__(maya_main)
        self.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)  # DELETE WINDOW ON CLOSE
        self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center())  # CENTER

        # Hide Axes radio button group
        self.fm_radio_buttons.hide()
        self.resize(self.verticalLayout.totalSizeHint())

    @QtCore.Slot()
    def on_cb_mode_currentIndexChanged(self):
        if self.cb_mode.currentText() == 'Choose Axis':
            self.fm_radio_buttons.show()
            self.resize(self.verticalLayout.totalSizeHint())

        else:
            self.fm_radio_buttons.hide()
            self.resize(self.verticalLayout.totalSizeHint())


    @QtCore.Slot()
    def on_btn_ok_clicked(self):
        print 'btn_ok_clicked'
        with pymel.UndoChunk():
            make_planer.project_vertex(mode=self.cb_mode.currentText(), x=self.rb_x.isChecked(), y=self.rb_y.isChecked(), z=self.rb_z.isChecked())


    @QtCore.Slot()
    def on_btn_cancel_clicked(self):
        print 'btn_cancel_clicked'
        self.close()

    def eventFilter(self, obj, event):
        log.info(event)


def showUI():
    for widget in QtWidgets.QApplication.allWidgets():
        if type(widget).__name__ == Make_Planer_Window.__name__:
            try:
                widget.close()
            except:
                pass
    window = Make_Planer_Window()
    window.show()
