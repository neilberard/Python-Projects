from PySide2 import QtCore, QtWidgets, QtGui


class ToolsWindowUi(object):

    def setupUi(self, ToolsWindow):
        """
        :param ToolsWindow: Subclass caller passing itself.
        :return:
        """
        ToolsWindow.setObjectName("AnimationExporterUi")
        ToolsWindow.resize(500, 500)


class ToolsWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ToolsWindow).__init__(self)
        self.setObjectName("ToolsWIndow")

def create_window():
    return QtWidgets.QMainWindow()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = create_window()
    win.show()
    app.exec_()

#C:\Program Files\Autodesk\Maya2017\bin>mayapy E:\Python_Projects\Projects\HacknSlash\python\ui\tools_window_ui.py



