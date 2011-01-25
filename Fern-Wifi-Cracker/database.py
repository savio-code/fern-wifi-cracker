# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created: Tue Nov 16 21:15:57 2010
#      by: PyQt4 UI code generator 4.7.7
#
# WARNING! All changes made in this file will be lost!
import os
from main_window import font_size
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

font_setting = font_size()

class database_ui(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(509, 306)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("%s/resources/Database-64.png"%(os.getcwd()))), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.key_table = QtGui.QTableWidget(Dialog)
        self.key_table.setGeometry(QtCore.QRect(20, 60, 471, 192))
        self.key_table.setObjectName(_fromUtf8("key_table"))
        self.key_table.setColumnCount(4)
        self.key_table.setRowCount(0)
	font = QtGui.QFont() 
	font.setPointSize(font_setting)
	self.key_table.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("%s/resources/router-icone-7671-128.png"%(os.getcwd()))), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item = QtGui.QTableWidgetItem()
        self.key_table.setHorizontalHeaderItem(0, item)
        item.setIcon(icon1)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("%s/resources/binary.png"%(os.getcwd()))), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item = QtGui.QTableWidgetItem()
        self.key_table.setHorizontalHeaderItem(1, item)
        item.setIcon(icon2)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("%s/resources/login_128.png"%(os.getcwd()))), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item = QtGui.QTableWidgetItem()
        self.key_table.setHorizontalHeaderItem(2, item)
        item.setIcon(icon3)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8("%s/resources/wifi_5.png"%(os.getcwd()))), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item = QtGui.QTableWidgetItem()
        self.key_table.setHorizontalHeaderItem(3, item)
        item.setIcon(icon4)
        self.save_button = QtGui.QPushButton(Dialog)
        self.save_button.setGeometry(QtCore.QRect(20, 260, 131, 31))
        self.save_button.setObjectName(_fromUtf8("save_button"))
	font = QtGui.QFont() 
	font.setPointSize(font_setting)
	self.save_button.setFont(font)	
        self.insert_button = QtGui.QPushButton(Dialog)
        self.insert_button.setGeometry(QtCore.QRect(200, 260, 131, 31))
        self.insert_button.setObjectName(_fromUtf8("insert_button"))
	font = QtGui.QFont() 
	font.setPointSize(font_setting)
	self.insert_button.setFont(font)
        self.delete_button = QtGui.QPushButton(Dialog)
        self.delete_button.setGeometry(QtCore.QRect(380, 260, 111, 31))
        self.delete_button.setObjectName(_fromUtf8("delete_button"))
	font = QtGui.QFont() 
	font.setPointSize(font_setting)
	self.delete_button.setFont(font)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 571, 16))
        self.label.setObjectName(_fromUtf8("label"))
	font = QtGui.QFont() 
	font.setPointSize(font_setting)
	self.label.setFont(font)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 451, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
	font = QtGui.QFont() 
	font.setPointSize(font_setting)
	self.label_2.setFont(font)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Fern - Key Database", None, QtGui.QApplication.UnicodeUTF8))
        self.key_table.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Dialog", "Access Point", None, QtGui.QApplication.UnicodeUTF8))
        self.key_table.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Dialog", "Encryption", None, QtGui.QApplication.UnicodeUTF8))
        self.key_table.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Dialog", "Key", None, QtGui.QApplication.UnicodeUTF8))
        self.key_table.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("Dialog", "Channel", None, QtGui.QApplication.UnicodeUTF8))
        self.save_button.setText(QtGui.QApplication.translate("Dialog", "Save Changes", None, QtGui.QApplication.UnicodeUTF8))
        self.insert_button.setText(QtGui.QApplication.translate("Dialog", "Insert New Key", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_button.setText(QtGui.QApplication.translate("Dialog", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Decryped wireless keys are automatically added to the Sqlite database after a successful", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "attack, Alternatively you can insert keys to the database manually", None, QtGui.QApplication.UnicodeUTF8))

