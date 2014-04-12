# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/jobform.ui'
#
# Created: Sat Apr 12 19:19:00 2014
#      by: PyQt5 UI code generator 5.0.1
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
        self.lineEdit = QtWidgets.QLineEdit(self.inputBox)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.label_2 = QtWidgets.QLabel(self.inputBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.inputBox)
        self.lineEdit_2.setMaximumSize(QtCore.QSize(75, 16777215))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.label_3 = QtWidgets.QLabel(self.inputBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.inputBox)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(75, 0))
        self.lineEdit_3.setMaximumSize(QtCore.QSize(75, 16777215))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_2.addWidget(self.lineEdit_3)
        self.verticalLayout.addWidget(self.inputBox)

        self.retranslateUi(jobForm)
        QtCore.QMetaObject.connectSlotsByName(jobForm)

    def retranslateUi(self, jobForm):
        _translate = QtCore.QCoreApplication.translate
        jobForm.setWindowTitle(_translate("jobForm", "Form"))
        self.label.setText(_translate("jobForm", "Beskrivning:"))
        self.label_2.setText(_translate("jobForm", "Pris:"))
        self.label_3.setText(_translate("jobForm", "Antal:"))

