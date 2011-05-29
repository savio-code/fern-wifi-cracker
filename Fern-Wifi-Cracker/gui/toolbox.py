# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created: Tue Jan 25 11:52:35 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!
import os
from main_window import font_size
from PyQt4 import QtCore, QtGui

font_setting = font_size()

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class toolbox_win(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(599, 343)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("%s/resources/1295905972_tool_kit.png"%(os.getcwd()))), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 551, 181))
	font = QtGui.QFont()
        font.setPointSize(font_setting)
        self.groupBox.setFont(font)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 30, 471, 16))
	font = QtGui.QFont()
        font.setPointSize(font_setting)
        self.groupBox.setFont(font)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
	font = QtGui.QFont()
        font.setPointSize(font_setting)
        self.label.setFont(font)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 210, 551, 111))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.pushButton = QtGui.QPushButton(self.groupBox_2)
        self.pushButton.setGeometry(QtCore.QRect(20, 30, 141, 61))
	font = QtGui.QFont()
        font.setPointSize(font_setting)
        self.groupBox_2.setFont(font)
	font = QtGui.QFont()
        font.setPointSize(font_setting)
        self.pushButton.setFont(font)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.pushButton.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("%s/resources/1295906241_preferences-desktop-font.png"%(os.getcwd()))), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setIconSize(QtCore.QSize(46, 50))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
	font = QtGui.QFont()
        font.setPointSize(font_setting)
        self.pushButton.setFont(font)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Fern Tool Box", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Features", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "As time elapses , new program features will be added to this section of the program", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Dialog", "General Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Font Settings", None, QtGui.QApplication.UnicodeUTF8))

