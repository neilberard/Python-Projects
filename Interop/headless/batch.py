# import maya.standalone
# maya.standalone.initialize()
from PySide2 import QtWidgets, QtCore, QtGui


def create_window():
    win = QtWidgets.QMainWindow()
    return win

# cmds.file(new=True, force=True)
#
# cmds.file(rename='E:/Python_Projects/Interop/headless/save_scene.ma')
#
# cmds.file(save=True, force=True, type='mayaAscii')

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = create_window()
    win.show()
    app.exec_()

"""Test Code"""
# C:\Program Files\Autodesk\Maya2017\bin

# mayapy E:\Python_Projects\Interop\headle
# ss\batch.py