import os
import re
import sys
import time
import thread
import urllib2
import shutil
import sqlite3
import commands
import subprocess

import variables
from PyQt4 import QtGui,QtCore

from wep import *
from wpa import *
from tools import *
from database import *
from variables import *
from functions import *

from gui.main_window import *

__version__= 1.51

#
# Main Window Class
#
class mainwindow(QtGui.QDialog,Ui_Dialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        self.refresh_interface()
        self.evaliate_permissions()

        self.connect(self,QtCore.SIGNAL("DoubleClicked()"),self.mouseDoubleClickEvent)
        self.connect(self.refresh_intfacebutton,QtCore.SIGNAL("clicked()"),self.refresh_interface)
        self.connect(self.interface_combo,QtCore.SIGNAL("currentIndexChanged(QString)"),self.setmonitor)
        self.connect(self.scan_button,QtCore.SIGNAL("clicked()"),self.scan_network)
        self.connect(self.wep_button,QtCore.SIGNAL("clicked()"),self.wep_attack_window)
        self.connect(self.wpa_button,QtCore.SIGNAL("clicked()"),self.wpa_attack_window)
        self.connect(self.tool_button,QtCore.SIGNAL("clicked()"),self.tool_box_window)
        self.connect(self.database_button,QtCore.SIGNAL("clicked()"),self.database_window)
        self.connect(self.update_button,QtCore.SIGNAL("clicked()"),self.update_fern)
        self.connect(self,QtCore.SIGNAL("finished downloading"),self.finished_downloading_files)
        self.connect(self,QtCore.SIGNAL("restart application"),self.restart_application)
        self.connect(self,QtCore.SIGNAL("failed update"),self.update_fail)
        self.connect(self,QtCore.SIGNAL("already latest update"),self.latest_update)
        self.connect(self,QtCore.SIGNAL("previous message"),self.latest_svn)
        self.connect(self,QtCore.SIGNAL("new update available"),self.new_update_avialable)
        self.connect(self,QtCore.SIGNAL("current_version"),self.current_update)
        self.connect(self,QtCore.SIGNAL("download failed"),self.download_failed)
        self.connect(self,QtCore.SIGNAL('internal scan error'),self.scan_error_display)
        self.connect(self,QtCore.SIGNAL('file downloaded'),self.downloading_update_files)


        self.update_label.setText('<font color=green>Currently installed version: Revision %s</font>'%(self.installed_revision()))

        # Display update status on main_windows
        thread.start_new_thread(self.update_initializtion_check,())

        self.update_database_label()

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
            self.label_16.setText('<font color=green>%s Key Entries</font>'%(str(len(items))))


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

        self.update_label.setText('<font color=green>Downloading.. %s Complete</font>'\
        %(self.percentage(files_downloaded,file_total)))

    def installed_revision(self):
        svn_info = commands.getstatusoutput('svn info ' + directory)
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
        self.update_label.setText('<font color=green>Currently installed version: Revision %s</font>'%(self.installed_revision()))


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
    # Update Fern application via SVN,updates at ("svn checkout http://fern-wifi-cracker.googlecode.com/svn/Fern-Wifi-Cracker/")
    #
    def update_fern(self):
        global updater_control
        updater_control = 1
        self.update_label.setText('<font color=green>Checking for update...</font>')
        thread.start_new_thread(self.update_launcher,())


    def percentage(self,current,total):
        float_point = float(current)/float(total)
        calculation = int(float_point * 100)
        percent = str(calculation) + '%'
        return percent


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

        svn_path = 'http://fern-wifi-cracker.googlecode.com/svn/Fern-Wifi-Cracker/'


        try:
            online_response_check = urllib2.urlopen('http://fern-wifi-cracker.googlecode.com/files/update_control')
            online_response = online_response_check.read()

            online_files = re.compile('total_files = \d{0,9}',re.IGNORECASE)

            for online_file_total in online_response.splitlines():
                if re.match(online_files,online_file_total):
                    file_total = int(online_file_total.split()[2])

            if 'Fern-Wifi-Cracker' in os.listdir('/tmp/'):
                commands.getstatusoutput('rm -r /tmp/Fern-Wifi-Cracker')

            svn_access = subprocess.Popen('cd /tmp/ \n svn checkout http://fern-wifi-cracker.googlecode.com/svn/Fern-Wifi-Cracker/',\
                    shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            svn_update = svn_access.stdout
            thread.start_new_thread(self.update_error,())
            while True:
                response = svn_update.readline()
                if len(response) > 0:
                    files_downloaded += 1
                    self.emit(QtCore.SIGNAL('file downloaded'))

                if str('revision') in str(response):
                    self.emit(QtCore.SIGNAL("finished downloading"))
                                                                                    # Delete all old files (*.py,*.py etc) except ".font_setting.dat" file
                    for old_file in os.listdir(os.getcwd()):
                        if os.path.isfile(os.getcwd() + os.sep + old_file) and old_file != '.font_settings.dat':
                            os.remove(os.getcwd() + os.sep + old_file)
                                                                                    # Delete all old directories except the "key-database" directory
                    for old_directory in os.listdir(os.getcwd()):
                        if os.path.isdir(os.getcwd() + os.sep + old_directory) and old_directory != 'key-database':
                            shutil.rmtree(os.getcwd() + os.sep + old_directory)

                    for update_file in os.listdir('/tmp/Fern-Wifi-Cracker'):        # Copy New update files to working directory
                        if os.path.isfile(update_directory + update_file):
                            shutil.copyfile(update_directory + update_file,os.getcwd() + os.sep + update_file)
                        else:
                            shutil.copytree(update_directory + update_file,os.getcwd() + os.sep + update_file)

                    time.sleep(5)
                    self.emit(QtCore.SIGNAL("restart application"))
                    break
                if len(svn_failure_message) > 2:
                    self.emit(QtCore.SIGNAL("download failed"))
                    break

        except(urllib2.URLError,urllib2.HTTPError):
            self.emit(QtCore.SIGNAL("download failed"))


    #
    # Update checker Thread
    #
    def update_initializtion_check(self):
        global updater_control
        updater_control = 0
        while updater_control != 1:
            try:
                online_response_thread = urllib2.urlopen('http://fern-wifi-cracker.googlecode.com/files/update_control')
                online_response_string = ''
                online_response = online_response_thread.read()

                online_version = re.compile('version = \d{0,9}',re.IGNORECASE)

                for version_iterate in online_response.splitlines():
                    if re.match(online_version,version_iterate):
                        online_response_string += version_iterate

                update_version_number = float(online_response_string.split()[2])

                if float(__version__) != update_version_number:
                    self.emit(QtCore.SIGNAL("new update available"))
                    break
                elif float(__version__) == update_version_number:
                    self.emit(QtCore.SIGNAL("already latest update"))
                    time.sleep(20)
                    self.emit(QtCore.SIGNAL("previous message"))
                    break
                else:
                    pass
            except Exception:
                self.emit(QtCore.SIGNAL("failed update"))
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
            os.mkdir('/tmp/fern-log/WEP-DUMP')
        else:
            commands.getstatusoutput('rm -r /tmp/fern-log/WEP-DUMP/*')
        wep_run = wep_attack_dialog()

        self.connect(wep_run,QtCore.SIGNAL('update database label'),self.update_database_label)
        self.connect(wep_run,QtCore.SIGNAL("stop scan"),self.stop_network_scan)

        wep_run.exec_()

    #
    # Execute the wep attack window
    #
    def wpa_attack_window(self):
        commands.getstatusoutput('killall aircrack-ng')
        if 'WPA-DUMP' not in os.listdir('/tmp/fern-log'):
            os.mkdir('/tmp/fern-log/WPA-DUMP')
        else:
            commands.getstatusoutput('rm -r /tmp/fern-log/WPA-DUMP/*')
        wpa_run = wpa_attack_dialog()

        self.connect(wpa_run,QtCore.SIGNAL('update database label'),self.update_database_label)
        self.connect(wpa_run,QtCore.SIGNAL("stop scan"),self.stop_network_scan)

        wpa_run.exec_()
    #
    # Execute database Window
    #
    def database_window(self):
        database_run = database_dialog()
        self.connect(database_run,QtCore.SIGNAL('update database label'),self.update_database_label)
        database_run.exec_()
    #
    # Refresh wireless network interface card and update combobo
    #
    def refresh_interface(self):
        commands.getstatusoutput('killall airodump-ng')
        commands.getstatusoutput('killall airmon-ng')
        try:
            self.mon_label.setText(" ")
	    self.interface_combo.clear()
            del list_
        except NameError:
            pass

        # Disable cards already on monitor modes
        wireless_interfaces = str(commands.getstatusoutput('airmon-ng'))
        prev_monitor = os.listdir('/sys/class/net')
        monitor_interfaces_list = []
        for monitors in prev_monitor:
            if monitors in wireless_interfaces:
                monitor_interfaces_list.append(monitors)
        for monitored_interfaces in monitor_interfaces_list:
            commands.getstatusoutput('airmon-ng stop %s'%(monitored_interfaces))

        # List Interface cards
        compatible_interface = str(commands.getoutput("airmon-ng | egrep -e '^[a-z]{2,4}[0-9]'"))
        interface_list = os.listdir('/sys/class/net')
        list_ = ['Select Interface']
        # Interate over interface output and update combo box
        if compatible_interface.count('\t') == 0:
            self.interface_combo.addItems(list_)
            self.mon_label.setText("<font color=red>No Wireless Interface was found</font>")
        else:
            for interface in interface_list:
                if interface in compatible_interface:
                    if interface.startswith('mon'):
                        pass
                    else:
                        list_.append(interface)

            self.interface_combo.addItems(list_)
            self.mon_label.setText("<font color=red>Select an interface card</font>")



    #
    # Set monitor mode on selected monitor from combo list
    #
    def setmonitor(self):
        monitor_card = str(self.interface_combo.currentText())
        if monitor_card != 'Select Interface':
            status = str(commands.getoutput("airmon-ng start %s"%(monitor_card)))
            if 'monitor mode enabled' in status:
                monitor_interface_process = str(commands.getoutput("airmon-ng | egrep -e '^[a-z]{2,4}[0-9]'"))
                monitor_interface = monitor_interface_process.splitlines()
                mon_int1 = monitor_interface[-1]
                mon_real = mon_int1[0:6].strip('\t\t')
                remove('/tmp/fern-log','monitor.log')
                write('/tmp/fern-log/monitor.log',mon_real)     # write monitoring interface like(mon0,mon1)to log
                self.mon_label.setText("<font color=green>Monitor Mode Enabled on %s</font>"%(mon_real))

                #
                # Create Fake Mac Address and index for use
                #
                mon_down = commands.getstatusoutput('ifconfig %s down'%(mon_real))
                if settings_exists('mac_address'):
                    commands.getstatusoutput('macchanger -m %s %s'%(read_settings('mac_address'),mon_real))
                else:
                    commands.getstatusoutput('macchanger -A %s'%(mon_real))
                mon_up = commands.getstatusoutput('ifconfig %s up'%(mon_real))
                for iterate in os.listdir('/sys/class/net'):
                    if str(iterate) == str(mon_real):
                        os.chmod('/sys/class/net/' + mon_real + '/address',0777)
                        mac_address = reader('/sys/class/net/' + mon_real + '/address')


                if 'monitor-mac-address.log' in os.listdir('/tmp/fern-log'):
                    remove('/tmp/fern-log','monitor-mac-address.log')
                    write('/tmp/fern-log/monitor-mac-address.log',mac_address)
                else:
                    write('/tmp/fern-log/monitor-mac-address.log',mac_address)


                #
                # Execute tips
                #
                if 'tips-settings.dat' in os.listdir('fern-settings'):
                    if reader('fern-settings/tips-settings.dat') == '1':
                        pass
                    else:
                        tips = tips_window()
                        tips.exec_()
                else:
                    write('fern-settings/tips-settings.dat','')
                    tips = tips_window()
                    tips.exec_()
            else:
                self.mon_label.setText("<font color=red>Monitor Mode not enabled check manually</font>")
	else:pass

    #
    # Double click event for poping of settings dialog box
    #
    def mouseDoubleClickEvent(self, event):
        try:
            setting = settings_dialog()
            setting.exec_()
        except IOError:
            self.mon_label.setText("<font color=red>Enable monitor mode to access settings</font>")


    def scan_error_display(self):
        global error_catch
        self.stop_scan_network()
        QtGui.QMessageBox.warning(self,'Scan Error','Fern failed to start scan due to an airodump-ng error: <font color=red>' \
                                        + error_catch[1] + '</font>')



    #
    # Scan for available networks
    #
    def scan_network(self):
        global scan_control
        scan_control = 0
        if 'monitor.log' not in os.listdir('/tmp/fern-log'):
            self.mon_label.setText("<font color=red>Enable monitor mode before scanning</font>")
        else:
            self.connect(self,QtCore.SIGNAL("wep_number_changed"),self.wep_number_changed)
            self.connect(self,QtCore.SIGNAL("wep_button_true"),self.wep_button_true)
            self.connect(self,QtCore.SIGNAL("wep_button_false"),self.wep_button_false)

            self.connect(self,QtCore.SIGNAL("wpa_number_changed"),self.wpa_number_changed)
            self.connect(self,QtCore.SIGNAL("wpa_button_true"),self.wpa_button_true)
            self.connect(self,QtCore.SIGNAL("wpa_button_false"),self.wpa_button_false)
            self.wpa_button.setEnabled(False)
            self.wep_button.setEnabled(False)
            self.wep_clientlabel.setEnabled(False)
            self.wpa_clientlabel.setEnabled(False)
            self.wep_clientlabel.setText("None Detected")
            self.wpa_clientlabel.setText("None Detected")
            self.label_7.setText("<font Color=green>\t Initializing</font>")
            thread.start_new_thread(self.scan_wep,())
            self.disconnect(self.scan_button,QtCore.SIGNAL("clicked()"),self.scan_network)
            self.connect(self.scan_button,QtCore.SIGNAL("clicked()"),self.stop_scan_network)


    def stop_scan_network(self):
        global error_catch
        global scan_control
        scan_control = 1
        commands.getstatusoutput('rm -r /tmp/fern-log/*.cap')
        commands.getstatusoutput('killall airodump-ng')
        commands.getstatusoutput('killall airmon-ng')
        self.label_7.setText("<font Color=red>\t Stopped</font>")
        self.wep_clientlabel.setText("None Detected")
        self.wpa_clientlabel.setText("None Detected")
        self.disconnect(self.scan_button,QtCore.SIGNAL("clicked()"),self.stop_scan_network)
        self.connect(self.scan_button,QtCore.SIGNAL("clicked()"),self.scan_network)



    def stop_network_scan(self):
        global scan_control
        scan_control = 1
        commands.getstatusoutput('killall airodump-ng')
        commands.getstatusoutput('killall airmon-ng')
        self.label_7.setText("<font Color=red>\t Stopped</font>")

    #
    # WEP Thread SLOTS AND SIGNALS
    #
    def wep_number_changed(self):
        number_access = reader('/tmp/fern-log/number.log')
        self.wep_clientlabel.setText('<font color=red>%s</font><font color=red>\t Detected</font>'%(number_access))

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
        number_access = reader('/tmp/fern-log/WPA/number.log')
        self.wpa_clientlabel.setText('<font color=red>%s</font><font color=red>\t Detected</font>'%(number_access))

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
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        error_catch = commands.getstatusoutput("airodump-ng --write /tmp/fern-log/zfern-wep --output-format csv \
                                    --encrypt wep %s"%(monitor))          #FOR WEP
        if error_catch[0] != 0:
            self.emit(QtCore.SIGNAL('internal scan error'))


    def scan_process1_thread1(self):
        global error_catch
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        error_catch = commands.getstatusoutput("airodump-ng --write /tmp/fern-log/WPA/zfern-wpa --output-format csv \
                                    --encrypt wpa %s"%(monitor))      # FOR WPA
        if error_catch[0] != 0:
            self.emit(QtCore.SIGNAL('internal scan error'))


    ###################
    def scan_process2_thread(self):
        global error_catch
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        if 'static-channel.log' in os.listdir('/tmp/fern-log'):
            channel = str(reader('/tmp/fern-log/static-channel.log'))
        else:
            channel = ''

        if bool(variables.xterm_setting):
            wep_display_mode = 'xterm -T "FERN (WEP SCAN)" -geometry 100 -e'       # if True or if xterm contains valid ascii characters
        else:
            wep_display_mode = ''

        error_catch = commands.getstatusoutput("%s 'airodump-ng -a --write /tmp/fern-log/zfern-wep --output-format csv\
                                        --encrypt wep %s'"%(wep_display_mode,monitor))      #FOR WEP
        if error_catch[0] != 0:
            self.emit(QtCore.SIGNAL('internal scan error'))


    def scan_process2_thread1(self):
        global error_catch
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        if 'static-channel.log' in os.listdir('/tmp/fern-log'):
            channel = str(reader('/tmp/fern-log/static-channel.log'))
        else:
            channel = ''

        if bool(variables.xterm_setting):                                             # if True or if xterm contains valid ascii characters
            wpa_display_mode = 'xterm -T "FERN (WPA SCAN)" -geometry 100 -e'
        else:
            wpa_display_mode = ''

        error_catch = commands.getstatusoutput("%s 'airodump-ng -a --write /tmp/fern-log/WPA/zfern-wpa \
                                    --output-format csv  --encrypt wpa %s'"%(wpa_display_mode,monitor))  # FOR WPA
        if error_catch[0] != 0:
            self.emit(QtCore.SIGNAL('internal scan error'))


    ###########################
    def scan_process3_thread(self):
        global error_catch
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        if 'static-channel.log' in os.listdir('/tmp/fern-log'):
            channel = str(reader('/tmp/fern-log/static-channel.log'))
        else:
            channel = ''

        error_catch = commands.getstatusoutput("airodump-ng --channel %s --write /tmp/fern-log/zfern-wep \
                                    --output-format csv  --encrypt wep %s"%(channel,monitor))    #FOR WEP
        if error_catch[0] != 0:
            self.emit(QtCore.SIGNAL('internal scan error'))


    def scan_process3_thread1(self):
        global error_catch
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        if 'static-channel.log' in os.listdir('/tmp/fern-log'):
            channel = str(reader('/tmp/fern-log/static-channel.log'))
        else:
            channel = ''

        error_catch = commands.getstatusoutput("airodump-ng --channel %s --write /tmp/fern-log/WPA/zfern-wpa \
                                --output-format csv  --encrypt wpa %s"%(channel,monitor))# FOR WPA
        if error_catch[0] != 0:
            self.emit(QtCore.SIGNAL('internal scan error'))

    #######################
    def scan_process4_thread(self):
        global error_catch
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        if 'static-channel.log' in os.listdir('/tmp/fern-log'):
            channel = str(reader('/tmp/fern-log/static-channel.log'))
        else:
            channel = ''

        if bool(variables.xterm_setting):
            wep_display_mode = 'xterm -T "FERN (WEP SCAN)" -geometry 100 -e'       # if True or if xterm contains valid ascii characters
        else:
            wep_display_mode = ''

        error_catch = commands.getstatusoutput("%s 'airodump-ng -a --channel %s --write /tmp/fern-log/zfern-wep \
                                                --output-format csv  --encrypt wep %s'"%(wep_display_mode,channel,monitor))# FOR WEP
        if error_catch[0] != 0:
            self.emit(QtCore.SIGNAL('internal scan error'))

    def scan_process4_thread1(self):
        global error_catch
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        if 'static-channel.log' in os.listdir('/tmp/fern-log'):
            channel = str(reader('/tmp/fern-log/static-channel.log'))
        else:
            channel = ''

        if bool(variables.xterm_setting):                                             # if True or if xterm contains valid ascii characters
            wpa_display_mode = 'xterm -T "FERN (WPA SCAN)" -geometry 100 -e'
        else:
            wpa_display_mode = ''

        error_catch = commands.getstatusoutput("%s 'airodump-ng -a --channel %s --write /tmp/fern-log/WPA/zfern-wpa \
                                                --output-format csv  --encrypt wpa %s'"%(wpa_display_mode,channel,monitor))
        if error_catch[0] != 0:
            self.emit(QtCore.SIGNAL('internal scan error'))

    def scan_wep(self):
        global xterm_setting
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        commands.getstatusoutput('rm -r /tmp/fern-log/*.csv')
        commands.getstatusoutput('rm -r /tmp/fern-log/*.cap')
        commands.getstatusoutput('rm -r /tmp/fern-log/WPA/*.csv')
        commands.getstatusoutput('rm -r /tmp/fern-log/WPA/*.cap')

        # Stactic channel settings consideration

        if 'static-channel.log' in os.listdir('/tmp/fern-log'):
            channel = str(reader('/tmp/fern-log/static-channel.log'))
        else:
            channel = ''

        # Channel desision block
        if scan_control == 0:
            if 'static-channel.log' not in os.listdir('/tmp/fern-log'):
                if len(variables.xterm_setting) == 0:
                    thread.start_new_thread(self.scan_process1_thread,())
                    thread.start_new_thread(self.scan_process1_thread1,())

                else:
                    thread.start_new_thread(self.scan_process2_thread,())
                    thread.start_new_thread(self.scan_process2_thread1,())
            else:
                if len(variables.xterm_setting) == 0:
                    thread.start_new_thread(self.scan_process3_thread,())
                    thread.start_new_thread(self.scan_process3_thread1,())
                else:
                    thread.start_new_thread(self.scan_process4_thread,())
                    thread.start_new_thread(self.scan_process4_thread1,())

        time.sleep(5)
        if scan_control != 1:
            self.label_7.setText("<font Color=green>\t Active</font>")

        commands.getstatusoutput('touch /tmp/fern-log/wep_details.log')
        commands.getstatusoutput('touch /tmp/fern-log/WPA/wpa_details.log')

        while scan_control != 1:
            try:
                time.sleep(2)

                wep_access_file = str(reader('/tmp/fern-log/zfern-wep-01.csv'))        # WEP access point log file
                wpa_access_file = str(reader('/tmp/fern-log/WPA/zfern-wpa-01.csv'))     # WPA access point log file

                number_access = str(wep_access_file.count('WEP')/2)        # number of access points wep detected
                try:
                    remove('/tmp/fern-log','number.log')
                except IOError:
                    pass
                write('/tmp/fern-log/number.log','%s'%(number_access))
                if int(number_access) > 0:
                    self.emit(QtCore.SIGNAL("wep_number_changed"))
                    self.emit(QtCore.SIGNAL("wep_button_true"))

                else:
                    self.emit(QtCore.SIGNAL("wep_button_false"))


                wep_access_convert = wep_access_file[0:wep_access_file.index('Station MAC')]
                wep_access_process = wep_access_convert[wep_access_convert.index('Key'):-1]
                wep_access_process1 = wep_access_process.strip('Key\r\n')
                process = wep_access_process1.splitlines()

                for iterate in range(len(process)):
                    detail_process1 = process[iterate]
                    wep_access = detail_process1.split(',')

                    mac_address =   wep_access[0].strip(' ')   # Mac address
                    channel =       wep_access[3].strip(' ')   # Channel
                    speed =         wep_access[4].strip(' ')   # Speed
                    power =         wep_access[8].strip(' ')   # Power
                    access_point =  wep_access[13].strip(' ')  # Access point Name

                    if access_point not in wep_details.keys():
                        wep_details[access_point] = [mac_address,channel,speed,power]


                # WPA Access point sort starts here
                read_wpa = reader('/tmp/fern-log/WPA/zfern-wpa-01.csv')
                number_access_wpa = str(read_wpa.count('WPA'))        # number of access points wep detected
                try:
                    remove('/tmp/fern-log/WPA','number.log')
                except IOError:
                    pass
                write('/tmp/fern-log/WPA/number.log','%s'%(number_access_wpa))

                if int(number_access_wpa) == 0:
                    self.emit(QtCore.SIGNAL("wpa_button_false"))
                elif int(number_access_wpa) > 0:
                    self.emit(QtCore.SIGNAL("wpa_button_true"))
                    self.emit(QtCore.SIGNAL("wpa_number_changed"))
                else:
                    self.emit(QtCore.SIGNAL("wpa_button_false"))


                wpa_access_convert = wpa_access_file[0:wpa_access_file.index('Station MAC')]
                wpa_access_process = wpa_access_convert[wpa_access_convert.index('Key'):-1]
                wpa_access_process1 = wpa_access_process.strip('Key\r\n')
                process = wpa_access_process1.splitlines()

                for iterate in range(len(process)):
                    detail_process1 = process[iterate]
                    wpa_access = detail_process1.split(',')

                    mac_address =   wpa_access[0].strip(' ')   # Mac address
                    channel =       wpa_access[3].strip(' ')   # Channel
                    speed =         wpa_access[4].strip(' ')   # Speed
                    power =         wpa_access[8].strip(' ')   # Power
                    access_point =  wpa_access[13].strip(' ')  # Access point Name

                    if access_point not in wpa_details.keys():
                        wpa_details[access_point] = [mac_address,channel,speed,power]



            except(ValueError,IndexError):
                pass



    def evaliate_permissions(self):
        if os.getenv('LOGNAME','none').lower() != 'root':
            QtGui.QMessageBox.warning(self,"Insufficient Priviledge","Aircrack and other dependencies need root priviledge to function, Please run application as root")
            sys.exit()

