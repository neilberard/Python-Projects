from PySide2 import QtCore, QtWidgets, QtGui



class ToolsWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ToolsWindow, self).__init__()
        self.setObjectName("ToolsWindow")
        # self.resize(500, 500)

        self.container = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QHBoxLayout(self.container)
        self.container.setLayout(self.layout)
        self.textbox = QtWidgets.QLineEdit(self.container)
        self.layout.addWidget(self.textbox)


        # self.verticalLayout = QtWidgets.QVBoxLayout(self)




if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = ToolsWindow()
    win.show()
    app.exec_()

#C:\Program Files\Autodesk\Maya2017\bin\mayapy E:\Python_Projects\Projects\HacknSlash\python\ui\tools_window_ui.py



