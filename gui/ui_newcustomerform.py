# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/newcustomerform.ui'
#
# Created: Sat Apr 12 19:19:00 2014
#      by: PyQt5 UI code generator 5.0.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewCustomerForm(object):
    def setupUi(self, NewCustomerForm):
        NewCustomerForm.setObjectName("NewCustomerForm")
        NewCustomerForm.resize(319, 120)
        NewCustomerForm.setMinimumSize(QtCore.QSize(0, 120))
        NewCustomerForm.setMaximumSize(QtCore.QSize(319, 16777215))
        self.horizontalLayout = QtWidgets.QHBoxLayout(NewCustomerForm)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(NewCustomerForm)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label = QtWidgets.QLabel(NewCustomerForm)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(NewCustomerForm)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(NewCustomerForm)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.lineEdit_2 = QtWidgets.QLineEdit(NewCustomerForm)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.lineEdit_2)
        self.lineEdit_3 = QtWidgets.QLineEdit(NewCustomerForm)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout_2.addWidget(self.lineEdit_3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(NewCustomerForm)
        QtCore.QMetaObject.connectSlotsByName(NewCustomerForm)

    def retranslateUi(self, NewCustomerForm):
        _translate = QtCore.QCoreApplication.translate
        NewCustomerForm.setWindowTitle(_translate("NewCustomerForm", "Form"))
        self.label_2.setText(_translate("NewCustomerForm", "Namn:"))
        self.label.setText(_translate("NewCustomerForm", "Adress:"))
        self.label_3.setText(_translate("NewCustomerForm", "Postnummer:"))

