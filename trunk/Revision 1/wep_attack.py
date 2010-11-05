# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created: Sun Oct 24 00:35:39 2010
#      by: PyQt4 UI code generator 4.7.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class wep_window(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setEnabled(True)
        Dialog.resize(472, 419)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("resources/wifi_4.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-30, -20, 501, 461))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8("resources/binary_2.png")))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_23 = QtGui.QLabel(Dialog)
        self.label_23.setEnabled(True)
        self.label_23.setGeometry(QtCore.QRect(170, 150, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_23.setFont(font)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setEnabled(True)
        self.label_4.setGeometry(QtCore.QRect(170, 110, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.ivs_progress = QtGui.QProgressBar(Dialog)
        self.ivs_progress.setGeometry(QtCore.QRect(150, 313, 281, 20))
        self.ivs_progress.setMaximum(20000)
        self.ivs_progress.setTextVisible(False)
        self.ivs_progress.setObjectName(_fromUtf8("ivs_progress"))
        self.channel_label = QtGui.QLabel(Dialog)
        self.channel_label.setGeometry(QtCore.QRect(240, 110, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.channel_label.setFont(font)
        self.channel_label.setObjectName(_fromUtf8("channel_label"))
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setEnabled(True)
        self.label_7.setGeometry(QtCore.QRect(170, 90, 41, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.power_label = QtGui.QLabel(Dialog)
        self.power_label.setGeometry(QtCore.QRect(240, 130, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.power_label.setFont(font)
        self.power_label.setObjectName(_fromUtf8("power_label"))
        self.encrypt_wep_label = QtGui.QLabel(Dialog)
        self.encrypt_wep_label.setGeometry(QtCore.QRect(240, 150, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.encrypt_wep_label.setFont(font)
        self.encrypt_wep_label.setObjectName(_fromUtf8("encrypt_wep_label"))
        self.essid_label = QtGui.QLabel(Dialog)
        self.essid_label.setGeometry(QtCore.QRect(240, 70, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.essid_label.setFont(font)
        self.essid_label.setObjectName(_fromUtf8("essid_label"))
        self.associate_label = QtGui.QLabel(Dialog)
        self.associate_label.setEnabled(False)
        self.associate_label.setGeometry(QtCore.QRect(20, 240, 231, 16))
        self.associate_label.setObjectName(_fromUtf8("associate_label"))
        self.bssid_label = QtGui.QLabel(Dialog)
        self.bssid_label.setGeometry(QtCore.QRect(240, 90, 181, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.bssid_label.setFont(font)
        self.bssid_label.setObjectName(_fromUtf8("bssid_label"))
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(-20, -60, 481, 491))
        self.label_6.setText(_fromUtf8(""))
        self.label_6.setPixmap(QtGui.QPixmap(_fromUtf8("D:/Doc1_files/image001.gif")))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 141, 131))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8("resources/router-icone-7671-128.png")))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.injection_work_label = QtGui.QLabel(Dialog)
        self.injection_work_label.setEnabled(False)
        self.injection_work_label.setGeometry(QtCore.QRect(210, 230, 231, 20))
        self.injection_work_label.setAlignment(QtCore.Qt.AlignCenter)
        self.injection_work_label.setObjectName(_fromUtf8("injection_work_label"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setEnabled(True)
        self.label_5.setGeometry(QtCore.QRect(170, 130, 41, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gathering_label = QtGui.QLabel(Dialog)
        self.gathering_label.setEnabled(False)
        self.gathering_label.setGeometry(QtCore.QRect(20, 280, 231, 16))
        self.gathering_label.setObjectName(_fromUtf8("gathering_label"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 50, 431, 171))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label_26 = QtGui.QLabel(self.groupBox)
        self.label_26.setGeometry(QtCore.QRect(10, 130, 451, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(50)
        font.setBold(False)
        self.label_26.setFont(font)
        self.label_26.setObjectName(_fromUtf8("label_26"))
        self.label_27 = QtGui.QLabel(self.groupBox)
        self.label_27.setGeometry(QtCore.QRect(10, 150, 171, 18))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_27.setFont(font)
        self.label_27.setObjectName(_fromUtf8("label_27"))
        self.wep_access_point_combo = QtGui.QComboBox(Dialog)
        self.wep_access_point_combo.setGeometry(QtCore.QRect(20, 10, 331, 31))
        self.wep_access_point_combo.setObjectName(_fromUtf8("wep_access_point_combo"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setEnabled(True)
        self.label_3.setGeometry(QtCore.QRect(170, 70, 41, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.attack_type_combo = QtGui.QComboBox(Dialog)
        self.attack_type_combo.setGeometry(QtCore.QRect(210, 250, 221, 31))
        self.attack_type_combo.setObjectName(_fromUtf8("attack_type_combo"))
        self.wep_attack_button = QtGui.QPushButton(Dialog)
        self.wep_attack_button.setGeometry(QtCore.QRect(370, 10, 81, 31))
        self.wep_attack_button.setMinimumSize(QtCore.QSize(9, 15))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.wep_attack_button.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("resources/wifi_2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.wep_attack_button.setIcon(icon1)
        self.wep_attack_button.setIconSize(QtCore.QSize(24, 27))
        self.wep_attack_button.setShortcut(_fromUtf8(""))
        self.wep_attack_button.setCheckable(False)
        self.wep_attack_button.setObjectName(_fromUtf8("wep_attack_button"))
        self.injecting_label = QtGui.QLabel(Dialog)
        self.injecting_label.setEnabled(False)
        self.injecting_label.setGeometry(QtCore.QRect(20, 260, 171, 16))
        self.injecting_label.setObjectName(_fromUtf8("injecting_label"))
        self.cracking_label = QtGui.QLabel(Dialog)
        self.cracking_label.setEnabled(False)
        self.cracking_label.setGeometry(QtCore.QRect(20, 300, 231, 16))
        self.cracking_label.setObjectName(_fromUtf8("cracking_label"))
        self.finished_label = QtGui.QLabel(Dialog)
        self.finished_label.setEnabled(False)
        self.finished_label.setGeometry(QtCore.QRect(20, 320, 231, 16))
        self.finished_label.setObjectName(_fromUtf8("finished_label"))
        self.ivs_progress_label = QtGui.QLabel(Dialog)
        self.ivs_progress_label.setEnabled(False)
        self.ivs_progress_label.setGeometry(QtCore.QRect(160, 290, 271, 20))
        self.ivs_progress_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ivs_progress_label.setObjectName(_fromUtf8("ivs_progress_label"))
        self.wep_copy_label = QtGui.QLabel(Dialog)
        self.wep_copy_label.setEnabled(False)
        self.wep_copy_label.setGeometry(QtCore.QRect(10, 390, 431, 20))
        self.wep_copy_label.setAlignment(QtCore.Qt.AlignCenter)
        self.wep_copy_label.setObjectName(_fromUtf8("wep_copy_label"))
        self.wep_key_label = QtGui.QLabel(Dialog)
        self.wep_key_label.setGeometry(QtCore.QRect(30, 360, 411, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.wep_key_label.setFont(font)
        self.wep_key_label.setText(_fromUtf8(""))
        self.wep_key_label.setAlignment(QtCore.Qt.AlignCenter)
        self.wep_key_label.setObjectName(_fromUtf8("wep_key_label"))
        self.wep_status_label = QtGui.QLabel(Dialog)
        self.wep_status_label.setEnabled(False)
        self.wep_status_label.setGeometry(QtCore.QRect(20, 340, 421, 20))
        self.wep_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.wep_status_label.setObjectName(_fromUtf8("wep_status_label"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        self.groupBox.setEnabled(False)
        self.label_26.setEnabled(False)
        self.label_27.setEnabled(False)
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Fern WEP Attack", None, QtGui.QApplication.UnicodeUTF8))
        self.label_23.setText(QtGui.QApplication.translate("Dialog", "<font color=green><b>Encryption:</b></font>     ", None, QtGui.QApplication.UnicodeUTF8))
        self.wep_copy_label.setText(QtGui.QApplication.translate("Dialog", "", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "<font color=green><b>Channel:</b></font>         ", None, QtGui.QApplication.UnicodeUTF8))
        self.channel_label.setText(QtGui.QApplication.translate("Dialog", "12", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "<font color=green><b>Bssid:</b></font>          ", None, QtGui.QApplication.UnicodeUTF8))
        self.power_label.setText(QtGui.QApplication.translate("Dialog", "34", None, QtGui.QApplication.UnicodeUTF8))
        self.encrypt_wep_label.setText(QtGui.QApplication.translate("Dialog", "wep", None, QtGui.QApplication.UnicodeUTF8))
        self.cracking_label.setText(QtGui.QApplication.translate("Dialog", "Cracking Encryption", None, QtGui.QApplication.UnicodeUTF8))
        self.wep_status_label.setText(QtGui.QApplication.translate("Dialog", "wep encryption status", None, QtGui.QApplication.UnicodeUTF8))
        self.essid_label.setText(QtGui.QApplication.translate("Dialog", "weee", None, QtGui.QApplication.UnicodeUTF8))
        self.injecting_label.setText(QtGui.QApplication.translate("Dialog", "Injecting packets", None, QtGui.QApplication.UnicodeUTF8))
        self.associate_label.setText(QtGui.QApplication.translate("Dialog", "Associating with Access Point", None, QtGui.QApplication.UnicodeUTF8))
        self.bssid_label.setText(QtGui.QApplication.translate("Dialog", "12", None, QtGui.QApplication.UnicodeUTF8))
        self.finished_label.setText(QtGui.QApplication.translate("Dialog", "Finished", None, QtGui.QApplication.UnicodeUTF8))
        self.injection_work_label.setText(QtGui.QApplication.translate("Dialog", " \t Injection capability status ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "<font color=green><b>Power:</b></font>           ", None, QtGui.QApplication.UnicodeUTF8))
        self.gathering_label.setText(QtGui.QApplication.translate("Dialog", "Gathering packets", None, QtGui.QApplication.UnicodeUTF8))
        self.ivs_progress_label.setText(QtGui.QApplication.translate("Dialog", "captured IVS status", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Access Point Details", None, QtGui.QApplication.UnicodeUTF8))
        self.label_26.setText(QtGui.QApplication.translate("Dialog", "Access point and specifications are derived on initiation,double click to get  IVS", None, QtGui.QApplication.UnicodeUTF8))
        self.label_27.setText(QtGui.QApplication.translate("Dialog", " automatic cracking rate", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "<font color=green><b>Essid:</b></font>             ", None, QtGui.QApplication.UnicodeUTF8))
        self.wep_attack_button.setText(QtGui.QApplication.translate("Dialog", "Attack", None, QtGui.QApplication.UnicodeUTF8))
