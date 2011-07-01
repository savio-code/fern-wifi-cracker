from core import variables

from gui.tips import *
from gui.toolbox import *
from gui.settings import *
from gui.geotrack import *
from gui.font_settings import *
from gui.ivs_settings import *
from core.variables import *
from core.functions import *
from gui.attack_settings import *

from toolbox.fern_tracker import *

from PyQt4 import QtGui,QtCore

#
# Tool Box window class
#
class tool_box_window(QtGui.QDialog,toolbox_win):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.connect(self.pushButton,QtCore.SIGNAL("clicked()"),self.font_exec)
        self.connect(self.geotrack_button,QtCore.SIGNAL("clicked()"),self.geotrack_exec)
        self.connect(self.attack_options_button,QtCore.SIGNAL("clicked()"),self.attack_settings_exec)

    def font_exec(self):
        font_dialog_box = font_dialog()
        font_dialog_box.exec_()

    def geotrack_exec(self):
        geotrack_dialog_box = Fern_geolocation_tracker()
        geotrack_dialog_box.exec_()

    def attack_settings_exec(self):
        wifi_attack_settings_box = wifi_attack_settings()
        wifi_attack_settings_box.exec_()



################################################################################
#                                                                              #
#                             GENERAL SETTINGS                                 #
#                                                                              #
################################################################################

class font_dialog(QtGui.QDialog,font_dialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        self.setWindowTitle('Font Settings')
        self.label_2.setText('Current Font: <font color=green><b>%s</b></font>'% \
                                (reader(os.getcwd() + '/.font_settings.dat' ).split()[2]))

        self.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),self.set_font)

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
        QtGui.QMessageBox.information(self,'Font Settings','Please restart application to apply changes')




class wifi_attack_settings(QtGui.QDialog,Ui_attack_settings):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        create_settings_file()
        self.display_components()

        self.connect(self.mac_button,QtCore.SIGNAL("clicked()"),self.set_static_mac)
        self.connect(self.mac_box,QtCore.SIGNAL("clicked()"),self.remove_mac_objects)
        self.connect(self.capture_box,QtCore.SIGNAL("clicked()"),self.remove_capture_objects)
        self.connect(self.direc_browse,QtCore.SIGNAL("clicked()"),self.set_capture_directory)


    def display_components(self):
        if settings_exists('capture_directory'):
            self.capture_box.setChecked(True)
            self.directory_label.setText('<font color=green><b>' + str(read_settings('capture_directory')) + '</b></font>')
        if settings_exists('mac_address'):
            self.mac_box.setChecked(True)
            self.mac_edit.setText(str(read_settings('mac_address')))



    def set_static_mac(self):
        mac_address = str(self.mac_edit.text())
        if not Check_MAC(mac_address):
            QtGui.QMessageBox.warning(self,"Invalid MAC Address",variables.invalid_mac_address_error)
            self.mac_edit.setFocus()
        else:
            create_settings('mac_address',mac_address)


    def set_capture_directory(self):
        directory = str(QtGui.QFileDialog.getExistingDirectory(self,"Select Capture Sorage Directory",""))
        if directory:
            self.directory_label.setText('<font color=green><b>' + directory)
            create_settings("capture_directory",directory)


    def remove_mac_objects(self):
        if not self.mac_box.isChecked():
            self.mac_edit.clear()
            remove_setting('mac_address')


    def remove_capture_objects(self):
        if not self.capture_box.isChecked():
            self.directory_label.clear()
            remove_setting('capture_directory')





################################################################################
#                                                                              #
#                    WEP ATTACK OPTIONAL SETTINGS                              #
#                                                                              #
################################################################################


#
# Class dialog for automatic ivs captupe and limit reference
#
class ivs_dialog(QtGui.QDialog,ivs_window):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        ivs_list = ['Select IVS Rate','5000','10000','15000','20000','25000','30000','35000','40000','45000','50000','55000','60000','65000','70000']
        self.ivs_combo.addItems(ivs_list)

        self.connect(self.ok_button,QtCore.SIGNAL("clicked()"),self.ivs_settings)
        self.connect(self.cancel_button,QtCore.SIGNAL("clicked()"),QtCore.SLOT("close()"))

    def ivs_settings(self):
        current_ivs = str(self.ivs_combo.currentText())
        if 'ivs_settings.log' in os.listdir('/tmp/fern-log'):
            remove('/tmp/fern-log','ivs_settings.log')
        if current_ivs != 'Select IVS Rate':
            write('/tmp/fern-log/ivs_settings.log',current_ivs)

        self.close()



#
# Tips Dialog, show user tips on how to access settings dialog and set scan preferences
#
class tips_window(QtGui.QDialog,tips_dialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        self.connect(self.pushButton,QtCore.SIGNAL("clicked()"),self.accept)

    def accept(self):
        check_status = self.checkBox.isChecked()

        if check_status == True:
            write('fern-settings/tips-settings.dat','1')
        else:
            remove('fern-settings','tips-settings.dat')
        self.close()

#Finished Here (tips_window)

#
# Class for the settings dialog box
#
class settings_dialog(QtGui.QDialog,settings):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        self.setupUi(self)
        if len(variables.xterm_setting) > 0:
            self.xterm_checkbox.setChecked(True)

        list_ = ['All Channels']
        for list_numbers in range(1,15):
            list_.append(str(list_numbers))
        self.channel_combobox.addItems(list_)
        self.connect(self.xterm_checkbox,QtCore.SIGNAL("clicked(bool)"),self.xterm)
        self.connect(self.channel_combobox,QtCore.SIGNAL("currentIndexChanged(QString)"),self.channel_log)


    #
    # Log selected temporary manual channel to fern-log directory
    #
    def channel_log(self):
        try:
            remove('/tmp/fern-log','static-channel.log')
        except IOError:
            pass
        channel = str(self.channel_combobox.currentText())
        if channel == 'All Channels':
            os.system('rm -r /tmp/fern-log/static-channel.log')
            pass
        else:
            write('/tmp/fern-log/static-channel.log',channel)

    #
    # Log xtern selectionn to fern-settings directory manual channel
    #
    def xterm(self):
        xterm_settings = self.xterm_checkbox.isChecked()
        if xterm_settings:
            variables.xterm_setting = 'xterm -geometry 100 -e'
        else:
            variables.xterm_setting = ''
