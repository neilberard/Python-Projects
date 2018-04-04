# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/rll/packages/omtk/9.9.9/omtk/ui/widget_list_influences.ui'
#
# Created: Sun Oct 16 11:09:23 2016
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

try:
    from PySide2 import QtCore, QtGui, QtWidgets
except:
    from omtk.qt.qt import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(316, 295)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_search = QtWidgets.QLineEdit(Form)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.horizontalLayout.addWidget(self.lineEdit_search)
        self.btn_update = QtWidgets.QPushButton(Form)
        self.btn_update.setObjectName("btn_update")
        self.horizontalLayout.addWidget(self.btn_update)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.checkBox_hideAssigned = QtWidgets.QCheckBox(Form)
        self.checkBox_hideAssigned.setChecked(True)
        self.checkBox_hideAssigned.setObjectName("checkBox_hideAssigned")
        self.verticalLayout.addWidget(self.checkBox_hideAssigned)
        self.treeWidget = QtWidgets.QTreeWidget(Form)
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.treeWidget.header().setVisible(False)
        self.verticalLayout.addWidget(self.treeWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None))
        self.btn_update.setText(QtWidgets.QApplication.translate("Form", "Update", None))
        self.checkBox_hideAssigned.setText(QtWidgets.QApplication.translate("Form", "Hide Assigned", None))

