from PySide2 import QtUiTools
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import os

import pymel.core as pymel
from Interop.pyside.core.qt import QtCore, QtWidgets, loadUiType
from Interop.avatar_rig.perforce import p4_funcs
import logging

Slot = QtCore.Slot()
reload(p4_funcs)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

if not __name__ == '__main__':
    ui_file_name = os.path.dirname(__file__) + r'\p4_environment.ui'
else:
    ui_file_name = r'Interop\avatar_rig\perforce\p4_environment.ui'


FormClass, BaseClass = loadUiType(ui_file_name)


class Base(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Base, self).__init__(parent)


class P4Window(Base, FormClass):
    def __init__(self):
        maya_main = wrapInstance(long(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)  # GET MAIN MAYA WINDOW
        super(P4Window, self).__init__(maya_main)
        self.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)  # DELETE WINDOW ON CLOSE
        self.move(QtWidgets.QApplication.desktop().screen().rect().center() - self.rect().center())  # CENTER

        #Gathering USER INFO
        self.p4funcs = p4_funcs.P4Funcs()

        #IS USER LOGGED INTO P4?? Peforming check to make sure.
        if not self.p4funcs.get_login():
            dialog = 'Warning: User is not logged into Perforce, \n Either open P4V and login or open command prompt and type "p4 login"'
            log.error(dialog)
            pymel.confirmDialog(message=dialog)
            return

        self.environment_info = self.p4funcs.get_info()

        #Gathering Workspaces and adding them to a combo box, setting currentIndex to current workspace.
        try:
            self.workspaces = self.p4funcs.get_workspaces(self.environment_info['User name'])
            for item in self.workspaces:
                self.cb_P4CLIENT.addItem(item)

            index = self.cb_P4CLIENT.findText(self.environment_info['Client name'])
            if index:
                self.cb_P4CLIENT.setCurrentIndex(index)
        except KeyError:
            log.warning('no workspace found')

        try:
            self.line_P4PORT.setText(self.environment_info['Server address'])
        except KeyError:
            log.warning('no server found, please set server')

        try:
            self.line_P4USER.setText(self.environment_info['User name'])
        except KeyError:
            log.warning('need to set user')

    @Slot
    def on_btn_accept_clicked(self):
        self.p4funcs.set_port(self.line_P4PORT.text())  # SERVER
        self.p4funcs.set_user(self.line_P4USER.text())  # USER
        self.p4funcs.set_client(self.cb_P4CLIENT.currentText())  # WORKSPACE



