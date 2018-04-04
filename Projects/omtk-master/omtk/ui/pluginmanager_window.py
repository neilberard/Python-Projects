# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/packages/omtk/9.9.9/omtk/ui/pluginmanager_window.ui'
#
# Created: Sun Oct 16 11:09:23 2016
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

try:
    from PySide2 import QtCore, QtGui, QtWidgets
except:
    from omtk.qt.qt import QtCore, QtGui, QtWidgets

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(485, 391)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit_search = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.verticalLayout.addWidget(self.lineEdit_search)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_reload = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_reload.setObjectName("pushButton_reload")
        self.horizontalLayout.addWidget(self.pushButton_reload)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 485, 28))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.actionReload = QtWidgets.QAction(mainWindow)
        self.actionReload.setObjectName("actionReload")
        self.actionSearchQueryChanged = QtWidgets.QAction(mainWindow)
        self.actionSearchQueryChanged.setObjectName("actionSearchQueryChanged")

        self.retranslateUi(mainWindow)
        QtCore.QObject.connect(self.pushButton_reload, QtCore.SIGNAL("released()"), self.actionReload.trigger)
        QtCore.QObject.connect(self.lineEdit_search, QtCore.SIGNAL("textChanged(QString)"), self.actionSearchQueryChanged.trigger)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QtWidgets.QApplication.translate("mainWindow", "OMTK - Plugin Manager", None))
        self.pushButton_reload.setText(QtWidgets.QApplication.translate("mainWindow", "Reload", None))
        self.actionReload.setText(QtWidgets.QApplication.translate("mainWindow", "Reload", None))
        self.actionSearchQueryChanged.setText(QtWidgets.QApplication.translate("mainWindow", "SearchQueryChanged", None))

