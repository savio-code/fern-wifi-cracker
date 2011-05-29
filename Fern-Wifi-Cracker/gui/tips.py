# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created: Wed Oct 13 22:30:36 2010
#      by: PyQt4 UI code generator 4.7.7
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

class tips_dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setEnabled(True)
        Dialog.resize(467, 167)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("%s/resources/1286998882_ktip.png"%(os.getcwd()))), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setSizeGripEnabled(False)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 0, 391, 31))
        self.label.setObjectName(_fromUtf8("label"))
	font = QtGui.QFont() 
	font.setPointSize(font_setting)
	self.label.setFont(font)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 61, 81))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8("%s/resources/1286998882_ktip.png"%(os.getcwd()))))
        self.label_2.setObjectName(_fromUtf8("label_2"))
	font = QtGui.QFont() 
	font.setPointSize(font_setting)
	self.label_2.setFont(font)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(60, 20, 391, 31))
        self.label_3.setObjectName(_fromUtf8("label_3"))
	font = QtGui.QFont() 
	font.setPointSize(font_setting)
	self.label_3.setFont(font)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(60, 40, 381, 31))
        self.label_4.setObjectName(_fromUtf8("label_4"))
	font = QtGui.QFont() 
	font.setPointSize(font_setting)
	self.label_4.setFont(font)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(180, 130, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
	font = QtGui.QFont() 
	font.setPointSize(font_setting)
	self.pushButton.setFont(font)
        self.checkBox = QtGui.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(40, 100, 191, 17))
        self.checkBox.setCheckable(True)
        self.checkBox.setChecked(False)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
	font = QtGui.QFont() 
	font.setPointSize(font_setting)
	self.checkBox.setFont(font)
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(60, 60, 351, 31))
        self.label_5.setObjectName(_fromUtf8("label_5"))
	font = QtGui.QFont() 
	font.setPointSize(font_setting)
	self.label_5.setFont(font)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Tips - Scan settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "To Access the \"Settings\" for the network scan preferences \"Double click\"", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", " on any area of the main window, \"Scan for network button\" is used to ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "scan for network based on the settings options of the settings dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("Dialog", "Don\'t show this message again", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Default  is automated scan, Fake Mac-Address is always used", None, QtGui.QApplication.UnicodeUTF8))

