# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/jobform.ui'
#
# Created: Mon Feb 23 20:51:24 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_jobForm(object):
    def setupUi(self, jobForm):
        jobForm.setObjectName("jobForm")
        jobForm.resize(670, 81)
        self.verticalLayout = QtWidgets.QVBoxLayout(jobForm)
        self.verticalLayout.setObjectName("verticalLayout")
        self.inputBox = QtWidgets.QGroupBox(jobForm)
        self.inputBox.setTitle("")
        self.inputBox.setObjectName("inputBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.inputBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.inputBox)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.description = QtWidgets.QLineEdit(self.inputBox)
        self.description.setObjectName("description")
        self.horizontalLayout_2.addWidget(self.description)
        self.label_2 = QtWidgets.QLabel(self.inputBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.price = QtWidgets.QLineEdit(self.inputBox)
        self.price.setMaximumSize(QtCore.QSize(75, 16777215))
        self.price.setObjectName("price")
        self.horizontalLayout_2.addWidget(self.price)
        self.label_3 = QtWidgets.QLabel(self.inputBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.number = QtWidgets.QLineEdit(self.inputBox)
        self.number.setMinimumSize(QtCore.QSize(75, 0))
        self.number.setMaximumSize(QtCore.QSize(75, 16777215))
        self.number.setObjectName("number")
        self.horizontalLayout_2.addWidget(self.number)
        self.verticalLayout.addWidget(self.inputBox)

        self.retranslateUi(jobForm)
        QtCore.QMetaObject.connectSlotsByName(jobForm)

    def retranslateUi(self, jobForm):
        _translate = QtCore.QCoreApplication.translate
        jobForm.setWindowTitle(_translate("jobForm", "Form"))
        self.label.setText(_translate("jobForm", "Beskrivning:"))
        self.label_2.setText(_translate("jobForm", "Pris:"))
        self.label_3.setText(_translate("jobForm", "Antal:"))

