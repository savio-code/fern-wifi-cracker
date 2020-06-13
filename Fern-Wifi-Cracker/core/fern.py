import os
import re
import sys
import time
import threading
import shutil
import sqlite3
import subprocess
from urllib import request

from core import variables
from PyQt5 import QtCore, QtGui, QtWidgets

from core.wep import *
from core.wpa import *
from core.wps import *
from core.tools import *
from core.database import *
from core.functions import *
from core.settings import *

from gui.main_window import *

__version__ = 3


#
# Main Window Class
#
class mainwindow(QtWidgets.QDialog, Ui_Dialog):
    file_downloaded_signal = QtCore.pyqtSignal()
    finished_downloading_signal = QtCore.pyqtSignal()
    internal_scan_error_signal = QtCore.pyqtSignal()
    restart_application_signal = QtCore.pyqtSignal()
    download_failed_signal = QtCore.pyqtSignal()
    current_version_signal = QtCore.pyqtSignal()
    new_update_available_signal = QtCore.pyqtSignal()
    already_latest_update_signal = QtCore.pyqtSignal()
    previous_message_signal = QtCore.pyqtSignal()
    failed_update_signal = QtCore.pyqtSignal()
    interface_cards_not_found_signal = QtCore.pyqtSignal()
    interface_cards_found_signal = QtCore.pyqtSignal()
    monitor_mode_enabled_signal = QtCore.pyqtSignal()
    monitor_failed_signal = QtCore.pyqtSignal()
    wep_number_changed_signal = QtCore.pyqtSignal()
    wep_button_true_signal = QtCore.pyqtSignal()
    wep_button_false_signal = QtCore.pyqtSignal()
    wpa_button_false_signal = QtCore.pyqtSignal()
    wpa_button_true_signal = QtCore.pyqtSignal()
    wpa_number_changed_signal = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        self.refresh_interface()
        self.evaliate_permissions()

        self.monitor_interface = str()
        self.wep_count = str()
        self.wpa_count = str()

        self.interface_cards = list()

        variables.wps_functions = WPS_Attack()  # WPS functions

        self.movie = QtGui.QMovie(self)
        self.animate_monitor_mode(True)  # Loading gif animation

        self.settings = Fern_settings()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.display_timed_objects)
        self.timer.setInterval(3000)

        # self.DoubleClicked.connect(self.mouseDoubleClickEvent)
        self.refresh_intfacebutton.clicked.connect(self.refresh_interface)
        self.interface_combo.currentIndexChanged['QString'].connect(self.setmonitor)
        self.monitor_mode_enabled_signal.connect(self.monitor_mode_enabled)
        self.monitor_failed_signal.connect(self.display_error_monitor)
        self.interface_cards_found_signal.connect(self.interface_cards_found)
        self.interface_cards_not_found_signal.connect(self.interface_card_not_found)
        self.scan_button.clicked.connect(self.scan_network)
        self.wep_button.clicked.connect(self.wep_attack_window)
        self.wpa_button.clicked.connect(self.wpa_attack_window)
        self.tool_button.clicked.connect(self.tool_box_window)

        self.wep_number_changed_signal.connect(self.wep_number_changed)
        self.wep_button_true_signal.connect(self.wep_button_true)
        self.wep_button_false_signal.connect(self.wep_button_false)

        self.wpa_number_changed_signal.connect(self.wpa_number_changed)
        self.wpa_button_true_signal.connect(self.wpa_button_true)
        self.wpa_button_false_signal.connect(self.wpa_button_false)

        self.database_button.clicked.connect(self.database_window)
        self.update_button.clicked.connect(self.update_fern)
        self.finished_downloading_signal.connect(self.finished_downloading_files)
        self.restart_application_signal.connect(self.restart_application)
        self.failed_update_signal.connect(self.update_fail)
        self.already_latest_update_signal.connect(self.latest_update)
        self.previous_message_signal.connect(self.latest_svn)
        self.new_update_available_signal.connect(self.new_update_avialable)
        self.current_version_signal.connect(self.current_update)
        self.download_failed_signal.connect(self.download_failed)
        self.internal_scan_error_signal.connect(self.scan_error_display)
        self.file_downloaded_signal.connect(self.downloading_update_files)

        self.update_label.setText(
            '<font color=green>Currently installed version: Revision %s</font>' % (self.installed_revision()))

        # Display update status on main_windows
        t = threading.Thread(target=self.update_initializtion_check)
        t.start()

        self.set_WindowFlags()

        self.update_database_label()
        self.set_xterm_settings()

    def set_WindowFlags(self):
        try:
            self.setWindowFlags(
                QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMaximizeButtonHint)  # Some older versions of Qt4 dont support some flags
        except:
            pass

    def display_timed_objects(self):
        self.show_Fern_Pro_tip()
        self.timer.stop()

    def show_Fern_Pro_tip(self):
        if (self.settings.setting_exists("fern_pro_tips")):
            if (self.settings.read_last_settings("fern_pro_tips") == "0"):
                tips = Fern_Pro_Tips()
                tips.exec_()
        else:
            self.settings.create_settings("fern_pro_tips", "0")
            tips = Fern_Pro_Tips()
            tips.exec_()

    #
    #   Read database entries and count entries then set Label on main window
    #
    def update_database_label(self):
        connection = sqlite3.connect(os.getcwd() + '/key-database/Database.db')
        query = connection.cursor()
        query.execute('''select * from keys''')
        items = query.fetchall()
        connection.close()
        if len(items) == 0:
            self.label_16.setText('<font color=red>No Key Entries</font>')
        else:
            self.label_16.setText('<font color=green>%s Key Entries</font>' % (str(len(items))))

    #
    #   Read last xterm settings
    #
    def set_xterm_settings(self):
        if not self.settings.setting_exists("xterm"):
            self.settings.create_settings("xterm", str())
        variables.xterm_setting = self.settings.read_last_settings("xterm")

    #
    # SIGNALs for update threads
    #
    def update_fail(self):
        self.update_label.setText('<font color=red>Unable to check for updates,network timeout')

    def download_failed(self):
        self.update_label.setText('<font color=red>Download failed,network timeout')

    def downloading_update_files(self):
        global file_total
        global files_downloaded

        self.update_label.setText('<font color=green>Downloading.. %s Complete</font>' \
                                  % (self.percentage(files_downloaded, file_total)))

    def installed_revision(self):
        svn_info = subprocess.getstatusoutput('svn info ' + directory)
        if svn_info[0] == 0:
            svn_version = svn_info[1].splitlines()[4].strip('Revision: ')
        else:
            svn_version = '94'
        return svn_version

    def finished_downloading_files(self):
        self.update_label.setText('<font color=green>Finished Downloading</font>')

    def restart_application(self):
        self.update_label.setText('<font color=red>Please Restart application</font>')

    def latest_update(self):
        self.update_label.setText('<font color=green>No new update is available for download</font>')

    def current_update(self):
        self.update_label.setText(
            '<font color=green>Currently installed version: Revision %s</font>' % (self.installed_revision()))

    def latest_svn(self):
        self.update_label.setText('<font color=green>Latest update is already installed</font>')

    def new_update_avialable(self):
        self.update_label.setText('<font color=green>New Update is Available</font>')
        self.update_button.setFocus()

    def update_error(self):
        global svn_access
        global svn_failure_message
        svn_failure_message = str()
        svn_failure = svn_access.stderr
        svn_failure_message = svn_failure.read()

    #
    # Update Fern application via SVN,updates at ("svn checkout http://github.com/savio-code/fern-wifi-cracker/trunk/Fern-Wifi-Cracker/")
    #
    def update_fern(self):
        global updater_control
        updater_control = 1
        self.update_label.setText('<font color=green>Checking for update...</font>')
        t = threading.Thread(target=self.update_launcher)
        t.start()

    def percentage(self, current, total):
        float_point = float(current) / float(total)
        calculation = int(float_point * 100)
        percent = str(calculation) + '%'
        return (percent)

    def update_launcher(self):
        ''' Downloads and installs update files
        '''
        global svn_access
        global file_total
        global files_downloaded
        global fern_directory

        file_total = int()
        files_downloaded = int()

        fern_directory = os.getcwd()

        update_directory = '/tmp/Fern-Wifi-Cracker/'

        try:
            online_response_check = request.urlopen(
                'https://raw.githubusercontent.com/savio-code/fern-wifi-cracker/master/Fern-Wifi-Cracker/version')
            online_response = online_response_check.read().decode("ascii",errors="ignore")

            online_files = re.compile('total_files = \d+', re.IGNORECASE)

            for online_file_total in online_response.splitlines():
                if re.match(online_files, online_file_total):
                    file_total = int(online_file_total.split()[2])

            if 'Fern-Wifi-Cracker' in os.listdir('/tmp/'):
                variables.exec_command('rm -r /tmp/Fern-Wifi-Cracker')

            svn_access = subprocess.Popen(
                'cd /tmp/ \n svn checkout https://github.com/savio-code/fern-wifi-cracker/trunk/Fern-Wifi-Cracker/', \
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            svn_update = svn_access.stdout
            t = threading.Thread(target=self.update_error)
            t.start()

            while True:
                response = svn_update.readline()
                if len(response) > 0:
                    files_downloaded += 1
                    self.file_downloaded_signal.emit()

                if str('revision') in str(response):
                    self.finished_downloading_signal.emit()
                    # Delete all old files (*.py,*.py etc) except ".font_setting.dat" file
                    for old_file in os.listdir(os.getcwd()):
                        if os.path.isfile(os.getcwd() + os.sep + old_file) and old_file != '.font_settings.dat':
                            os.remove(os.getcwd() + os.sep + old_file)
                            # Delete all old directories except the "key-database" directory
                    for old_directory in os.listdir(os.getcwd()):
                        if os.path.isdir(os.getcwd() + os.sep + old_directory) and old_directory != 'key-database':
                            shutil.rmtree(os.getcwd() + os.sep + old_directory)

                    for update_file in os.listdir(
                            '/tmp/Fern-Wifi-Cracker'):  # Copy New update files to working directory
                        if os.path.isfile(update_directory + update_file):
                            shutil.copyfile(update_directory + update_file, os.getcwd() + os.sep + update_file)
                        else:
                            shutil.copytree(update_directory + update_file, os.getcwd() + os.sep + update_file)

                    for new_file in os.listdir(os.getcwd()):  # chmod New files to allow permissions
                        os.chmod(os.getcwd() + os.sep + new_file,0o777)

                    time.sleep(5)
                    self.restart_application_signal.emit()
                    break
                if len(svn_failure_message) > 2:
                    self.download_failed_signal.emit()
                    break

        except(request.URLError, request.HTTPError):
            self.download_failed_signal.emit()

    #
    # Update checker Thread
    #
    def update_initializtion_check(self):
        global updater_control
        updater_control = 0
        while updater_control != 1:
            try:
                online_response_thread = request.urlopen(
                    'https://raw.githubusercontent.com/savio-code/fern-wifi-cracker/master/Fern-Wifi-Cracker/version')
                online_response_string = ''
                online_response = online_response_thread.read().decode("ascii",errors="ignore")

                online_version = re.compile('version = \d+\.?\d+', re.IGNORECASE)

                for version_iterate in online_response.splitlines():
                    if re.match(online_version, version_iterate):
                        online_response_string += version_iterate

                update_version_number = float(online_response_string.split()[2])

                if float(__version__) != update_version_number:
                    self.new_update_available_signal.emit()
                    break

                if float(__version__) == update_version_number:
                    self.already_latest_update_signal.emit()
                    time.sleep(20)
                    self.previous_message_signal.emit()
                    break

            except Exception:
                self.failed_update_signal.emit()
                time.sleep(9)

    #
    # Launches Tool Box window
    #
    def tool_box_window(self):
        tool_box = tool_box_window()
        tool_box.exec_()

    #
    # Execute the wep attack window
    #
    def wep_attack_window(self):
        if 'WEP-DUMP' not in os.listdir('/tmp/fern-log'):
            os.mkdir('/tmp/fern-log/WEP-DUMP', 448)         # 488 =  Octal 700
        else:
            variables.exec_command('rm -r /tmp/fern-log/WEP-DUMP/*')
        wep_run = wep_attack_dialog()

        wep_run.update_database_label_signal.connect(self.update_database_label)
        wep_run.stop_scan_signal.connect(self.stop_network_scan)

        wep_run.exec_()

    #
    # Execute the wep attack window
    #
    def wpa_attack_window(self):
        variables.exec_command('killall aircrack-ng')
        if 'WPA-DUMP' not in os.listdir('/tmp/fern-log'):
            os.mkdir('/tmp/fern-log/WPA-DUMP', 448)
        else:
            variables.exec_command('rm -r /tmp/fern-log/WPA-DUMP/*')
        wpa_run = wpa_attack_dialog()

        wpa_run.update_database_label_signal.connect(self.update_database_label)
        wpa_run.stop_scan_signal.connect(self.stop_network_scan)

        wpa_run.exec_()

    #
    # Execute database Window
    #
    def database_window(self):
        database_run = database_dialog()
        database_run.update_database_label_signal.connect(self.update_database_label)
        database_run.exec_()

    #
    # Refresh wireless network interface card and update combobo
    #

    def refresh_interface(self):
        variables.exec_command('killall airodump-ng')
        variables.exec_command('killall airmon-ng')

        self.animate_monitor_mode(True)
        self.mon_label.clear()
        self.interface_combo.clear()
        self.interface_combo.setEnabled(True)
        self.interface_cards = list()

        t = threading.Thread(target=self.refresh_card_thread)
        t.start()

    def refresh_card_thread(self):
        # Disable cards already on monitor modes
        wireless_interfaces = str(subprocess.getstatusoutput('airmon-ng'))
        prev_monitor = os.listdir('/sys/class/net')
        monitor_interfaces_list = []
        for monitors in prev_monitor:
            if monitors in wireless_interfaces:
                monitor_interfaces_list.append(monitors)
        for monitored_interfaces in monitor_interfaces_list:
            variables.exec_command('airmon-ng stop %s' % (monitored_interfaces))

        # List Interface cards
        compatible_interface = str(subprocess.getoutput("airmon-ng"))
        interface_list = os.listdir('/sys/class/net')

        # Interate over interface output and update combo box
        isHasCompatibleCard = False
        for interface in interface_list:
            if interface.lower() in compatible_interface.lower():
                isHasCompatibleCard = True
                break

        if not isHasCompatibleCard:
            self.interface_cards_not_found_signal.emit()
        else:
            for interface in interface_list:
                if interface in compatible_interface:
                    if not interface.startswith('mon'):
                        self.interface_cards.append(interface)
            self.interface_cards_found_signal.emit()


    def interface_card_not_found(self):
        self.interface_combo.setEnabled(False)
        self.mon_label.setText("<font color=red>No Wireless Interface was found</font>")
        self.animate_monitor_mode(False)

    def interface_cards_found(self):
        self.interface_combo.addItem('Select Interface')
        interface_icon = QtGui.QIcon("%s/resources/mac_address.png" % (os.getcwd()))
        for interface in self.interface_cards:
            self.interface_combo.addItem(interface_icon, interface)
        self.mon_label.setText("<font color=red>Select an interface card</font>")
        self.animate_monitor_mode(False)

    #
    # Animates monitor mode by loading gif
    #
    def animate_monitor_mode(self, status):
        self.movie = QtGui.QMovie("%s/resources/loading.gif" % (os.getcwd()))
        self.movie.start()
        self.loading_label.setMovie(self.movie)

        if (status):  # if status == True (setting of monitor mode is in progress)
            self.interface_combo.setEnabled(False)
            self.loading_label.setVisible(True)
            self.mon_label.setVisible(False)
        else:
            self.interface_combo.setEnabled(True)
            self.loading_label.setVisible(False)
            self.mon_label.setVisible(True)

    #
    # Set monitor mode on selected monitor from combo list
    #
    def setmonitor(self):
        last_settings = str()
        self.monitor_interface = str()
        monitor_card = str(self.interface_combo.currentText())
        if monitor_card != 'Select Interface':
            mac_settings = self.settings.setting_exists('mac_address')
            if mac_settings:
                last_settings = self.settings.read_last_settings('mac_address')
            threading.Thread(target=self.set_monitor_thread, args=(monitor_card, mac_settings, last_settings,)).start()
            self.animate_monitor_mode(True)
        else:
            self.mon_label.setText("<font color=red>Monitor Mode not enabled check manually</font>")
            self.animate_monitor_mode(False)

    def killConflictProcesses(self):
        process = subprocess.getstatusoutput("airmon-ng check")
        status = process[0]
        output = process[1]

        if (status == 0):
            for line in output.splitlines():
                splitedLines = line.split()
                if (len(splitedLines) >= 2):
                    prefix = str(splitedLines[0])
                    if (prefix.isdigit()):
                        pid = int(prefix)
                        killProcess(pid)

    def set_monitor_thread(self, monitor_card, mac_setting_exists, last_settings):
        self.killConflictProcesses()

        subprocess.getstatusoutput('ifconfig %s down' % (
            self.monitor_interface))  # Avoid this:  "ioctl(SIOCSIWMODE) failed: Device or resource busy"

        status = str(subprocess.getoutput("airmon-ng start %s" % (monitor_card)))
        messages = ("monitor mode enabled", "monitor mode vif enabled", "monitor mode already")

        monitor_created = False;

        for x in messages:
            if (x in status):
                monitor_created = True

        if (monitor_created):
            monitor_interface_process = str(subprocess.getoutput("airmon-ng"))


            regex = re.compile("mon\d", re.IGNORECASE)
            interfaces = regex.findall(monitor_interface_process)

            if len(interfaces) == 0:
            	regex = re.compile("wlan\dmon", re.IGNORECASE)
            	interfaces = regex.findall(monitor_interface_process)

            	if len(interfaces) == 0:
            		self.monitor_failed_signal.emit()
            		return



            interfaces = regex.findall(monitor_interface_process)
            if (interfaces):
                self.monitor_interface = interfaces[0]
            else:
                self.monitor_interface = monitor_card

            variables.monitor_interface = self.monitor_interface
            self.interface_combo.setEnabled(False)
            variables.wps_functions.monitor_interface = self.monitor_interface
            self.monitor_mode_enabled_signal.emit()

            # Create Fake Mac Address and index for use
            mon_down = subprocess.getstatusoutput('ifconfig %s down' % (self.monitor_interface))
            if mac_setting_exists:
                variables.exec_command('macchanger -m %s %s' % (last_settings, self.monitor_interface))
            else:
                variables.exec_command('macchanger -A %s' % (self.monitor_interface))
            # mon_up = subprocess.getstatusoutput('ifconfig %s up'%(self.monitor_interface))       # Lets leave interface down to avoid channel looping during channel specific attack

            subprocess.getstatusoutput('ifconfig %s down' % (self.monitor_interface))

            for iterate in os.listdir('/sys/class/net'):
                if str(iterate) == str(self.monitor_interface):
                    os.chmod('/sys/class/net/' + self.monitor_interface + '/address', 0o777)
                    variables.monitor_mac_address = reader(
                        '/sys/class/net/' + self.monitor_interface + '/address').strip()
                    variables.wps_functions.monitor_mac_address = variables.monitor_mac_address
        else:
            self.monitor_failed_signal.emit()

    def display_monitor_error(self, color, error):
        message = "<font color='" + color + "'>" + error + "</font>"
        self.mon_label.setText(message)
        self.animate_monitor_mode(False)

    def tip_display(self):
        tips = tips_window()
        tips.type = 1
        tips.exec_()

    def display_error_monitor(self):
        self.display_monitor_error("red", "problem occured while setting up the monitor mode of selected")

    def monitor_mode_enabled(self):
        self.mon_label.setText("<font color=green>Monitor Mode Enabled on %s</font>" % (self.monitor_interface))
        self.animate_monitor_mode(False)
        # Execute tips
        if (self.settings.setting_exists("tips")):
            if (self.settings.read_last_settings("tips") == "0"):
                self.tip_display()
        else:
            self.settings.create_settings("tips", "1")
            self.tip_display()

    #
    # Double click event for poping of settings dialog box
    #
    def mouseDoubleClickEvent(self, event):
        if (len(self.monitor_interface)):
            setting = settings_dialog()
            setting.exec_()
        else:
            self.mon_label.setText("<font color=red>Enable monitor mode to access settings</font>")

    def scan_error_display(self):
        global error_catch
        self.stop_scan_network()
        QtWidgets.QMessageBox.warning(self, 'Scan Error',
                                      'Fern failed to start scan due to an airodump-ng error: <font color=red>' \
                                      + error_catch[1] + '</font>')

    #
    # Scan for available networks
    #
    def scan_network(self):
        global scan_control
        scan_control = 0

        self.wep_count = int()
        self.wpa_count = int()

        variables.wep_details = {}
        variables.wpa_details = {}

        variables.wps_functions = WPS_Attack()  # WPS functions

        variables.wps_functions.monitor_interface = self.monitor_interface
        variables.wps_functions.monitor_mac_address = variables.monitor_mac_address

        variables.wps_functions.start_WPS_Devices_Scan()  # Starts WPS Scanning

        if not self.monitor_interface:
            self.mon_label.setText("<font color=red>Enable monitor mode before scanning</font>")
        else:
            self.wpa_button.setEnabled(False)
            self.wep_button.setEnabled(False)
            self.wep_clientlabel.setEnabled(False)
            self.wpa_clientlabel.setEnabled(False)
            self.wep_clientlabel.setText("None Detected")
            self.wpa_clientlabel.setText("None Detected")
            self.label_7.setText("<font Color=green>\t Initializing</font>")
            threading.Thread(target=self.scan_wep).start()
            self.scan_button.clicked.disconnect(self.scan_network)
            self.scan_button.clicked.connect(self.stop_scan_network)

    def stop_scan_network(self):
        global error_catch
        global scan_control
        scan_control = 1
        variables.exec_command('rm -r /tmp/fern-log/*.cap')
        variables.exec_command('killall airodump-ng')
        variables.exec_command('killall airmon-ng')
        self.label_7.setText("<font Color=red>\t Stopped</font>")
        variables.wps_functions.stop_WPS_Scanning()  # Stops WPS scanning
        self.wep_clientlabel.setText("None Detected")
        self.wpa_clientlabel.setText("None Detected")
        self.scan_button.clicked.disconnect(self.stop_scan_network)
        self.scan_button.clicked.connect(self.scan_network)

    def stop_network_scan(self):
        global scan_control
        scan_control = 1
        variables.exec_command('killall airodump-ng')
        variables.exec_command('killall airmon-ng')
        self.label_7.setText("<font Color=red>\t Stopped</font>")

    #
    # WEP Thread SLOTS AND SIGNALS
    #
    def wep_number_changed(self):
        self.wep_clientlabel.setText('<font color=red>%s</font><font color=red>\t Detected</font>' % (self.wep_count))

    def wep_button_true(self):
        self.wep_button.setEnabled(True)
        self.wep_clientlabel.setEnabled(True)

    def wep_button_false(self):
        self.wep_button.setEnabled(False)
        self.wep_clientlabel.setEnabled(False)
        self.wep_clientlabel.setText('None Detected')

    #
    # WPA Thread SLOTS AND SIGNALS
    #
    def wpa_number_changed(self):
        self.wpa_clientlabel.setText('<font color=red>%s</font><font color=red>\t Detected</font>' % (self.wpa_count))

    def wpa_button_true(self):
        self.wpa_button.setEnabled(True)
        self.wpa_clientlabel.setEnabled(True)

    def wpa_button_false(self):
        self.wpa_button.setEnabled(False)
        self.wpa_clientlabel.setEnabled(False)
        self.wpa_clientlabel.setText('None Detected')

    #
    # WEP SCAN THREADING FOR AUTOMATIC SCAN OF NETWORK
    #
    ###################
    def scan_process1_thread(self):
        global error_catch
        error_catch = variables.exec_command("airodump-ng --write /tmp/fern-log/zfern-wep --output-format csv \
                                    --encrypt wep %s" % (self.monitor_interface))  # FOR WEP

    def scan_process1_thread1(self):
        global error_catch
        error_catch = variables.exec_command("airodump-ng --write /tmp/fern-log/WPA/zfern-wpa --output-format csv \
                                    --encrypt wpa %s" % (self.monitor_interface))  # FOR WPA

    ###################
    def scan_process2_thread(self):
        global error_catch
        if bool(variables.xterm_setting):
            wep_display_mode = 'xterm -T "FERN (WEP SCAN)" -geometry 100 -e'  # if True or if xterm contains valid ascii characters
        else:
            wep_display_mode = ''

        error_catch = variables.exec_command("%s 'airodump-ng -a --write /tmp/fern-log/zfern-wep --output-format csv\
                                        --encrypt wep %s'" % (wep_display_mode, self.monitor_interface))  # FOR WEP

    def scan_process2_thread1(self):
        global error_catch
        if bool(variables.xterm_setting):  # if True or if xterm contains valid ascii characters
            wpa_display_mode = 'xterm -T "FERN (WPA SCAN)" -geometry 100 -e'
        else:
            wpa_display_mode = ''

        error_catch = variables.exec_command("%s 'airodump-ng -a --write /tmp/fern-log/WPA/zfern-wpa \
                                    --output-format csv  --encrypt wpa %s'" % (
        wpa_display_mode, self.monitor_interface))  # FOR WPA

    ###########################
    def scan_process3_thread(self):
        global error_catch
        error_catch = variables.exec_command("airodump-ng --channel %s --write /tmp/fern-log/zfern-wep \
                                    --output-format csv  --encrypt wep %s" % (
        variables.static_channel, self.monitor_interface))  # FOR WEP

    def scan_process3_thread1(self):
        global error_catch
        error_catch = variables.exec_command("airodump-ng --channel %s --write /tmp/fern-log/WPA/zfern-wpa \
                                --output-format csv  --encrypt wpa %s" % (
        variables.static_channel, self.monitor_interface))  # FOR WPA

    #######################
    def scan_process4_thread(self):
        global error_catch
        if bool(variables.xterm_setting):
            wep_display_mode = 'xterm -T "FERN (WEP SCAN)" -geometry 100 -e'  # if True or if xterm contains valid ascii characters
        else:
            wep_display_mode = ''

        error_catch = variables.exec_command("%s 'airodump-ng -a --channel %s --write /tmp/fern-log/zfern-wep \
                                                --output-format csv  --encrypt wep %s'" % (
        wep_display_mode, variables.static_channel, self.monitor_interface))  # FOR WEP

    def scan_process4_thread1(self):
        global error_catch
        if bool(variables.xterm_setting):  # if True or if xterm contains valid ascii characters
            wpa_display_mode = 'xterm -T "FERN (WPA SCAN)" -geometry 100 -e'
        else:
            wpa_display_mode = ''

        error_catch = variables.exec_command("%s 'airodump-ng -a --channel %s --write /tmp/fern-log/WPA/zfern-wpa \
                                                --output-format csv  --encrypt wpa %s'" % (
        wpa_display_mode, variables.static_channel, self.monitor_interface))

    def scan_wep(self):
        global xterm_setting
        variables.exec_command('rm -r /tmp/fern-log/*.csv')
        variables.exec_command('rm -r /tmp/fern-log/*.cap')
        variables.exec_command('rm -r /tmp/fern-log/WPA/*.csv')
        variables.exec_command('rm -r /tmp/fern-log/WPA/*.cap')

        # Channel desision block
        if scan_control == 0:
            if not variables.static_channel:
                if len(variables.xterm_setting) == 0:
                    threading.Thread(target=self.scan_process1_thread).start()
                    threading.Thread(target=self.scan_process1_thread1).start()
                else:
                    threading.Thread(target=self.scan_process2_thread).start()
                    threading.Thread(target=self.scan_process2_thread1).start()
            else:
                if len(variables.xterm_setting) == 0:
                    threading.Thread(target=self.scan_process3_thread).start()
                    threading.Thread(target=self.scan_process3_thread1).start()
                else:
                    threading.Thread(target=self.scan_process4_thread).start()
                    threading.Thread(target=self.scan_process4_thread1).start()

        time.sleep(5)
        if scan_control != 1:
            self.label_7.setText("<font Color=green>\t Active</font>")

        while scan_control != 1:
            try:
                time.sleep(2)

                wep_access_file = str(reader('/tmp/fern-log/zfern-wep-01.csv'))  # WEP access point log file
                wpa_access_file = str(reader('/tmp/fern-log/WPA/zfern-wpa-01.csv'))  # WPA access point log file


                wep_access_convert = wep_access_file[0:wep_access_file.index('Station MAC')]
                wep_access_process = wep_access_convert[wep_access_convert.index('Key'):-1]
                wep_access_process1 = wep_access_process.strip('Key\r\n')
                process = wep_access_process1.splitlines()

                # Display number of WEP access points detected
                wep_devices = 0;
                for line in wpa_access_file.splitlines():
                    if "WEP" in line:
                        wep_devices += 1

                self.wep_count = str(wep_devices)  # number of access points wep detected

                if int(self.wep_count) > 0:
                    self.wep_number_changed_signal.emit()
                    self.wep_button_true_signal.emit()
                else:
                    self.wep_button_false_signal.emit()

                for iterate in range(len(process)):
                    detail_process1 = process[iterate]
                    wep_access = detail_process1.split(',')

                    mac_address = wep_access[0].strip(' ')  # Mac address
                    channel = wep_access[3].strip(' ')  # Channel
                    speed = wep_access[4].strip(' ')  # Speed
                    power = wep_access[8].strip(' ')  # Power
                    access_point = wep_access[13].strip(' ')  # Access point Name

                    if access_point not in wep_details.keys():
                        wep_details[access_point] = [mac_address, channel, speed, power]

                # WPA Access point sort starts here

                # Display number of WEP access points detected
                self.wpa_count = str(wpa_access_file.count('WPA'))  # number of access points wep detected

                wpa_devices = 0;
                for line in wpa_access_file.splitlines():
                    if "WPA" in line or "WPA2" in line:
                        wpa_devices += 1

                self.wpa_count = str(wpa_devices)


                if int(self.wpa_count) == 0:
                    self.wpa_button_false_signal.emit()
                elif int(self.wpa_count) >= 1:
                    self.wpa_button_true_signal.emit()
                    self.wpa_number_changed_signal.emit()
                else:
                    self.wpa_button_false_signal.emit()

                wpa_access_convert = wpa_access_file[0:wpa_access_file.index('Station MAC')]
                wpa_access_process = wpa_access_convert[wpa_access_convert.index('Key'):-1]
                wpa_access_process1 = wpa_access_process.strip('Key\r\n')
                process = wpa_access_process1.splitlines()

                for iterate in range(len(process)):
                    detail_process1 = process[iterate]
                    wpa_access = detail_process1.split(',')

                    mac_address = wpa_access[0].strip(' ')  # Mac address
                    channel = wpa_access[3].strip(' ')  # Channel
                    speed = wpa_access[4].strip(' ')  # Speed
                    power = wpa_access[8].strip(' ')  # Power
                    access_point = wpa_access[13].strip(' ')  # Access point Name

                    if access_point not in wpa_details.keys():
                        wpa_details[access_point] = [mac_address, channel, speed, power]


            except(ValueError, IndexError):
                pass

    def showEvent(self, event):
        self.timer.start()

    def evaliate_permissions(self):
        if os.geteuid() != 0:
            QtWidgets.QMessageBox.warning(self, "Insufficient Priviledge",
                                          "Aircrack and other dependencies need root priviledge to function, Please run application as root")
            sys.exit()

