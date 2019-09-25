from core import variables

from gui.tips import *
from gui.toolbox import *
from gui.settings import *
from gui.geotrack import *
from gui.font_settings import *
from core.variables import *
from core.functions import *
from gui.attack_settings import *
from core.settings import *
from core.toolbox import *
from gui.fern_pro_tip import *
from gui.toolbox import *
from core.toolbox.fern_ray_fusion import *


from PyQt5 import QtCore, QtGui, QtWidgets

#
# Tool Box window class
#
class tool_box_window(QtWidgets.QDialog,toolbox_win):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.pushButton.clicked.connect(self.font_exec)
        self.geotrack_button.clicked.connect(self.geotrack_exec)
        self.attack_options_button.clicked.connect(self.attack_settings_exec)
        self.cookie_hijack_button.clicked.connect(self.cookie_hijack_exec)
        self.ray_fusion_button.clicked.connect(self.ray_fusion_exec)


    #
    #   TOOLBOX FEATURES
    #
    def geotrack_exec(self):
        QtWidgets.QMessageBox.warning(self,"Geo Tracker","This feature has been deprecated")


    def cookie_hijack_exec(self):
        try:
            import scapy
        except ImportError:
            QtWidgets.QMessageBox.warning(self,"Scapy Dependency","Scapy library is currently not installed \nPlease run \"pip install scapy\" to install the dependency")
            return

        cookie_hijacker = fern_cookie_hijacker.Fern_Cookie_Hijacker()
        cookie_hijacker.exec_()


    def ray_fusion_exec(self):
        ray_fusion = Ray_Fusion()
        ray_fusion.exec_()



    #
    #   SETTINGS
    #
    def font_exec(self):
        font_dialog_box = font_dialog()
        font_dialog_box.exec_()

    def attack_settings_exec(self):
        wifi_attack_settings_box = wifi_attack_settings()
        wifi_attack_settings_box.exec_()



################################################################################
#                                                                              #
#                             GENERAL SETTINGS                                 #
#                                                                              #
################################################################################

class font_dialog(QtWidgets.QDialog,font_dialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        self.setWindowTitle('Font Settings')
        self.label_2.setText('Current Font: <font color=green><b>%s</b></font>'% \
                                (reader(os.getcwd() + '/.font_settings.dat' ).split()[2]))

        self.buttonBox.accepted.connect(self.set_font)

        font_range = []
        for font_numbers in range(1,21):
            font_range.append(str(font_numbers))
        self.comboBox.addItems(font_range)

    def set_font(self):
        if '.font_settings.dat' in os.listdir(os.getcwd()):
            os.remove('.font_settings.dat')
            choosen_font = self.comboBox.currentText()
            font_string  = 'font_size = %s'%(choosen_font)
            write('.font_settings.dat',font_string)

        self.close()
        QtWidgets.QMessageBox.information(self,'Font Settings','Please restart application to apply changes')




class wifi_attack_settings(QtWidgets.QDialog,Ui_attack_settings):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)

        self.settings = Fern_settings()
        self.display_components()

        self.mac_button.clicked.connect(self.set_static_mac)
        self.mac_box.clicked.connect(self.remove_mac_objects)
        self.capture_box.clicked.connect(self.remove_capture_objects)
        self.direc_browse.clicked.connect(self.set_capture_directory)




    def display_components(self):
        if self.settings.setting_exists('capture_directory'):
            self.capture_box.setChecked(True)
            self.directory_label.setText('<font color=green><b>' + str(self.settings.read_last_settings('capture_directory')) + '</b></font>')
        if self.settings.setting_exists('mac_address'):
            self.mac_box.setChecked(True)
            self.mac_edit.setText(str(self.settings.read_last_settings('mac_address')))



    def set_static_mac(self):
        mac_address = str(self.mac_edit.text())
        if not Check_MAC(mac_address):
            QtWidgets.QMessageBox.warning(self,"Invalid MAC Address",variables.invalid_mac_address_error)
            self.mac_edit.setFocus()
        else:
            self.settings.create_settings('mac_address',mac_address)


    def set_capture_directory(self):
        directory = str(QtWidgets.QFileDialog.getExistingDirectory(self,"Select Capture Storage Directory",""))
        if directory:
            self.directory_label.setText('<font color=green><b>' + directory)
            self.settings.create_settings("capture_directory",directory)


    def remove_mac_objects(self):
        if not self.mac_box.isChecked():
            self.mac_edit.clear()
            self.settings.remove_settings('mac_address')


    def remove_capture_objects(self):
        if not self.capture_box.isChecked():
            self.directory_label.clear()
            self.settings.remove_settings('capture_directory')





################################################################################
#                                                                              #
#                    WEP ATTACK OPTIONAL SETTINGS                              #
#                                                                              #
################################################################################


#
# Tips Dialog, show user tips on how to access settings dialog and set scan preferences
#
class tips_window(QtWidgets.QDialog,tips_dialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.type = int()           # Type of tip display e.g tip from mainwindow = 1

        self.settings = Fern_settings()

        self.pushButton.clicked.connect(self.accept)

    def accept(self):
        check_status = self.checkBox.isChecked()

        if(self.type == 1):         # From Main Window
            if check_status == True:
                self.settings.create_settings("tips","1")
            else:
                self.settings.create_settings("tips","0")

        if(self.type == 2):
            if check_status == True:
                self.settings.create_settings("copy key tips","1")
            else:
                self.settings.create_settings("copy key tips","0")

        self.close()



class Fern_Pro_Tips(QtWidgets.QDialog,Fern_Pro_Tip_ui):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)

        self.settings = Fern_settings()

        self.yes_button.clicked.connect(self.open_website)
        self.show_message_checkbox.clicked.connect(self.toggle_tip)


    def open_website(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("http://www.fern-pro.com/"))
        self.toggle_tip()
        self.close()


    def toggle_tip(self):
        checked = self.show_message_checkbox.isChecked()
        if(checked):
            self.settings.create_settings("fern_pro_tips","1")
            return

        self.settings.create_settings("fern_pro_tips","0")





#Finished Here (tips_window)

#
# Class for the settings dialog box
#
class settings_dialog(QtWidgets.QDialog,settings):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)

        self.settings = Fern_settings()

        self.setupUi(self)
        if len(variables.xterm_setting) > 0:
            self.xterm_checkbox.setChecked(True)

        self.label_4.setText("\t\t<font color=green>%s Activated</font>"%(variables.monitor_interface))

        list_ = ['All Channels']
        for list_numbers in range(1,15):
            list_.append(str(list_numbers))
        self.channel_combobox.addItems(list_)
        self.buttonBox.accepted.connect(self.change_settings)
        self.buttonBox.rejected.connect(self.close)


    #
    # Log selected temporary manual channel to fern-log directory
    #
    def change_settings(self):
        channel = str(self.channel_combobox.currentText())
        term_settings = self.xterm_checkbox.isChecked()

        if channel == 'All Channels':
            variables.static_channel = str()
        else:
            variables.static_channel = channel

        if term_settings:
            self.settings.create_settings("xterm","xterm -geometry 100 -e")
        else:
            self.settings.create_settings("xterm",str())
        variables.xterm_setting = self.settings.read_last_settings("xterm")


