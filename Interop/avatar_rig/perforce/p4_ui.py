from PySide2 import QtUiTools
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
import os

from Interop.pyside.core.qt import QtCore, QtWidgets, loadUiType
from Interop.avatar_rig.perforce import p4_funcs
reload(p4_funcs)



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
        self.environment_info = self.p4funcs.get_info()
        self.workspaces = self.p4funcs.get_workspaces(self.environment_info['User name'])
        for item in self.workspaces:
            self.cb_P4CLIENT.addItem(item)

        index = self.cb_P4CLIENT.findText(self.environment_info['Client name'])
        if index:
            self.cb_P4CLIENT.setCurrentIndex(index)


        self.line_P4PORT.setText(self.environment_info['Server address'])
        self.line_P4USER.setText(self.environment_info['User name'])











    """Sample"""
    # @QtCore.Slot()
    # def on_clickMe_clicked(self):
    #     print 'CLICKED'


if __name__ == '__main__':
    P4_Window = P4Window()
    P4_Window.show()