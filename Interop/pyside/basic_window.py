import sys
from PySide2 import QtGui, QtCore, QtWidgets


def create_window():
    win = QtWidgets.QMainWindow()
    return win


app = QtWidgets.QApplication.instance()
win = create_window()
win.show()
app.exec_()

if __name__ == '__main__':
    pass
