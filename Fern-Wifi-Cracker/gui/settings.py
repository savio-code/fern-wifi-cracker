# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created: Thu Oct 14 08:16:19 2010
#      by: PyQt5 UI code generator 4.7.7
#
# WARNING! All changes made in this file will be lost!
import os
from PyQt5.QtWidgets import *
from main_window import font_size
from PyQt5 import QtCore, QtWidgets, QtGui

font_setting = font_size()

class settings(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(427, 133)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("%s/resources/wifi_5.png"%(os.getcwd())), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(-20, 90, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
	font = QtGui.QFont()
	font.setPointSize(font_setting)
	self.buttonBox.setFont(font)
        self.channel_combobox = QtWidgets.QComboBox(Dialog)
        self.channel_combobox.setGeometry(QtCore.QRect(170, 20, 121, 21))
        self.channel_combobox.setObjectName("channel_combobox")
	font = QtGui.QFont()
	font.setPointSize(font_setting)
	self.channel_combobox.setFont(font)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(110, 20, 61, 16))
        self.label.setObjectName("label")
	font = QtGui.QFont()
	font.setPointSize(font_setting)
	self.label.setFont(font)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, -10, 91, 111))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("%s/resources/radio-wireless-signal-icone-5919-96.png"%(os.getcwd())))
        self.label_2.setObjectName("label_2")
	font = QtGui.QFont()
	font.setPointSize(font_setting)
	self.label_2.setFont(font)
        self.xterm_checkbox = QtWidgets.QCheckBox(Dialog)
        self.xterm_checkbox.setGeometry(QtCore.QRect(300, 20, 171, 17))
        self.xterm_checkbox.setObjectName("xterm_checkbox")
	font = QtGui.QFont()
	font.setPointSize(font_setting)
	self.xterm_checkbox.setFont(font)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(110, 50, 311, 16))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.label_3.setFont(font)
	font = QtGui.QFont()
	font.setPointSize(font_setting)
	self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 90, 101, 16))
        self.label_4.setObjectName("label_4")
	font = QtGui.QFont()
	font.setPointSize(font_setting)
	self.label_4.setFont(font)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(100, 90, 46, 13))
	font = QtGui.QFont()
	font.setPointSize(font_setting)
	self.label_5.setFont(font)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(False)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtCore.QCoreApplication.translate("Dialog", "Access Point Scan Preferences", None, 0))
        self.label.setText(QtCore.QCoreApplication.translate("Dialog", "Channel:", None, 0))
        self.xterm_checkbox.setText(QtCore.QCoreApplication.translate("Dialog", "Enable XTerms", None, 0))
        self.label_3.setText(QtCore.QCoreApplication.translate("Dialog", "Automatic scan to all channels is Default without XTerm", None, 0))
        self.label_4.setText(QtCore.QCoreApplication.translate("Dialog", "\t <font color=green>Activated</font>", None, 0))
        self.label_5.setText(QtCore.QCoreApplication.translate("Dialog", "", None, 0))

