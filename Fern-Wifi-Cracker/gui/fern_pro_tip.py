# -*- coding: utf-8 -*-

#
# Created: Thu Aug 07 19:58:03 2014
#      by: PyQt5 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!
import os
from PyQt5.QtWidgets import *
from main_window import font_size
from PyQt5 import QtCore, QtWidgets, QtGui

font_setting = font_size()

try:
    _encoding = 0
    def _translate(context, text, disambig):
        return QtCore.QCoreApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtCore.QCoreApplication.translate(context, text, disambig)

class Fern_Pro_Tip_ui(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(413, 188)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("%s/resources/fern_pro.png"%(os.getcwd())))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem2)
        self.show_message_checkbox = QtWidgets.QCheckBox(Dialog)
        self.show_message_checkbox.setObjectName("show_message_checkbox")
        self.verticalLayout_3.addWidget(self.show_message_checkbox)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.yes_button = QtWidgets.QPushButton(Dialog)
        self.yes_button.setObjectName("yes_button")
        self.horizontalLayout.addWidget(self.yes_button)
        self.no_button = QtWidgets.QPushButton(Dialog)
        self.no_button.setObjectName("no_button")
        self.horizontalLayout.addWidget(self.no_button)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        self.no_button.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Fern Professional", None))
        self.label.setText(_translate("Dialog", "A professional version of Fern Wifi Cracker is now available", None))
        self.label_3.setText(_translate("Dialog", "Would you like to visit the website?", None))
        self.show_message_checkbox.setText(_translate("Dialog", "Don\'t show this message again", None))
        self.yes_button.setText(_translate("Dialog", "Yes", None))
        self.no_button.setText(_translate("Dialog", "No", None))

