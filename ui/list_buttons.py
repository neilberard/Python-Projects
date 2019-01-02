from PySide2 import QtCore, QtWidgets  # So pycharm with reconize QT symbols


class Window(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.list = QtWidgets.QListWidget(self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.list)

    def addListItem(self, text):
        item = QtWidgets.QListWidgetItem(text)
        self.list.addItem(item)
        widget = QtWidgets.QWidget(self.list)
        button = QtWidgets.QToolButton(widget)
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()
        layout.addWidget(button)
        self.list.setItemWidget(item, widget)
        button.clicked[()].connect(
            lambda: self.handleButtonClicked(item))

    def handleButtonClicked(self, item):
        print(item.text())

if __name__ == '__main__':



    window = Window()
    for label in 'red blue green yellow purple'.split():
        window.addListItem(label)
    window.setGeometry(500, 300, 300, 200)
    window.show()
